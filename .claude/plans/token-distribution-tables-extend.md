# Task: Token Distribution Tables — extend with NumSamples, claim rename, and Llama-2-70B

> **SUPERSEDED.** Current authoritative spec is
> `token-distribution-tables-multi-model.md`. The per-model
> `table8_long_form_llama2_70b.csv` introduced here has been collapsed into a single
> combined `table8_long_form.csv` with a `Model` column.

## What
Extend the existing token-distribution CSVs (Table 8 long-form, Table 9 polygraph):
- Add a `NumSamples` column (count of passages / generations) to both.
- Rename `AtomMin/AtomMedium/AtomMax` → `ClaimMin/ClaimMedium/ClaimMax` in Table 8 (long-form only — polygraph has no claim concept).
- Add a parallel long-form table for **Llama-2-70B-chat** at
  `table8_long_form_llama2_70b.csv` (FactScore + LongFact rows; RAGTruth row absent — no 70B RAGTruth data on disk).

Source plan: `research-repo-template/.claude/plans/token-distribution-tables.md`
(found in Phase 1; this spec extends it).

## Why
Paper Table 8 (`paper/figs/tab8_long_form_dataset_stats.tex`) needs the claim-length
columns populated and the sample count visible. The Llama-2-70B columns are needed
for the parallel 70B paper experiments — same dataset, different generator.

## Files to Change
- `research-repo-template/scripts/token_distribution.py` — add a `--model` switch
  (or extend `LONG_FORM_SOURCES` to include Llama-2-70B paths), rename the Atom*
  CSV header to Claim*, and add `NumSamples`. Polygraph: just add `NumSamples`.
- `research-repo-template/.artifacts/token-distribution-long-form/table8_long_form.csv`
  — regenerate with new schema `Dataset,NumSamples,Min,Medium,Max,ClaimMin,ClaimMedium,ClaimMax`.
- `research-repo-template/.artifacts/token-distribution-long-form/table8_long_form_llama2_70b.csv`
  — new file, same schema. FactScore + LongFact rows (no RAGTruth on disk for 70B).
- `research-repo-template/.artifacts/token-distribution-polygraph/table9_polygraph.csv`
  — regenerate with new schema `Dataset,NumSamples,Min,Medium,Max`.

## Key Decisions
- **NumSamples for long-form** = number of JSONL lines (one per passage / generation).
- **NumSamples for polygraph** = `len(stats["greedy_tokens"])` — same denominator the
  Min/Med/Max are computed over. Blank row for XSUM (no source).
- **Atom → Claim rename in CSV header only.** Data-side field names (`atoms`,
  `tok_start_in_response`, `tok_end_in_response`) stay as-is — only the CSV column
  labels change, matching the paper's `atom→claim` terminology rename
  (`.claude/plans/atom-to-claim-rename.md`).
- **Llama-2-70B sources** (under `papers/repos/temp-vit/data/raw_data/meta-llama/Llama-2-70b-chat-hf/`):
  - FactScore: `factscore_full_l8_all/passage_atom_spans_all.jsonl` — confirmed schema parity
    with Mistral (extra `j` key, ignored).
  - LongFact: `longfact_objects_full_l8_all/passage_atom_spans_all.jsonl` — same.
  - RAGTruth: not present for 70B → row omitted from `table8_long_form_llama2_70b.csv`
    (do not emit a blank row; signal absence by absence).
- **Output file format**: separate CSV per model (per user choice). One CSV per
  generator model, all three datasets per file when available.
- **Run env**: same `/root/miniconda/envs/vllm_polygraph/bin/python` for torch
  deserialization; long-form path is plain stdlib so any python works for that half.

## Files / commands the implementer can copy
Run from workspace root:
```
/root/miniconda/envs/vllm_polygraph/bin/python research-repo-template/scripts/token_distribution.py
```
Should produce:
- `.artifacts/token-distribution-long-form/table8_long_form.csv` (Mistral)
- `.artifacts/token-distribution-long-form/table8_long_form_llama2_70b.csv` (Llama-2-70B)
- `.artifacts/token-distribution-polygraph/table9_polygraph.csv`

## Validation
- `head` each CSV — confirm header line matches the new schema exactly.
- `wc -l` each — long-form Mistral=4 (3 data + header), long-form Llama-2-70B=3
  (2 data + header), polygraph=7 (6 data + header, XSUM blank).
- Spot-check Mistral FactScore row vs. previous run: Min/Medium/Max for passage
  length should be unchanged (113 / 280 / 512); Claim* should match the previous
  AtomMin/AtomMedium/AtomMax (4 / 33 / 261); only NumSamples is new.
- For 70B, log `n_resp`, `n_atoms` to stderr and sanity-check they're > 0 and on
  the order of the Mistral counts (FactScore: typically several hundred passages).
