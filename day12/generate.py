
import time

from openai import OpenAI

import config


# Connect to local Ollama LLM endpoint
client = OpenAI(
    base_url=config.LLM_BASE_URL,
    api_key=config.LLM_API_KEY,
)


def generate_answer(query: str, chunks: list[dict]) -> dict:
    start_time = time.perf_counter()

    # Combine retrieved chunks into context
    context = "\n\n".join(
        f"Source: {chunk['source']}, Page: {chunk['page']}\n"
        f"{chunk['content']}"
        for chunk in chunks
    )

    system_message = config.SYSTEM_PROMPT.format(
        context=context
    )

    response = client.chat.completions.create(
        model=config.LLM_MODEL,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": query},
        ],
        temperature=config.TEMPERATURE,
        reasoning_effort=config.REASONING_EFFORT,
        **{config.TOKEN_LIMIT_PARAM: config.MAX_TOKENS},
    )

    generation_time_ms = round(
        (time.perf_counter() - start_time) * 1000, 2
    )

    answer = response.choices[0].message.content or ""
    finish_reason = response.choices[0].finish_reason

    if not answer.strip():
        print(
            f"WARNING: The model returned an empty answer. "
            f"Finish reason: {finish_reason}"
        )

    usage = response.usage

    return {
        "query": query,
        "answer": answer.strip(),
        "context_used": context,
        "model": config.LLM_MODEL,
        "thinking": False,
        "finish_reason": finish_reason,
        "generation_time_ms": generation_time_ms,
        "prompt_tokens": usage.prompt_tokens if usage else 0,
        "tokens_generated": usage.completion_tokens if usage else 0,
    }


if __name__ == "__main__":
    from retrieve import retrieve_chunks

    test_query = "What is the company's remote work policy?"

    retrieval_result = retrieve_chunks(test_query)

    result = generate_answer(
        query=test_query,
        chunks=retrieval_result["retrieved_chunks"],
    )

    print("\nQuestion:", result["query"])
    print("\nAnswer:", result["answer"])
    print("\nModel:", result["model"])
    print("Thinking:", result["thinking"])
    print("Finish reason:", result["finish_reason"])
    print("Generation time:", result["generation_time_ms"], "ms")
    print("Prompt tokens:", result["prompt_tokens"])
    print("Tokens generated:", result["tokens_generated"])
