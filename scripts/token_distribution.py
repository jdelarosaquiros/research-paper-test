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


def _read_long_form_jsonl(jsonl_path: Path) -> tuple[list[int], list[int]]:
    """Return (resp_token_counts_per_example, atom_token_lengths_across_all_atoms)."""
    import json

    resp_tokens: list[int] = []
    atom_lens: list[int] = []
    with jsonl_path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            resp_tokens.append(int(obj["n_resp_tokens"]))
            # tok_end_in_response is end-INCLUSIVE: passage_dataset.py clamps hi
            # to T_resp-1 and treats hi==lo as a valid 1-token atom.
            for atom in obj.get("atoms", []):
                atom_lens.append(
                    int(atom["tok_end_in_response"])
                    - int(atom["tok_start_in_response"])
                    + 1
                )
    return resp_tokens, atom_lens


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


def _write_csv(out_path: Path, header: list[str], rows: list[list[str]]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {out_path}", file=sys.stderr)


def build_long_form_table() -> None:
    rows: list[list[str]] = []
    print("== Table 8 (long-form) ==", file=sys.stderr)
    for name, path in LONG_FORM_SOURCES:
        resp_tokens, atom_lens = _read_long_form_jsonl(path)
        lo, med, hi = _summary(resp_tokens)
        a_lo, a_med, a_hi = _summary(atom_lens)
        print(
            f"  {name}: n_resp={len(resp_tokens)} resp_min={lo} resp_med={med} resp_max={hi}"
            f" | n_atoms={len(atom_lens)} atom_min={a_lo} atom_med={a_med} atom_max={a_hi}",
            file=sys.stderr,
        )
        rows.append(
            [name, str(lo), str(med), str(hi), str(a_lo), str(a_med), str(a_hi)]
        )
    _write_csv(
        LONG_FORM_OUT,
        ["Dataset", "Min", "Medium", "Max", "AtomMin", "AtomMedium", "AtomMax"],
        rows,
    )


def build_polygraph_table() -> None:
    rows: list[list[str]] = []
    print("== Table 9 (polygraph) ==", file=sys.stderr)
    for name, dataset_dir in POLYGRAPH_SOURCES:
        if dataset_dir is None:
            print(f"  {name}: source missing -> blank row", file=sys.stderr)
            rows.append([name, "", "", ""])
            continue
        counts = _read_polygraph_tokens(dataset_dir)
        lo, med, hi = _summary(counts)
        print(f"  {name}: n={len(counts)} min={lo} median={med} max={hi}", file=sys.stderr)
        rows.append([name, str(lo), str(med), str(hi)])
    _write_csv(POLYGRAPH_OUT, ["Dataset", "Min", "Medium", "Max"], rows)


def main(argv: list[str] | None = None) -> None:
    argv = sys.argv[1:] if argv is None else argv
    do_long = "--polygraph-only" not in argv
    do_polygraph = "--long-form-only" not in argv
    if do_long:
        build_long_form_table()
    if do_polygraph:
        build_polygraph_table()


if __name__ == "__main__":
    main()
