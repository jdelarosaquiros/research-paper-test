"""Compute per-dataset output-token length statistics (min / median / max).

Writes two CSVs:
- .artifacts/token-distribution-long-form/table8_long_form.csv
- .artifacts/token-distribution-polygraph/table9_polygraph.csv

See research-repo-template/.claude/plans/token-distribution-tables.md for source decisions.
"""

from __future__ import annotations

import csv
import statistics
import sys
from pathlib import Path

WORKSPACE = Path("/workspace/storage/claude_code_test")
ARTIFACTS = WORKSPACE / "research-repo-template" / ".artifacts"

LONG_FORM_OUT = ARTIFACTS / "token-distribution-long-form" / "table8_long_form.csv"
POLYGRAPH_OUT = ARTIFACTS / "token-distribution-polygraph" / "table9_polygraph.csv"

LONG_FORM_SOURCES: list[tuple[str, Path]] = [
    (
        "Factscore",
        WORKSPACE
        / "papers/repos/temp-vit/data/raw_data/mistralai/Mistral-7B-Instruct-v0.2"
        / "factscore_full_l8_all/passage_atom_spans_all.jsonl",
    ),
    (
        "Longscore",
        WORKSPACE
        / "papers/repos/temp-vit/data/raw_data/mistralai/Mistral-7B-Instruct-v0.2"
        / "longfact_objects_full_l8_all/passage_atom_spans_all.jsonl",
    ),
    (
        "RAGTruth",
        WORKSPACE
        / "papers/repos/temp-vit/data/raw_data/mistralai/Mistral-7B-Instruct-v0.1"
        / "ragtruth_mistral-7B-instruct_full_all/passage_atom_spans_all.jsonl",
    ),
]

POLYGRAPH_ROOT = (
    WORKSPACE / "main_experiments_hf/polygraph_outputs_enriched/polygraph_output_test"
)

POLYGRAPH_SOURCES: list[tuple[str, Path | None]] = [
    (
        "WMT14FrEn",
        POLYGRAPH_ROOT
        / "nmt/mistralai/Mistral-7B-Instruct-v0.2"
        / "['LM-Polygraph/wmt14', 'fren_simple_instruct']",
    ),
    (
        "WMT19DeEn",
        POLYGRAPH_ROOT
        / "nmt/mistralai/Mistral-7B-Instruct-v0.2"
        / "['LM-Polygraph/wmt19', 'deen_simple_instruct']",
    ),
    (
        "TriviaQA",
        POLYGRAPH_ROOT
        / "qa/meta-llama/Llama-3.1-8B-Instruct"
        / "['LM-Polygraph/triviaqa', 'simple_instruct']",
    ),
    (
        "MMLU",
        POLYGRAPH_ROOT
        / "qa/mistralai/Mistral-7B-Instruct-v0.2"
        / "['LM-Polygraph/mmlu', 'simple_instruct']",
    ),
    (
        "GSM8k",
        POLYGRAPH_ROOT
        / "qa/mistralai/Mistral-7B-Instruct-v0.2"
        / "['LM-Polygraph/gsm8k', 'simple_instruct']",
    ),
    # XSUM not present in polygraph_outputs_enriched -> blank row.
    ("XSUM", None),
]


def _read_long_form_tokens(jsonl_path: Path) -> list[int]:
    import json

    tokens: list[int] = []
    with jsonl_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            tokens.append(int(obj["n_resp_tokens"]))
    return tokens


def _latest_manager_under(dataset_dir: Path) -> Path:
    """Find the most-recent ue_manager_seed* file under a dataset folder."""
    candidates = sorted(dataset_dir.rglob("ue_manager_seed*"))
    if not candidates:
        raise FileNotFoundError(f"no ue_manager_seed* under {dataset_dir}")
    # Date subdirs sort lexicographically (YYYY-MM-DD/HH-MM-SS), so the last is newest.
    return candidates[-1]


def _read_polygraph_tokens(dataset_dir: Path) -> list[int]:
    import torch

    manager_path = _latest_manager_under(dataset_dir)
    print(f"  loading {manager_path}", file=sys.stderr)
    manager = torch.load(manager_path, weights_only=False, map_location="cpu")
    stats = manager["stats"] if isinstance(manager, dict) else getattr(manager, "stats")
    greedy = stats["greedy_tokens"]
    return [len(t) for t in greedy]


def _summary(counts: list[int]) -> tuple[int, int, int]:
    return min(counts), round(statistics.median(counts)), max(counts)


def _write_csv(out_path: Path, rows: list[tuple[str, str, str, str]]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Dataset", "Min", "Medium", "Max"])
        w.writerows(rows)
    print(f"wrote {out_path}", file=sys.stderr)


def build_long_form_table() -> None:
    rows: list[tuple[str, str, str, str]] = []
    print("== Table 8 (long-form) ==", file=sys.stderr)
    for name, path in LONG_FORM_SOURCES:
        counts = _read_long_form_tokens(path)
        lo, med, hi = _summary(counts)
        print(f"  {name}: n={len(counts)} min={lo} median={med} max={hi}", file=sys.stderr)
        rows.append((name, str(lo), str(med), str(hi)))
    _write_csv(LONG_FORM_OUT, rows)


def build_polygraph_table() -> None:
    rows: list[tuple[str, str, str, str]] = []
    print("== Table 9 (polygraph) ==", file=sys.stderr)
    for name, dataset_dir in POLYGRAPH_SOURCES:
        if dataset_dir is None:
            print(f"  {name}: source missing -> blank row", file=sys.stderr)
            rows.append((name, "", "", ""))
            continue
        counts = _read_polygraph_tokens(dataset_dir)
        lo, med, hi = _summary(counts)
        print(f"  {name}: n={len(counts)} min={lo} median={med} max={hi}", file=sys.stderr)
        rows.append((name, str(lo), str(med), str(hi)))
    _write_csv(POLYGRAPH_OUT, rows)


def main() -> None:
    build_long_form_table()
    build_polygraph_table()


if __name__ == "__main__":
    main()
