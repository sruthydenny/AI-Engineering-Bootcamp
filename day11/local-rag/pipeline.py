
import json
from pathlib import Path

from retrieve import retrieve_chunks
from generate import generate_answer


def answer_question(query: str) -> dict:
    retrieval_result = retrieve_chunks(query)

    generation_result = generate_answer(
        query=query,
        chunks=retrieval_result["retrieved_chunks"],
    )

    return {
        **generation_result,
        "retrieval": retrieval_result,
    }


if __name__ == "__main__":
    base_dir = Path(__file__).parent

    # Load test questions
    with open(base_dir / "test_questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    # Load your saved manual ratings
    ratings_path = base_dir / "ratings.json"

    with open(ratings_path, "r", encoding="utf-8") as f:
        ratings = json.load(f)

    output_path = base_dir / "pipeline_outputs.json"
    outputs = []

    for index, item in enumerate(questions, start=1):
        question_id = item["id"]

        print(f"\n[{index}/{len(questions)}] {item['question']}")

        result = answer_question(item["question"])
        retrieval = result["retrieval"]

        # Reuse the saved rating for this question ID
        saved_rating = ratings.get(question_id, {})

        output = {
            "id": question_id,
            "question": item["question"],
            "expected_answer": item["expected_answer"],
            "actual_answer": result["answer"],
            "retrieved_context": [
                chunk["content"]
                for chunk in retrieval["retrieved_chunks"]
            ],
            "context_sources": [
                {
                    "source": chunk["source"],
                    "page": chunk["page"]
                }
                for chunk in retrieval["retrieved_chunks"]
            ],
            "model": result["model"],
            "thinking": result["thinking"],
            "finish_reason": result["finish_reason"],
            "embedding_model": retrieval["embedding_model"],
            "prompt_tokens": result["prompt_tokens"],
            "tokens_generated": result["tokens_generated"],
            "retrieval_time_ms": retrieval["retrieval_time_ms"],
            "generation_time_ms": result["generation_time_ms"],
            "passed": saved_rating.get("passed"),
            "rating_note": saved_rating.get("rating_note", "")
        }

        outputs.append(output)

        # Save after each question
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(outputs, f, indent=2, ensure_ascii=False)

        print("Answer:", result["answer"])
        print("Generation time:", result["generation_time_ms"], "ms")

    print(f"\nCompleted all {len(outputs)} questions.")
    print(f"Results saved to: {output_path}")
