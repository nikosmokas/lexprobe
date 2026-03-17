# LexProbe

LexProbe is an AI-powered legal document analysis system designed to detect risks, explain clauses, and assist users in understanding contracts before signing them.

This project explores modern AI architecture concepts including document ingestion, Retrieval Augmented Generation (RAG), vector databases, and LLM-powered reasoning.

The goal is to build a production-style AI system that analyzes legal documents using a knowledge base of European legislation and legal references.

## Features

* Upload and analyze legal documents (PDF / DOCX)
* Automatic clause extraction and explanation
* AI-powered contract risk detection
* Retrieval Augmented Generation (RAG) over legal texts
* Natural language queries over legal knowledge
* Vector search for relevant legislation

Example queries:

* "Is this NDA safe to sign?"
* "Explain this clause in simple terms."
* "Does this contract comply with EU regulations?"

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
