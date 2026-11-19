uv run python compare.py
| Metric | n | Local mean +/- 2xSE | Cloud mean +/- 2xSE | Paired difference +/- 2xSE | Verdict |
|---|---:|---:|---:|---:|---|
| Contextual Relevancy | 18 | 0.284 +/- 0.100 | 0.305 +/- 0.106 | 0.021 +/- 0.056 | no clear difference |
| Contextual Recall | 18 | 0.806 +/- 0.183 | 0.806 +/- 0.183 | 0.000 +/- 0.000 | no clear difference |
| Contextual Precision | 18 | 0.699 +/- 0.130 | 0.725 +/- 0.150 | 0.026 +/- 0.094 | no clear difference |
| Faithfulness | 18 | 0.786 +/- 0.094 | 0.838 +/- 0.157 | 0.052 +/- 0.163 | no clear difference |
| Answer Relevancy | 18 | 0.950 +/- 0.059 | 1.000 +/- 0.000 | 0.050 +/- 0.059 | no clear difference |

**Local:** median generation time 18586.22 ms; slowest 300116.29 ms; average completion tokens 146.50; empty or failed answers 0.
**Cloud:** median generation time 1027.62 ms; slowest 2199.11 ms; average completion tokens 62.39; empty or failed answers 0.