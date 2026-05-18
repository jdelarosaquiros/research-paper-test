# Task: Add an ECE-calibration ablation table mirroring Table 3 (PRR)

## What
Add a new ablation table — `paper/figs/tab12_polygraph_ece.tex` — that mirrors
Table 3 (`tab2_ood.tex`, label `tab:polygraph`, LM-Polygraph short-form) but
reports **ECE (Expected Calibration Error)** instead of PRR. Add a short
ablation paragraph in `paper/sections/09_ablations.tex` that points at the
new table and notes the lower-is-better convention. Wire the new table into
the input block at the bottom of `09_ablations.tex`.

## Why
Table 3 measures ranking quality (PRR). A calibration view is missing — ECE
captures whether the confidence scores are *calibrated* (mean predicted
probability matches empirical frequency), independent of ranking. The two
metrics commonly disagree: a baseline can rank well (high PRR) and still be
miscalibrated (high ECE) or vice versa. The LM-Polygraph benchmark CSVs
already contain a per-method `ece` column, so the table can be filled
directly from the same data source as Table 3.

## Source data
- `.artifacts/polygraph-benchmark/{mmlu,gsm8k,wmt19deen}_simple_instruct_mistral7b_v2.csv`
- Schema: `estimator,auroc,prr,ece,brier,n_examples,gen_metric`.
- ECE definition (per README): "15-bin expected calibration error of
  `p_high_quality = 1 - minmax(scores)` against
  `y_high_quality = 1 - y_binary`. Lower = better."
- Same variant-selection rule as the PRR table:
  - **Encoder Only** → `EncoderOnly_PRR_Stage2` if present, else `---`.
  - **Temp-ViT** → `TempViT_PRR_Stage3` if present, else fall back to
    `TempViT_Stage3` (its ECE column) so the row is fully populated.
  - **Act-ViT (F-v2, N_eff=6)** → `ActViT_Foundation_Neff6`.
  - GSM8k has no `EncoderOnly_PRR_*` row → that cell stays `---`.

## Files to Change
- `paper/figs/tab12_polygraph_ece.tex` — **new file**. Structurally identical
  to `tab2_ood.tex` (same row labels, same Hybrid/Mechanistic/Ours bands,
  same `---` placeholder convention for unfilled cells), with ECE values
  from the `ece` column. Caption explicitly says ECE and "lower is better".
- `paper/sections/09_ablations.tex` — add a new
  `\paragraph{Calibration on LM-Polygraph (Table~\ref{tab:polygraph_ece}).}`
  paragraph between the In-distribution-vs-OOD paragraph and the
  Token-level-overlap paragraph (it sits naturally with the per-table
  ablation block), plus `\input{figs/tab12_polygraph_ece}` in the input
  list at the bottom.

## Cell values (3 decimals, all from the `ece` column; lower = better)

### Mistral-7B-Instruct (Mis-7B-Inst) — MMLU / GSM8k / WMT19
| Method | MMLU | GSM8k | WMT19 |
|---|---|---|---|
| MaximumSequenceProbability     | 0.910 | 0.355 | 0.190 |
| Perplexity                     | 0.910 | 0.258 | 0.095 |
| MeanTokenEntropy               | 0.834 | 0.301 | \underline{0.090} |
| SelfCertainty                  | 0.530 | 0.142 | 0.177 |
| TokenSAR                       | 0.858 | 0.257 | \textbf{0.081} |
| MeanPointwiseMutualInformation | \underline{0.225} | 0.149 | 0.328 |
| BoostedProbSequence            | 0.912 | 0.457 | 0.200 |
| CSL                            | 0.908 | 0.414 | 0.162 |
| AttentionScore                 | 0.344 | 0.145 | 0.304 |
| RAUQ                           | 0.743 | 0.144 | 0.325 |
| Act-ViT (F-v2, N_eff=6)        | \textbf{0.061} | \underline{0.111} | 0.170 |
| Encoder Only                   | 0.064 | --- | 0.154 |
| Temp-ViT                       | 0.448 | \textbf{0.066} | 0.178 |

(Llama-2-13B and Llama-2-70B row banks: all `---`, same as Table 3.)
(FactProbe, Feature-Gaps, HaMI: all `---`, same as Table 3.)

### Bolding rule reminder
**ECE is lower-is-better**, so `\textbf{}` marks the *minimum* and
`\underline{}` the second-minimum per column. The PRR table used the
opposite convention (higher-is-better) — the caption must call this out.

## Caption (new file)
> **LM-Polygraph calibration ablation.** Expected Calibration Error (ECE,
> 15 bins, lower is better) per dataset across QA and NMT corpora on
> Mistral-7B-Instruct-v0.2. ECE is computed on
> `p_high_quality = 1 - minmax(scores)` against the binary high-quality
> label (`Accuracy=1` for QA, `COMET >= train_median` for NMT). Method
> groupings (Confidence, Hybrid, Mechanistic, Ours) follow
> Section~\ref{sec:baselines}. Lowest ECE per column in \textbf{bold};
> second-lowest \underline{underlined}. ``---'' = not yet run.

## Prose paragraph (insert into `09_ablations.tex`)
> \paragraph{Calibration on LM-Polygraph (Table~\ref{tab:polygraph_ece}).}
> Table~\ref{tab:polygraph} compares uncertainty scores by ranking quality
> (PRR); Table~\ref{tab:polygraph_ece} reports calibration via Expected
> Calibration Error on the same three Mis-7B-Inst cells. Lower ECE is
> better. Act-ViT and Encoder~Only are the best-calibrated detectors on
> MMLU (ECE $\leq 0.064$, vs. $> 0.5$ for most Confidence baselines);
> Temp-ViT wins the calibration race on GSM8k ($0.066$). The picture on
> WMT19 is different: short, well-conditioned Confidence baselines
> (TokenSAR, MeanTokenEntropy, Perplexity) are already well-calibrated
> on NMT outputs, so the supervised detectors trail them on ECE while
> still winning the PRR ranking comparison. Ranking quality and
> calibration are orthogonal — this table makes that explicit.

## Key Decisions
- **One new file** rather than adding an ECE column to `tab2_ood.tex`:
  the table is already two-page-width and 18 columns wide; adding a
  second metric per cell would overflow. A standalone Mis-7B-only ECE
  table is readable and matches the artifact coverage.
- **Same row set, bands, and `---` convention** as Table 3 — only the
  metric (and the bolding polarity) changes.
- **3-decimal precision** to match Table 3.
- **Bolding polarity flipped**: `\textbf{}` = minimum (best), since lower
  ECE is better. Caption announces this explicitly.
- **Variant selection** matches Table 3 (use PRR-trained variants where
  available, fall back to non-PRR variant for Temp-ViT on GSM8k) — keeps
  the two tables apples-to-apples on the trained rows.
- **Mis-7B-only**: the polygraph-benchmark/ artifacts only cover
  Mis-7B-Inst × {MMLU, GSM8k, WMT19}. Llama-2-13B and Llama-2-70B bands
  stay all-`---`, matching Table 3.
- **Where to insert prose**: under Ablations, right after the existing
  short-form ablations group, before the verbose token-level overlap
  paragraph.

## Validation
- `cd paper && PATH=/usr/local/texlive/2024/bin/x86_64-linux:$PATH latexmk -pdf main.tex`
  builds cleanly.
- `pdftotext -layout main.pdf -` shows a new "Table 4" (or similar — the
  number depends on float ordering; just confirm there is a new table
  whose caption contains "ECE" / "Calibration") with the 13 row labels
  from the source data and the values in the spec table.
- `grep -n "tab:polygraph_ece" paper/sections/*.tex` shows exactly one
  `\ref` and one `\label` (in the new figure file).
- Spot-check: MMLU column min = Act-ViT 0.061; GSM8k column min =
  Temp-ViT 0.066; WMT19 column min = TokenSAR 0.081.
