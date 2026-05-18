"""Aggregate per-dataset LM-Polygraph estimator scores into per-category means.

Reads `{wmt19deen,mmlu,gsm8k}_simple_instruct_mistral7b_v2.csv` (schema:
`estimator,auroc,prr,ece,brier,n_examples,gen_metric`) and emits two
aggregate CSVs keyed by `(method, llm, category)`:

- `prr_by_category.csv`  — per-category mean of the `prr` column.
- `ece_by_category.csv`  — per-category mean of the `ece` column.

Categories follow the paper's grouping:
    QA  ← TriviaQA, CoQA, MMLU
    CoT ← GSM8k
    NMT ← WMT14, WMT19

Aggregation is the arithmetic mean over the datasets *present* in each
category (skip-NaN). This means today's Mis-7B-Inst aggregates equal the
single per-dataset value in each category, but the script is correct when
more datasets are filled in later.

Stdlib only. Run from this directory:

    python3 aggregate_by_category.py
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path
from statistics import mean

HERE = Path(__file__).resolve().parent

# (csv basename, dataset_label, category, llm).
# When TriviaQA / CoQA / WMT14 CSVs land, append rows here and re-run.
DATASETS: list[tuple[str, str, str, str]] = [
    ("mmlu_simple_instruct_mistral7b_v2.csv",       "MMLU",   "QA",  "Mistral-7B-Instruct"),
    ("gsm8k_simple_instruct_mistral7b_v2.csv",      "GSM8k",  "CoT", "Mistral-7B-Instruct"),
    ("wmt19deen_mistral7b_v2.csv",                  "WMT19",  "NMT", "Mistral-7B-Instruct"),
]

CATEGORIES = ["QA", "CoT", "NMT"]


def _load_csv(path: Path) -> dict[str, dict[str, float]]:
    """Return {estimator: {"prr": float, "ece": float}}."""
    out: dict[str, dict[str, float]] = {}
    with path.open() as f:
        for row in csv.DictReader(f):
            out[row["estimator"]] = {
                "prr": float(row["prr"]),
                "ece": float(row["ece"]),
            }
    return out


def _aggregate(metric: str) -> dict[tuple[str, str, str], tuple[float, int]]:
    """For each (method, llm, category), return (mean(metric), n_datasets)."""
    # buckets[(method, llm, category)] = [values from each dataset present]
    buckets: dict[tuple[str, str, str], list[float]] = {}
    for fname, _dataset_label, category, llm in DATASETS:
        path = HERE / fname
        if not path.exists():
            print(f"  skip missing source: {path.name}", file=sys.stderr)
            continue
        data = _load_csv(path)
        for method, vals in data.items():
            buckets.setdefault((method, llm, category), []).append(vals[metric])

    return {key: (mean(vs), len(vs)) for key, vs in buckets.items()}


def _write_wide(
    out_path: Path,
    metric: str,
    agg: dict[tuple[str, str, str], tuple[float, int]],
) -> None:
    """Wide-form CSV: one row per (method, llm), one column-pair per category."""
    # Collect all (method, llm) pairs that appear in any category.
    method_llm: set[tuple[str, str]] = {(m, l) for (m, l, _c) in agg}

    header = ["method", "llm"]
    for cat in CATEGORIES:
        header += [f"{cat.lower()}_{metric}", f"{cat.lower()}_n"]

    rows: list[list[str]] = []
    for method, llm in sorted(method_llm):
        row: list[str] = [method, llm]
        for cat in CATEGORIES:
            entry = agg.get((method, llm, cat))
            if entry is None:
                row += ["", "0"]
            else:
                val, n = entry
                row += [f"{val:.4f}", str(n)]
        rows.append(row)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {out_path.name}  ({len(rows)} rows)", file=sys.stderr)


def _print_summary(metric: str, agg: dict[tuple[str, str, str], tuple[float, int]]) -> None:
    """Print the row a human is likely to spot-check against the latex table."""
    print(f"\n== {metric.upper()} per-category means (3 decimals) ==", file=sys.stderr)
    print(f"  {'method':<40s}{'llm':<22s}{'QA':>10s}{'CoT':>10s}{'NMT':>10s}", file=sys.stderr)
    methods = sorted({m for (m, _l, _c) in agg})
    llms = sorted({l for (_m, l, _c) in agg})
    for llm in llms:
        for method in methods:
            cells = []
            for cat in CATEGORIES:
                entry = agg.get((method, llm, cat))
                cells.append(f"{entry[0]:.3f}" if entry else "---")
            if any(c != "---" for c in cells):
                print(f"  {method:<40s}{llm:<22s}{cells[0]:>10s}{cells[1]:>10s}{cells[2]:>10s}", file=sys.stderr)


def main() -> None:
    prr = _aggregate("prr")
    ece = _aggregate("ece")
    _write_wide(HERE / "prr_by_category.csv", "prr", prr)
    _write_wide(HERE / "ece_by_category.csv", "ece", ece)
    _print_summary("prr", prr)
    _print_summary("ece", ece)


if __name__ == "__main__":
    main()
