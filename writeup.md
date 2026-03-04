# Local RAG System – Design Notes

## Overview

The goal of this project was to build a local Retrieval-Augmented Generation (RAG) system capable of answering questions from a company wiki.

The system works by indexing the wiki content into a vector database and retrieving relevant chunks of text when a user asks a question. Those chunks are then passed to a local language model to generate an answer.

The entire pipeline runs locally using Ollama to avoid API costs.

Pipeline:

Wiki Markdown → Chunking → Embeddings → ChromaDB → Retrieval → LLM → Answer


## Chunking Strategy

The wiki was exported as Markdown files. These documents were combined and split using a RecursiveCharacterTextSplitter.

Configuration used:

chunk_size = 700  
chunk_overlap = 100

Reasoning:

Large documents cannot be embedded effectively as a single unit. Smaller chunks improve retrieval accuracy because semantic search operates on localized context.

700 characters was chosen as a balance between:

• retaining enough semantic context  
• keeping chunks small enough for effective retrieval

The 100 character overlap ensures that information near chunk boundaries is not lost during retrieval.


## Embedding Model

Embeddings were generated using the model:

nomic-embed-text (via Ollama)

This model was selected because it:

• runs locally  
• produces high quality semantic embeddings  
• is optimized for retrieval tasks


## Vector Database

ChromaDB was used as the vector database.

Reasons:

• simple setup  
• local persistence  
• good integration with LangChain


## Retrieval Strategy

When a user submits a query:

1. The query is embedded using the same embedding model.
2. ChromaDB performs similarity search.
3. The top-k most relevant chunks are retrieved.
4. These chunks are used as context for the LLM.

The retriever was configured to return 5 chunks to improve recall.


## Where the System Breaks

Several limitations exist:

1. **Chunk Boundary Problems**

Important information may be split across chunks and the retriever may fail to retrieve both parts.

2. **No Reranking**

The system currently relies on raw vector similarity. A reranking model could significantly improve answer quality.

3. **No Metadata Filtering**

Chunks currently lack metadata like section titles or page names, which could improve retrieval precision.

4. **Prompt Sensitivity**

If the prompt is poorly structured, the LLM may still hallucinate even when context is provided.


## What I Would Improve

If this system were productionized, I would improve it in several ways:

1. **Structured Chunking**

Split documents based on headings instead of raw character length.

2. **Add Metadata**

Store document titles and sections in the vector database.

3. **Hybrid Search**

Combine vector search with keyword search.

4. **Reranking Model**

Use a cross-encoder to rerank retrieved chunks.

5. **Evaluation**

Introduce retrieval metrics such as Recall@K and manual evaluation sets.


## Final Thoughts

This project demonstrates a simple but functional local RAG pipeline.

The system successfully retrieves relevant information from the documentation and generates answers without relying on external APIs.

While the current implementation is minimal, the architecture can be extended with better chunking strategies, reranking models, and metadata-aware retrieval.
