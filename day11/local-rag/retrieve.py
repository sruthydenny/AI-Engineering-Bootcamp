
import time
from pathlib import Path

import chromadb
from openai import OpenAI

import config

embedding_client = OpenAI(
    base_url=config.EMBEDDING_BASE_URL,
    api_key=config.LLM_API_KEY,
)



BASE_DIR = Path(__file__).parent
CHROMA_DIR = BASE_DIR / "chroma_db"

chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = chroma_client.get_collection(
    name=config.COLLECTION_NAME
)


def retrieve_chunks(query: str) -> dict:
    start_time = time.perf_counter()

    
    response = embedding_client.embeddings.create(
        model=config.EMBEDDING_MODEL,
        input=[query],
    )
    query_embedding = response.data[0].embedding

    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=config.TOP_K,
        include=["documents", "metadatas", "distances"],
    )

    retrieved_chunks = []

    for i in range(len(results["documents"][0])):
        distance = results["distances"][0][i]

        retrieved_chunks.append({
            "content": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "page": results["metadatas"][0][i]["page"],
            "relevance_score": round(1 - distance, 4),
        })

    retrieval_time_ms = round(
        (time.perf_counter() - start_time) * 1000, 2
    )

    return {
        "query": query,
        "retrieved_chunks": retrieved_chunks,
        "retrieval_time_ms": retrieval_time_ms,
        "embedding_model": config.EMBEDDING_MODEL,
    }


if __name__ == "__main__":
    test_query = "An employee clicked a phishing email but did not submit credentials. What incident priority applies and what are the response time requirements?"
    result = retrieve_chunks(test_query)

    print(f"\nQuery: {result['query']}")
    print(f"Retrieval time: {result['retrieval_time_ms']} ms")
    print(f"Embedding model: {result['embedding_model']}")

    for i, chunk in enumerate(result["retrieved_chunks"], start=1):
        print(f"\n--- Result {i} ---")
        print(f"Source: {chunk['source']}")
        print(f"Page: {chunk['page']}")
        print(f"Relevance: {chunk['relevance_score']}")
        print(f"Content: {chunk['content'][:400]}")
