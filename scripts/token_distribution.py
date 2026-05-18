"""Compute per-dataset output-token length statistics (min / median / max).

Writes two CSVs:
- .artifacts/token-distribution-long-form/table8_long_form.csv  (all generators, Model column)
- .artifacts/token-distribution-polygraph/table9_polygraph.csv

See research-repo-template/.claude/plans/token-distribution-tables-multi-model.md
(current schema). Prior plans (token-distribution-tables.md,
token-distribution-tables-extend.md) are superseded for the long-form half.
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

RAW_ROOT = WORKSPACE / "papers/repos/temp-vit/data/raw_data"

# (model_label, dataset_label, jsonl_path). Order = paper's model-axis order.
# RAGTruth uses the sentence sidecar (atoms = claim spans); the non-sentence file
# has token-granularity spans.
LONG_FORM_SOURCES: list[tuple[str, str, Path]] = [
    (
        "Mistral-7B-Instruct",
        "Factscore",
        RAW_ROOT
        / "mistralai/Mistral-7B-Instruct-v0.2/factscore_full_l8_all/passage_atom_spans_all.jsonl",
    ),
    (
        "Mistral-7B-Instruct",
        "Longscore",
        RAW_ROOT
        / "mistralai/Mistral-7B-Instruct-v0.2/longfact_objects_full_l8_all/passage_atom_spans_all.jsonl",
    ),
    (
        "Mistral-7B-Instruct",
        "RAGTruth",
        RAW_ROOT
        / "mistralai/Mistral-7B-Instruct-v0.1/ragtruth_mistral-7B-instruct_full_all/passage_atom_spans_all_sentence.jsonl",
    ),
    (
        "Llama-2-13b-chat",
        "Factscore",
        RAW_ROOT
        / "meta-llama/Llama-2-13b-chat-hf/factscore_full_l8_all/passage_atom_spans_all.jsonl",
    ),
    (
        "Llama-2-13b-chat",
        "Longscore",
        RAW_ROOT
        / "meta-llama/Llama-2-13b-chat-hf/longfact_objects_full_l8_all/passage_atom_spans_all.jsonl",
    ),
    (
        "Llama-2-13b-chat",
        "RAGTruth",
        RAW_ROOT
        / "meta-llama/Llama-2-13b-chat-hf/ragtruth_llama-2-13b-chat_full_all/passage_atom_spans_all_sentence.jsonl",
    ),
    (
        "Llama-2-70b-chat",
        "Factscore",
        RAW_ROOT
        / "meta-llama/Llama-2-70b-chat-hf/factscore_full_l8_all/passage_atom_spans_all.jsonl",
    ),
    (
        "Llama-2-70b-chat",
        "Longscore",
        RAW_ROOT
        / "meta-llama/Llama-2-70b-chat-hf/longfact_objects_full_l8_all/passage_atom_spans_all.jsonl",
    ),
    (
        # 70B RAGTruth has no `raw_data/.../ragtruth_*` subfolder; the equivalent
        # passage_atom_spans sidecar lives under data/full_layer_cells/ instead.
        # Schema parity with the raw_data sentence sidecars (verified 2026-05-18).
        "Llama-2-70b-chat",
        "RAGTruth",
        WORKSPACE
        / "papers/repos/temp-vit/data/full_layer_cells/ragtruth"
        / "meta-llama__Llama-2-70b-chat-hf/passage_atom_spans_all_sentence.jsonl",
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
    header = [
        "Dataset",
        "Model",
        "NumSamples",
        "Min",
        "Medium",
        "Max",
        "ClaimMin",
        "ClaimMedium",
        "ClaimMax",
    ]
    rows: list[list[str]] = []
    print("== Table 8 (long-form, all models) ==", file=sys.stderr)
    for model, dataset, path in LONG_FORM_SOURCES:
        resp_tokens, atom_lens = _read_long_form_jsonl(path)
        lo, med, hi = _summary(resp_tokens)
        c_lo, c_med, c_hi = _summary(atom_lens)
        n_samples = len(resp_tokens)
        print(
            f"  {model} / {dataset}: n_samples={n_samples}"
            f" passage_min={lo} passage_med={med} passage_max={hi}"
            f" | n_claims={len(atom_lens)}"
            f" claim_min={c_lo} claim_med={c_med} claim_max={c_hi}",
            file=sys.stderr,
        )
        rows.append(
            [
                dataset,
                model,
                str(n_samples),
                str(lo),
                str(med),
                str(hi),
                str(c_lo),
                str(c_med),
                str(c_hi),
            ]
        )
    _write_csv(LONG_FORM_OUT, header, rows)


def build_polygraph_table() -> None:
    rows: list[list[str]] = []
    print("== Table 9 (polygraph) ==", file=sys.stderr)
    for name, dataset_dir in POLYGRAPH_SOURCES:
        if dataset_dir is None:
            print(f"  {name}: source missing -> blank row", file=sys.stderr)
            rows.append([name, "", "", "", ""])
            continue
        counts = _read_polygraph_tokens(dataset_dir)
        lo, med, hi = _summary(counts)
        n = len(counts)
        print(f"  {name}: n_samples={n} min={lo} median={med} max={hi}", file=sys.stderr)
        rows.append([name, str(n), str(lo), str(med), str(hi)])
    _write_csv(
        POLYGRAPH_OUT,
        ["Dataset", "NumSamples", "Min", "Medium", "Max"],
        rows,
    )


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
