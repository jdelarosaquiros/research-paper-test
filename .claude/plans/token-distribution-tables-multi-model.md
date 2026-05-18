# Task: Token Distribution Table — multi-model long-form (Mistral-7B, Llama-2-13b, Llama-2-70b)

## What
Extend the long-form token-distribution table (`table8_long_form.csv`) so a single CSV
covers all three generators used in `papers/repos/temp-vit`:

- Mistral-7B-Instruct (v0.2 for fs/lf, v0.1 for rt) — already covered.
- Llama-2-13b-chat-hf — fs, lf, rt — **new**.
- Llama-2-70b-chat-hf — fs, lf, rt — rt sourced from `full_layer_cells/`
  (the `raw_data/.../ragtruth_*` subfolder doesn't exist for 70B; the equivalent
  passage_atom_spans sidecar lives one tree over). Previously covered as a
  separate file; merge into the combined CSV.

Add a `Model` column. Collapse the per-model file
(`table8_long_form_llama2_70b.csv`) into the single combined CSV and delete it.

Source plans (extended by this spec):
- `research-repo-template/.claude/plans/token-distribution-tables.md`
- `research-repo-template/.claude/plans/token-distribution-tables-extend.md`

## Why
Paper needs token-length stats for all three generators in the temp-vit cell grid.
A single CSV with a `Model` column is easier to filter and consume than per-model
files (user choice).

## Files to Change
- `research-repo-template/scripts/token_distribution.py`
  - Refactor `LONG_FORM_SOURCES` / `LONG_FORM_SOURCES_70B` into a single
    `(model_label, dataset_label, path)` list covering all three generators.
  - Combined output: header
    `Dataset,Model,NumSamples,Min,Medium,Max,ClaimMin,ClaimMedium,ClaimMax`.
  - Stop writing `table8_long_form_llama2_70b.csv`; emit a single
    `table8_long_form.csv` only.
  - Polygraph table unchanged.
- `research-repo-template/.artifacts/token-distribution-long-form/table8_long_form.csv`
  — regenerate with new schema; 8 rows total (3 Mistral + 3 Llama-2-13b + 2 Llama-2-70b).
- `research-repo-template/.artifacts/token-distribution-long-form/table8_long_form_llama2_70b.csv`
  — delete (rolled into combined CSV).
- `research-repo-template/.claude/plans/token-distribution-tables.md`,
  `research-repo-template/.claude/plans/token-distribution-tables-extend.md`
  — add a header note pointing at this spec as the current authoritative schema.

## Source paths (under `papers/repos/temp-vit/data/raw_data/`)
- Mistral-7B fs:  `mistralai/Mistral-7B-Instruct-v0.2/factscore_full_l8_all/passage_atom_spans_all.jsonl`
- Mistral-7B lf:  `mistralai/Mistral-7B-Instruct-v0.2/longfact_objects_full_l8_all/passage_atom_spans_all.jsonl`
- Mistral-7B rt:  `mistralai/Mistral-7B-Instruct-v0.1/ragtruth_mistral-7B-instruct_full_all/passage_atom_spans_all_sentence.jsonl`
- Llama-2-13b fs: `meta-llama/Llama-2-13b-chat-hf/factscore_full_l8_all/passage_atom_spans_all.jsonl`
- Llama-2-13b lf: `meta-llama/Llama-2-13b-chat-hf/longfact_objects_full_l8_all/passage_atom_spans_all.jsonl`
- Llama-2-13b rt: `meta-llama/Llama-2-13b-chat-hf/ragtruth_llama-2-13b-chat_full_all/passage_atom_spans_all_sentence.jsonl`
- Llama-2-70b fs: `meta-llama/Llama-2-70b-chat-hf/factscore_full_l8_all/passage_atom_spans_all.jsonl`
- Llama-2-70b lf: `meta-llama/Llama-2-70b-chat-hf/longfact_objects_full_l8_all/passage_atom_spans_all.jsonl`
- Llama-2-70b rt: **uses a different directory pattern** —
  `papers/repos/temp-vit/data/full_layer_cells/ragtruth/meta-llama__Llama-2-70b-chat-hf/passage_atom_spans_all_sentence.jsonl`.
  The `raw_data/meta-llama/Llama-2-70b-chat-hf/ragtruth_*` subfolder does not exist
  for 70B, but the passage_atom_spans sidecar with matching schema lives under
  `full_layer_cells/`. Verified 2026-05-18 (schema parity, ~2958 rows).
  The prior extend spec's claim "no 70B RAGTruth on disk" was incorrect.

## Key Decisions
- **Model labels** in the CSV: `Mistral-7B-Instruct`, `Llama-2-13b-chat`,
  `Llama-2-70b-chat` (drop the HF org prefix; keep variant suffix so v0.1/v0.2
  distinction is implicit via the row's dataset choice for rt).
- **Dataset labels** unchanged: `Factscore`, `Longscore`, `RAGTruth` — kept verbatim
  to stay consistent with the prior CSV the paper already references.
- **RAGTruth source**: use `passage_atom_spans_all_sentence.jsonl` (sentence-level
  spans) for both Mistral and Llama-2-13b — matches the prior spec's note that the
  non-sentence file has token-granularity atoms.
- **Combined CSV row order**: stable by (model, dataset), Mistral first, then
  Llama-2-13b, then Llama-2-70b — matches the paper's model-axis convention.
- **Delete legacy per-model file** rather than keeping in parallel — user picked the
  single combined option.

## Validation
- `head` the combined CSV — header matches `Dataset,Model,NumSamples,Min,Medium,Max,ClaimMin,ClaimMedium,ClaimMax`.
- `wc -l` = 10 (9 data + header).
- Mistral rows must match the pre-existing values exactly:
  - Factscore: 183 / 113 / 280 / 512 / 4 / 33 / 261
  - Longscore: 1140 / 50 / 151 / 513 / 4 / 33 / 512
  - RAGTruth: 2911 / 6 / 157 / 512 / 1 / 22 / 197
- Llama-2-70b rows must match the prior separate CSV exactly:
  - Factscore: 549 / 60 / 512 / 512 / 3 / 34 / 154
  - Longscore: 1140 / 76 / 512 / 512 / 2 / 35 / 426
- Llama-2-13b rows: log `n_resp`, `n_claims` to stderr; sanity-check non-zero and
  in the same order of magnitude as the Mistral counts.
- `table8_long_form_llama2_70b.csv` no longer exists.

## Run command
From workspace root:
```
/root/miniconda/envs/vllm_polygraph/bin/python research-repo-template/scripts/token_distribution.py --long-form-only
```
