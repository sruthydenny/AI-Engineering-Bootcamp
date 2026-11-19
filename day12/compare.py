import json
import math
from pathlib import Path
from statistics import median, stdev


METRICS = [
    "Contextual Relevancy",
    "Contextual Recall",
    "Contextual Precision",
    "Faithfulness",
    "Answer Relevancy",
]


def load(name):
    with (BASE / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def interval(values):
    n = len(values)
    if not n:
        return None
    mean = sum(values) / n
    se = stdev(values) / math.sqrt(n) if n > 1 else 0.0
    return mean, 2 * se


def fmt_interval(values):
    result = interval(values)
    if result is None:
        return "n/a"
    mean, half_width = result
    return f"{mean:.3f} +/- {half_width:.3f}"


BASE = Path(__file__).parent
local_eval = load("eval_results_local.json")
cloud_eval = load("eval_results_cloud.json")
local_outputs = load("pipeline_outputs_local.json")
cloud_outputs = load("pipeline_outputs_cloud.json")

local_by_id = {row["id"]: row for row in local_eval}
cloud_by_id = {row["id"]: row for row in cloud_eval}

print("| Metric | n | Local mean +/- 2xSE | Cloud mean +/- 2xSE | Paired difference +/- 2xSE | Verdict |")
print("|---|---:|---:|---:|---:|---|")
for metric in METRICS:
    local_values = []
    cloud_values = []
    differences = []
    for question_id in sorted(set(local_by_id) & set(cloud_by_id)):
        local_metric = local_by_id[question_id]["metrics"].get(metric)
        cloud_metric = cloud_by_id[question_id]["metrics"].get(metric)
        if not local_metric or not cloud_metric:
            continue
        local_score = local_metric["score"]
        cloud_score = cloud_metric["score"]
        if local_score is None or cloud_score is None or local_metric["error"] or cloud_metric["error"]:
            continue
        local_values.append(local_score)
        cloud_values.append(cloud_score)
        differences.append(cloud_score - local_score)

    n = len(differences)
    diff_result = interval(differences)
    if diff_result is None:
        verdict = "no clear difference"
    else:
        diff_mean, diff_half_width = diff_result
        if diff_mean - diff_half_width <= 0 <= diff_mean + diff_half_width:
            verdict = "no clear difference"
        elif diff_mean > 0:
            verdict = "cloud higher"
        else:
            verdict = "local higher"

    print(
        f"| {metric} | {n} | {fmt_interval(local_values)} | "
        f"{fmt_interval(cloud_values)} | {fmt_interval(differences)} | {verdict} |"
    )


def run_summary(label, outputs):
    times = [
        row["generation_time_ms"]
        for row in outputs
        if isinstance(row.get("generation_time_ms"), (int, float))
    ]
    completion_tokens = [
        row["tokens_generated"]
        for row in outputs
        if isinstance(row.get("tokens_generated"), (int, float))
    ]
    empty_or_failed = sum(
        not str(row.get("actual_answer") or "").strip()
        or row.get("finish_reason") not in (None, "stop")
        for row in outputs
    )
    return {
        "median_generation_ms": median(times) if times else None,
        "slowest_generation_ms": max(times) if times else None,
        "average_completion_tokens": (
            sum(completion_tokens) / len(completion_tokens)
            if completion_tokens else None
        ),
        "empty_or_failed_answers": empty_or_failed,
    }


print()
for label, outputs in (
    ("Local", local_outputs),
    ("Cloud", cloud_outputs),
):
    summary = run_summary(label, outputs)
    print(
        f"**{label}:** median generation time "
        f"{summary['median_generation_ms']:.2f} ms; slowest "
        f"{summary['slowest_generation_ms']:.2f} ms; average completion tokens "
        f"{summary['average_completion_tokens']:.2f}; empty or failed answers "
        f"{summary['empty_or_failed_answers']}."
    )
