# Task: Token Distribution Tables (Table 8 & Table 9)

> **SUPERSEDED for long-form schema.** Current authoritative spec for the long-form
> CSV is `token-distribution-tables-multi-model.md`, which adds a `Model` column and
> rolls Mistral-7B, Llama-2-13b, and Llama-2-70b into a single combined CSV.
> The polygraph half of this plan is still current.

## What
Generate two CSVs of per-dataset output-token length statistics (Min, Median, Max):
- **Table 8 — long-form** (Factscore, Longfact, RAGTruth) from `papers/repos/temp-vit/data/raw_data/...`.
- **Table 9 — polygraph** (WMT14FrEn, WMT19DeEn, TriviaQA, MMLU, GSM8k, XSUM) from
  `main_experiments_hf/polygraph_outputs_enriched/...`. CoQA is intentionally excluded.
  XSUM source is missing from `polygraph_outputs_enriched`; row is kept with blank cells.

## Why
Needed for the paper's dataset-stats tables. Both tables describe the **generated**
response length distribution per dataset, used to contextualize per-token / sentence-level
methods downstream.

## Files to Change
- `research-repo-template/scripts/token_distribution.py` — new. Computes both tables and writes CSVs.
- `research-repo-template/.artifacts/token-distribution-long-form/table8_long_form.csv` — output. Now includes per-atom token length columns (`AtomMin`, `AtomMedium`, `AtomMax`).
- `research-repo-template/.artifacts/token-distribution-polygraph/table9_polygraph.csv` — output.

## Key Decisions
- **Metric**: per-example **output (greedy) token count**, aggregated as min / median / max.
  Median is reported in the "Medium" column (user used "Medium" as a synonym for "Median").
  Cast median to int via `round()` to keep all values integer-valued.
- **Long-form source**: `passage_atom_spans_all.jsonl` (`n_resp_tokens` field). Verified
  identical between `_l8` and `_full` layer variants — pick whichever exists.
  - Factscore → `mistralai/Mistral-7B-Instruct-v0.2/factscore_full_l8_all/`
  - Longfact  → `mistralai/Mistral-7B-Instruct-v0.2/longfact_objects_full_l8_all/`
  - RAGTruth  → `mistralai/Mistral-7B-Instruct-v0.1/ragtruth_mistral-7B-instruct_full_all/`
- **Polygraph source**: `ue_manager_seed1` pickles in the most-recent date subdir of each
  bracket-named dataset folder. `torch.load(..., weights_only=False)` then read
  `manager["stats"]["greedy_tokens"]` (list of per-example token-id lists).
- **CoQA**: dropped per user instruction.
- **XSUM**: row preserved, cells blank (no `polygraph_outputs_enriched` artifact exists).
- **Row labels**: kept exactly as user specified (`Factscore`, `Longscore`, `RAGTruth`;
  `WMT14FrEn`, `WMT19DeEn`, `TriviaQA`, `MMLU`, `GSM8k`, `XSUM`). The user wrote
  "Longscore" which is the same dataset as Longfact — keep "Longscore" as the row label.
- **CSV columns**:
  - Table 8: `Dataset,Min,Medium,Max,AtomMin,AtomMedium,AtomMax` — first three are per-response output token length; last three are per-atom token length (`tok_end_in_response - tok_start_in_response`) aggregated across all atoms in the dataset.
  - Table 9: `Dataset,Min,Medium,Max` (atoms are long-form only).
- **Script env**: vanilla python with `torch` is enough; use `/root/miniconda/envs/vllm_polygraph/bin/python` so torch deserialization works against the pickled lm-polygraph manager.

## Validation
- Both CSVs exist at the target paths.
- Long-form table has 3 rows with non-empty integer Min/Med/Max.
- Polygraph table has 6 rows; XSUM row has blank Min/Med/Max; other 5 rows non-empty.
- Spot-check: print n_examples per dataset to stderr while running so we can sanity-check
  that nothing was empty or skipped.
