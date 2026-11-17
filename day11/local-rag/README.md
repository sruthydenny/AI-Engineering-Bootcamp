# Local RAG Document Q&A System

## Overview

This project implements a fully local Retrieval-Augmented Generation (RAG) system that answers questions using information from PDF documents.

The system extracts text from PDFs, splits it into chunks, generates local embeddings, stores them in ChromaDB, retrieves relevant content, and generates answers using a locally running Ollama language model.

## Technologies Used

- Python 3.12
- uv for Python project and dependency management
- Ollama for running local language models
- ChromaDB for vector storage
- all-minilm for local embeddings
- LangChain text splitters for document chunking
- PyPDF for PDF text extraction
- OpenAI-compatible client for communicating with Ollama

## Project Structure

```text
local-rag/
├── documents/                  # Source PDF documents
├── chroma_db/                  # Local ChromaDB storage (generated)
├── config.py                   # Configuration settings
├── ingest.py                   # PDF ingestion and embedding
├── retrieve.py                 # Relevant chunk retrieval
├── generate.py                 # Answer generation
├── pipeline.py                 # Complete RAG pipeline
├── benchmark.py                # Model benchmarking
├── test_questions.json         # Test questions
├── ratings.json                # Manual question ratings
├── benchmark_results.json      # Benchmark results
├── pipeline_outputs.json       # RAG pipeline outputs
├── decision_log.md              # Implementation decisions
├── README.md                    # Project documentation
└── AGENTS.md                    # AI assistant instructions
```

## Requirements

- Python 3.12 or later
- uv
- Ollama

Required local Ollama models:

- qwen3.5:4b-q4_K_M (final language model)
- all-minilm (final embedding model)

Additional models used for comparison:

- qwen3.5:2b-q4_K_M
- nomic-embed-text

## Setup

Install the project dependencies:

```bash
uv sync
```

Make sure Ollama is running and the required models are available:

```bash
ollama list
```

## Adding Documents

Place PDF documents inside the `documents/` directory.

## Running the RAG Pipeline

First, ingest the PDF documents and build the local vector database:

```bash
uv run python ingest.py
```

Then run the question-answering pipeline:

```bash
uv run python pipeline.py
```

The pipeline retrieves relevant document chunks and generates answers using the local Ollama model.

## Running the Benchmark

Run the benchmark script:

```bash
uv run python benchmark.py
```

The benchmark compares two local language models using different task categories. Results are saved in `benchmark_results.json`.

## Benchmark Results

The benchmark compares:

- `qwen3.5:4b-q4_K_M`
- `qwen3.5:2b-q4_K_M`

The 4B model achieved a higher average quality rating, while the 2B model completed the benchmark faster.

See `benchmark_results.json` for individual responses, timings, token generation rates, and quality ratings.

## Rebuilding the Vector Database

The ChromaDB database is generated locally and is not included in version control.

To rebuild it after adding or changing PDF documents, run:

```bash
uv run python ingest.py
```

## AI Assistance Disclosure

ChatGPT was used for guidance and troubleshooting during development.