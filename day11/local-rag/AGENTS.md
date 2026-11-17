# Local RAG Project Agent Instructions

## Running scripts

- Run Python scripts with `uv run python <script>.py` from this directory.
- Verify Ollama first with `curl.exe http://localhost:11434/api/version`.
- Run the Exercise 1 benchmark with `uv run python benchmark.py`.
- Run `ollama ps` and stop extra loaded models with `ollama stop <model>` before benchmarking.

## Project rules

- Keep the pipeline local: use Ollama models with no `cloud` tags.
- Use only models that are available locally for generation.
- Every reported benchmark number must come from `benchmark_results.json`.
- Never invent, estimate, or fabricate benchmark measurements or results.
- Re-running `benchmark.py` overwrites `benchmark_results.json`; add human quality ratings only after the final run.
- Explain every line of code created or changed so the student can understand it.
- Complete one project stage at a time and check it before proceeding.
- Commit AGENTS.md before AI-assisted implementation.
- Keep the remaining project changes separate until the capstone is complete.
