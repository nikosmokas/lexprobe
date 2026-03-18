import os
import re
import json
from bs4 import BeautifulSoup

INPUT_DIR = "../datasets/eurlex_html"
OUTPUT_FILE = "../data/processed/legal_chunks.jsonl"

CHUNK_SIZE = 300


def extract_celex_from_html(soup, fallback_filename):
    # BEST source: <h1>
    h1 = soup.find("h1")
    if h1:
        text = h1.get_text(strip=True)
        if re.match(r"\d{4}[A-Z]\d+", text):
            return text

    # fallback to filename
    match = re.search(r"(\d{4}[A-Z]\d+)", fallback_filename)
    return match.group(1) if match else "unknown"


def extract_title(soup):
    strong = soup.find("strong")
    return strong.get_text(strip=True) if strong else ""


def clean_text(text):
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def remove_annex(text):
    # Cut everything after ANNEX (important!)
    parts = re.split(r"\bANNEX\b", text, flags=re.IGNORECASE)
    return parts[0]


def chunk_text(text, size=CHUNK_SIZE):
    words = text.split()
    for i in range(0, len(words), size):
        yield " ".join(words[i:i + size])


def is_valid_chunk(text):
    if len(text.split()) < 40:
        return False

    blacklist = [
        r"passport",
        r"date of birth",
        r"place of birth",
        r"nationality",
        r"alias",
        r"born",
    ]

    for pattern in blacklist:
        if re.search(pattern, text, re.IGNORECASE):
            return False

    return True


def parse_html_file(filepath):
    filename = os.path.basename(filepath)

    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "xml")

    celex_id = extract_celex_from_html(soup, filename)
    title = extract_title(soup)

    text_div = soup.find("div", {"id": "TexteOnly"})
    if not text_div:
        return

    full_text = clean_text(text_div.get_text(" ", strip=True))

    # 🔥 remove annex garbage
    full_text = remove_annex(full_text)

    # split articles
    parts = re.split(r"(Article\s+\d+)", full_text, flags=re.IGNORECASE)

    for i in range(1, len(parts), 2):
        article_title = parts[i]
        article_text = parts[i + 1]

        article_text = clean_text(article_text)

        chunk_id = 0
        for chunk in chunk_text(article_text):

            if not is_valid_chunk(chunk):
                continue

            yield {
                "doc_id": celex_id,
                "title": title,
                "article": article_title,
                "chunk_id": chunk_id,
                "text": chunk,
                "source": "eur-lex"
            }

            chunk_id += 1


def run_pipeline():
    all_files = []

    for root, _, files in os.walk(INPUT_DIR):
        for file in files:
            if file.lower().endswith((".html", ".xhtml")):
                all_files.append(os.path.join(root, file))

    total_files = len(all_files)

    print(f"Found {total_files} files")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    total_chunks = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:

        for i, path in enumerate(all_files):
            try:
                for chunk in parse_html_file(path):
                    f_out.write(json.dumps(chunk, ensure_ascii=False) + "\n")
                    total_chunks += 1

                if (i + 1) % 200 == 0 or (i + 1) == total_files:
                    print(f"{i+1}/{total_files} processed")

            except Exception as e:
                print(f"Skipping {path}: {e}")

    print("\n✅ DONE")
    print(f"Files: {total_files}")
    print(f"Chunks: {total_chunks}")


if __name__ == "__main__":
    run_pipeline()