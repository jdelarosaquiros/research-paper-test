# Task: Table 3 — switch reported metric from AUROC to PRR

## What
Refill every numeric cell in Table 3 (LM-Polygraph short-form, file
`paper/figs/tab2_ood.tex`, label `tab:polygraph`, **rendered as Table 3**) with
the PRR (Prediction Rejection Ratio) value from `.artifacts/polygraph-benchmark/`,
update the caption, and fix the one prose passage that still calls the metric
AUROC. For the two trained rows (Temp-ViT, Encoder Only) use the **PRR-trained
variant** in the CSV when available; otherwise fall back to whatever Temp-ViT/
Encoder-Only variant currently sources the cell. Row names stay "Temp-ViT" and
"Encoder Only" — no `(PRR)` suffix.

## Why
`05_experiments.tex` already declares "the Prediction Rejection Ratio for
Table~\ref{tab:polygraph}" as the evaluation metric, but the table cells, the
caption ("AUROC per dataset across QA and NMT corpora"), and the
`07_polygraph_efficiency.tex` discussion ("per-dataset AUROC on three cells")
all still report AUROC. Harmonise to PRR across the table, caption, and prose.

## Source data
- `.artifacts/polygraph-benchmark/mmlu_simple_instruct_mistral7b_v2.csv` —
  Mistral-7B-v0.2 × MMLU
- `.artifacts/polygraph-benchmark/gsm8k_simple_instruct_mistral7b_v2.csv` —
  Mistral-7B-v0.2 × GSM8k
- `.artifacts/polygraph-benchmark/wmt19deen_mistral7b_v2.csv` —
  Mistral-7B-v0.2 × WMT19 De→En
- Schema: `estimator,auroc,prr,ece,brier,n_examples,gen_metric`

No CSVs exist for TriviaQA, CoQA, or WMT14, and no CSVs exist for Llama-2-13b
or Llama-2-70b — those cells stay `---` (unchanged from the current table).

## Trained-row variant selection (per user instruction)
- **Encoder Only** = Stage-2 detector. PRR-trained variant
  `EncoderOnly_PRR_Stage2` is present in MMLU and WMT19; absent in GSM8k →
  cell stays `---` (no fallback — current table cell is already `---`).
- **Temp-ViT** = Stage-3 full pipeline. PRR-trained variant
  `TempViT_PRR_Stage3` is present in MMLU and WMT19; absent in GSM8k →
  fall back to `TempViT_Stage3` (the AUROC-trained variant) and report **its
  PRR column value**, so the row is fully populated.
- **Act-ViT (F-v2, N_eff=6)** maps to `ActViT_Foundation_Neff6`.

## Files to Change
- `paper/figs/tab2_ood.tex` — replace numeric values for Mistral × MMLU,
  Mistral × GSM8k, Mistral × WMT19 cells; update bold/underline per column;
  rewrite caption to say PRR, update gen-metric description.
- `paper/sections/07_polygraph_efficiency.tex` — replace "per-dataset AUROC"
  with "per-dataset PRR" (line 12). Update the two literal numbers in the
  Encoder-Only commentary (lines 20–21): `0.790` → `0.816`, `0.006` → `0.001`.

Not touched:
- `paper/sections/05_experiments.tex` — already declares PRR for `tab:polygraph`.
- `paper/sections/00_abstract.tex` — abstract mentions "short-form tasks"
  without naming a metric.
- `paper/sections/08_conclusions.tex` — "sentence-level AUROC" refers to
  Table 2 (`tab:sentence`), not Table 3.
- `paper/sections/09_ablations.tex` — AUROC/PRR mentions refer to stage and
  long-form tables, not Table 3.

## Cell values (3 decimals, all from the `prr` column)

### Mistral-7B-Instruct (Mis-7B-Inst) — MMLU / GSM8k / WMT19
| Method | MMLU | GSM8k | WMT19 |
|---|---|---|---|
| MaximumSequenceProbability     | 0.065 | 0.499 | 0.806 |
| Perplexity                     | 0.065 | 0.486 | 0.806 |
| MeanTokenEntropy               | 0.065 | 0.488 | 0.810 |
| SelfCertainty                  | 0.072 | 0.472 | \underline{0.816} |
| TokenSAR                       | 0.082 | 0.486 | 0.805 |
| MeanPointwiseMutualInformation | 0.113 | 0.401 | 0.791 |
| BoostedProbSequence            | 0.073 | 0.488 | 0.812 |
| CSL                            | 0.062 | 0.485 | 0.805 |
| AttentionScore                 | 0.084 | 0.410 | 0.788 |
| RAUQ                           | 0.072 | 0.488 | 0.805 |
| Act-ViT (F-v2, N_eff=6)        | \underline{0.113} | \textbf{0.539} | 0.815 |
| Encoder Only                   | \textbf{0.114} | --- | \textbf{0.816} |
| Temp-ViT                       | 0.111 | \underline{0.530} | 0.813 |

(GSM8k Encoder-Only stays `---` because the CSV has no EncoderOnly row.)

(For SelfCertainty=0.8160 vs Act-ViT=0.8150 vs Encoder Only=0.8162 on WMT19,
all round to 0.816 / 0.815 / 0.816 at 3 decimals — Encoder Only wins by
0.0002 pre-rounding, so it gets the bold; SelfCertainty is true second.)

FactProbe, Feature-Gaps, HaMI: all `---` (unchanged).
Llama-2-13B and Llama-2-70B row banks: all `---` (unchanged).

## Caption rewrite
Old: "AUROC per dataset across QA and NMT corpora; COMET (NMT) and AlignScore
(long-form QA) quality scores are binarised at the training-set median."

New: "PRR per dataset across QA and NMT corpora; for AUROC computation,
binary correctness labels use accuracy for QA (MMLU, GSM8k) and COMET
binarised at the training-set median for NMT (WMT19). PRR is computed against
the continuous-quality target (binary accuracy for QA, raw COMET for NMT) per
Section~\ref{sec:baselines}."

(The AlignScore mention is removed because there is no long-form column in
Table 3; it must have been a leftover from a prior version.)

## Prose updates in `07_polygraph_efficiency.tex`
- Line 12: `per-dataset AUROC` → `per-dataset PRR`.
- Line 20: `Encoder Only wins WMT19 ($0.790$)` → `Encoder Only wins WMT19 ($0.816$)`.
- Line 21: `lands within $0.006$ of the Act-ViT mechanistic baseline on MMLU` →
  `slightly edges the Act-ViT mechanistic baseline on MMLU ($0.114$ vs $0.113$)`.
  (Pre-change, Encoder Only was 0.911 vs Act-ViT 0.917 = 0.006 below; post-
  change, Encoder Only 0.1140 vs Act-ViT 0.1134 = above by 0.0006, so the
  qualitative comparison flips. Phrasing updated to match.)

The "Temp-ViT row loses some accuracy on the short-form QA cells" sentence
still holds qualitatively under PRR (Temp-ViT lags Act-ViT/Encoder Only by
0.003–0.009 PRR across the three cells), so it stays.

## Key Decisions
- **Three-decimal precision**: matches the rest of the table.
- **Bold/underline per column**, same convention as before.
- **No name change** for Temp-ViT / Encoder Only — per explicit user
  instruction, even though the cells now come from the PRR-trained variant.
- **GSM8k Temp-ViT fallback**: use `TempViT_Stage3` row, report its PRR. The
  user said "if available" for the PRR variant, so falling back to the
  AUROC-trained variant is in scope. Encoder Only stays `---` because no
  EncoderOnly variant exists in the GSM8k CSV at all.
- **Don't change** the abstract / conclusion / ablation files — their AUROC
  mentions reference other tables.

## Validation
- `cd paper && PATH=/usr/local/texlive/2024/bin/x86_64-linux:$PATH latexmk -pdf main.tex`
  builds cleanly.
- `pdftotext -layout main.pdf - | sed -n '/Table 3/,/Table 4/p'` shows PRR in
  the caption and 3-decimal values matching the table above.
- `grep -n "AUROC" paper/sections/07_polygraph_efficiency.tex` shows no AUROC
  mention in the Table-3 paragraph (lines 7–30).
- `grep -nE "0\.790|0\.911|0\.917" paper/sections/07_polygraph_efficiency.tex`
  returns no matches (old AUROC values purged).
