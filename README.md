# local-rag-wyrd
Local RAG system for answering questions from the Wyrd company wiki using Ollama, LangChain, and ChromaDB.
# Local RAG for Wyrd Wiki

This project implements a local Retrieval-Augmented Generation (RAG) system to answer questions from the Wyrd company wiki.

## Stack
- Ollama (LLM + embeddings)
- LangChain
- ChromaDB
- Python

## Pipeline
Wiki Markdown → Chunking → Embeddings → Vector DB → Retrieval → LLM → Answer

## Run

Install dependencies:

pip install -r requirements.txt

Index documents:

python loading_content.py

Ask questions:

python query.py
