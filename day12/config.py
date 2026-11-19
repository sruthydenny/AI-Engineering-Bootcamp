
import os

# Local LLM connection
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434/v1")
LLM_API_KEY = os.getenv("LLM_API_KEY", "ollama")
LLM_MODEL = os.getenv("LLM_MODEL", "qwen3.5:4b-q4_K_M")

# Local embedding model
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-minilm")
EMBEDDING_BASE_URL = os.getenv(
    "EMBEDDING_BASE_URL",
    "http://localhost:11434/v1",
)

# Document chunking and retrieval
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 8
COLLECTION_NAME = "bootcamp_docs"

# Instructions for answering document questions
SYSTEM_PROMPT = """You are a helpful assistant answering questions based on provided context.

Use ONLY the context below to answer.

Instructions:
1. Read all the provided context before answering.
2. Identify every part of the question and answer each part.
3. Use relevant facts even if they appear in different chunks or pages.
4. Do not say information is missing if it appears anywhere in the context.
5. Do not invent facts or use outside knowledge.
6. If the answer is not in the context, say "I cannot find this information in the provided documents."

Context:

{context}
"""

# Generation settings
TEMPERATURE = 1
REASONING_EFFORT = os.getenv("REASONING_EFFORT", "none")
MAX_TOKENS = 1024
TOKEN_LIMIT_PARAM = os.getenv("TOKEN_LIMIT_PARAM", "max_tokens")
