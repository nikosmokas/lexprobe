const chat = document.getElementById("chat");
const spinner = document.getElementById("spinner");
let isContractMode = false;

function addMessage(payload, type) {
  const div = document.createElement("div");
  div.className = "msg " + type;

  if (type === "bot") {
    // Structured message
    const title = document.createElement("h3");
    title.textContent = payload.title || "Legal Explanation";
    div.appendChild(title);

    const ul = document.createElement("ul");
    payload.points.forEach(p => {
      const li = document.createElement("li");
      li.textContent = p;
      ul.appendChild(li);
    });
    div.appendChild(ul);

    const sources = document.createElement("div");
    sources.className = "sources";
    sources.innerHTML = "Sources:<br>" + payload.sources.map(s => `- ${s.doc_id} (${s.article})`).join("<br>");
    div.appendChild(sources);

    const conf = document.createElement("div");
    conf.className = "confidence";
    conf.textContent = `Confidence: ${payload.confidence}`;
    div.appendChild(conf);

  } else {
    // user message
    div.textContent = payload;
  }

  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function ask() {
  const input = document.getElementById("question");
  const question = input.value.trim();
  if (!question) return;

  addMessage(question, "user");
  input.value = "";

  spinner.style.display = "block";

  try {
    const res = await fetch(`http://127.0.0.1:8000/ask?q=${encodeURIComponent(question)}`);
    const data = await res.json();

    console.log("API RESPONSE:", data);

    const payload = data.answer;

    // Convert API response into structured format for the chat
    let structuredPayload = {
      title: payload.title || "Legal Explanation",
      points: payload.points || payload.answer.split("\n").filter(p => p.trim() !== ""),
      sources: payload.sources || [],
      confidence: payload.confidence || 0
    };

    addMessage(structuredPayload, "bot");

  } catch (err) {
    addMessage("Error: " + err.message, "bot");
  }

  spinner.style.display = "none";
}

function toggleMode() {
  isContractMode = !isContractMode;
  const inputBox = document.getElementById("inputBox");
  const uploadBox = document.getElementById("uploadBox");
  const button = document.querySelector("button[onclick='toggleMode()']");

  if (isContractMode) {
    inputBox.style.display = "none";
    uploadBox.style.display = "block";
    button.textContent = "Switch to Q&A";
  } else {
    inputBox.style.display = "flex";
    uploadBox.style.display = "none";
    button.textContent = "Switch to Contract Analysis";
  }
}

async function uploadAndAnalyze() {
  const fileInput = document.getElementById("fileInput");
  const promptInput = document.getElementById("contractPrompt");

  const file = fileInput.files[0];
  const prompt = promptInput.value.trim();

  if (!file) {
    alert("Please select a file");
    return;
  }
  if (!prompt) {
    alert("Please enter a prompt");
    return;
  }

  addMessage(`Uploaded: ${file.name} - Prompt: ${prompt}`, "user");

  spinner.style.display = "block";

  try {
    // First, upload the file
    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_prompt", prompt);

    const uploadRes = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData
    });

    const uploadData = await uploadRes.json();
    const fileId = uploadData.file_id;

    // Then, analyze
    const analyzeFormData = new FormData();
    analyzeFormData.append("file_id", fileId);

    const analyzeRes = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      body: analyzeFormData
    });

    const analyzeData = await analyzeRes.json();

    console.log("ANALYZE RESPONSE:", analyzeData);

    const payload = analyzeData.answer;

    addMessage(payload, "bot");

  } catch (err) {
    addMessage("Error: " + err.message, "bot");
  }

  spinner.style.display = "none";
  fileInput.value = "";
  promptInput.value = "";
}