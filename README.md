# LexProbe

LexProbe is an AI-powered legal document analysis system designed to detect risks, explain clauses, and assist users in understanding contracts before signing them.

This project explores modern AI architecture concepts including document ingestion, Retrieval Augmented Generation (RAG), vector databases, and LLM-powered reasoning.

The goal is to build a production-style AI system that analyzes legal documents using a knowledge base of European legislation and legal references.

## Features

* Upload and analyze legal documents (PDF / DOCX / TXT)
* Automatic clause extraction and explanation
* AI-powered contract risk detection
* Retrieval Augmented Generation (RAG) over legal texts
* Natural language queries over legal knowledge
* Vector search for relevant legislation

Example queries:

* "Is this NDA safe to sign?"
* "Explain this clause in simple terms."
* "Does this contract comply with EU regulations?"

## Local Qdrant startup

For local vector storage using Qdrant, run:

```bash
docker run -p 6333:6333 -v ${PWD}/qdrant_storage:/qdrant/storage qdrant/qdrant
```

## Deployment

### Deployment Options

Choose your deployment target:

#### 🚀 **Railway (Recommended for beginners)**
1. Create [Railway](https://railway.app) account
2. Connect your GitHub repo
3. Add `GEMINI_API_KEY` environment variable
4. Push to main - Railway auto-deploys using `docker-compose.yml`

#### 🖥️ **VPS (DigitalOcean/Linode/AWS EC2)**
1. Provision a VPS with Docker installed
2. Add SSH key to `authorized_keys`
3. Set these GitHub secrets:
   - `SERVER_HOST`: your-server.com
   - `SERVER_USER`: root
   - `SERVER_SSH_KEY`: your private SSH key
   - `GEMINI_API_KEY`: your API key
4. Use `.github/workflows/deploy-vps.yml`

#### ☁️ **Cloud Platforms**
- **Render**: Connect repo, auto-deploys Docker
- **AWS ECS**: Use docker-compose with ECS context
- **Google Cloud Run**: Deploy containers directly
- **Azure Container Instances**: Quick container deployment

#### 🏠 **Local Development**
```bash
export GEMINI_API_KEY="your-key"
docker-compose up --build
```

### Manual Deployment

1. **Start Qdrant:**
   ```bash
   docker run -p 6333:6333 -v ${PWD}/qdrant_storage:/qdrant/storage qdrant/qdrant
   ```

2. **Start Backend:**
   ```bash
   pip install -r requirements.txt
   uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Start Frontend:**
   ```bash
   cd ui && python -m http.server 5500
   ```

### CI/CD

The project includes GitHub Actions CI/CD pipeline (`.github/workflows/ci-cd.yml`) that:
- Runs tests and linting
- Builds Docker images
- Deploys to production

Set these secrets in your GitHub repository:
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

## Architecture

The system follows a modern AI pipeline:

Document Upload
→ Text Extraction
→ Chunking & Embeddings
→ Vector Database
→ RAG Retrieval
→ LLM Analysis
→ Risk Report

## Tech Stack

Backend:

* FastAPI

AI / ML:

* LLMs (OpenAI / local models)
* Embeddings

Data:

* Chroma or Qdrant (vector database)

Infrastructure:

* Docker
* Kubernetes (local cluster)

## Project Structure

```
lexprobe/
├── .env
├── .git/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── app/
│   ├── api/
│   │   ├── main.py
│   │   ├── mcp_agent.py
│   │   └── __pycache__/
│   ├── rag/
│   │   ├── embed.py
│   │   ├── generate.py
│   │   ├── prompt.py
│   │   ├── rag_pipeline.py
│   │   ├── rerank.py
│   │   ├── retrieve.py
│   │   ├── utils.py
│   │   └── __pycache__/
│   └── tools/
│       ├── parse_document.py
│       ├── risk_analysis.py
│       └── search_legal_db.py
├── data/
│   ├── processed/
│   │   └── legal_chunks.jsonl
│   └── raw/
│       ├── eurlex_html/
│       └── test/
├── scripts/
│   ├── embed_and_upload.py
│   ├── parse_eurlex.py
│   └── test_search.py
└── ui/
    ├── app.js
    └── index.html
```

## Legal Knowledge Sources

LexProbe builds its knowledge base from publicly available legal datasets such as:

* EUR-Lex (European Union legislation)
* GDPR documentation
* Public legal texts and regulatory documents

These documents are processed, chunked, and embedded to enable semantic retrieval during document analysis.

## Disclaimer

LexProbe is an experimental AI system and **does not provide legal advice**.
Always consult a qualified legal professional before making legal decisions.

## Project Goals

This project is designed as a learning platform for:

* AI solution architecture
* Retrieval Augmented Generation (RAG)
* document processing pipelines
* AI agents and tool usage
* scalable AI system design

