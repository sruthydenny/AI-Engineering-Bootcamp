import json
import time
from pathlib import Path

from openai import OpenAI


MODELS = ["qwen3.5:9b-q4_K_M"]
BASE_URL = "http://localhost:11434/v1"
API_KEY = "ollama"
REASONING_EFFORT = "none"
OUTPUT_FILE = Path(__file__).with_name("benchmark_results_9b.json")

PROMPTS = [
    {
        "category": "factual",
        "prompt": "What causes tides on Earth? Answer in 2-3 sentences.",
    },
    {
        "category": "reasoning",
        "prompt": (
            "If a train travels 120 km in 1.5 hours, and then 80 km in 1 hour, "
            "what is the average speed for the entire journey? Show the calculation."
        ),
    },
    {
        "category": "summarization",
        "prompt": (
            "Summarize this paragraph in exactly two sentences: "
            "The annual review found that customer support response times improved after "
            "the team introduced shift handoff notes and a shared triage queue. The busiest "
            "period was still Monday morning, when unresolved tickets increased by 18 percent."
        ),
    },
    {
        "category": "structured",
        "prompt": (
            'List 3 European capitals and their countries. Respond ONLY with valid JSON '
            'in this form: [{"city": "string", "country": "string"}]'
        ),
    },
    {
        "category": "code_generation",
        "prompt": (
            "Write a Python function named average_of_positive that accepts a list of numbers "
            "and returns the average of only the positive values. Return 0.0 if there are "
            "no positive values."
        ),
    },
    {
        "category": "instruction_following",
        "prompt": (
            "Create an email sign-off plan. Use exactly four bullet points, with each bullet "
            "containing only a noun and a period. Do not include an introduction or conclusion."
        ),
    },
    {
        "category": "classification",
        "prompt": (
            "Classify the following sentence as Positive, Negative, or Neutral, and output "
            "only the label: 'The software update was released on schedule.'"
        ),
    },
]


def run_benchmark(model: str, prompt_item: dict) -> dict:
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
    start = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt_item["prompt"]}],
        temperature=0.7,
        reasoning_effort=REASONING_EFFORT,
        max_tokens=1024,
    )
    elapsed = time.perf_counter() - start
    choice = response.choices[0]
    usage = response.usage
    completion_tokens = usage.completion_tokens if usage else None
    response_text = choice.message.content or ""

    if not response_text.strip():
        print(
            f"WARNING: Empty response for model={model}, "
            f"category={prompt_item['category']}"
        )

    return {
        "model": model,
        "category": prompt_item["category"],
        "prompt": prompt_item["prompt"],
        "response": response_text,
        "thinking": REASONING_EFFORT != "none",
        "finish_reason": choice.finish_reason,
        "time_seconds": round(elapsed, 2),
        "prompt_tokens": usage.prompt_tokens if usage else None,
        "completion_tokens": completion_tokens,
        "tokens_per_second": (
            round(completion_tokens / elapsed, 1)
            if completion_tokens and elapsed > 0
            else None
        ),
        "quality_rating": None,
        "rating_note": "",
    }


def main() -> None:
    results = []
    for model in MODELS:
        for prompt_item in PROMPTS:
            print(f"Running {model} - {prompt_item['category']}...")
            results.append(run_benchmark(model, prompt_item))

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:
        json.dump(results, output, indent=2, ensure_ascii=False)

    print(f"Wrote {len(results)} benchmark rows to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
