# 🧠 Flask + Ollama + Chroma RAG App

This is a **Retrieval-Augmented Generation (RAG)** web application built with:

- **Flask** — Python web framework
- **LangChain** — orchestration for LLMs, prompts, retrieval
- **Ollama** — runs local LLMs and embedding models
- **Chroma** — local vector database for storing embeddings

The app lets you:
1. Upload documents (`.txt`, `.md`, `.pdf`)
2. Embed them into a Chroma DB using Ollama embeddings
3. Ask natural language questions in a simple web UI
4. Get answers grounded in your documents via retrieval

---

## ✨ Features

- **Web UI** to upload files and ask questions
- **Automatic document chunking** for better retrieval
- **Persistent vector database** (`chroma_db/`) so embeddings survive restarts
- **Local LLM & embeddings** via Ollama (no cloud API required)
- **RAG pipeline**: Retriever → Prompt → Model → Answer

---

## 📂 Project Structure

<!-- thest -->