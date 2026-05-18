# Task: Restructure Table 3 (and Table 10) to per-category aggregates; move per-dataset view to ablation

## What
Re-shape Table 3 (PRR, `tab2_ood.tex`, `tab:polygraph`) and Table 10 (ECE,
`tab12_polygraph_ece.tex`, `tab:polygraph_ece`) from a per-dataset layout
(18 columns: 6 datasets × 3 LLMs) to a **per-category** layout (9 columns:
3 categories × 3 LLMs):

- **QA**  ← TriviaQA, CoQA, MMLU
- **CoT** ← GSM8k
- **NMT** ← WMT14, WMT19

Add the per-dataset PRR view back to the paper as a new **extended ablation
table** (Table 13). Add a Python aggregation script under
`.artifacts/polygraph-benchmark/` that materialises both aggregates as CSVs.

## Why
The current Table 3 / 10 layouts are 18-column wide and 90% empty (only the
Mistral × {MMLU, GSM8k, WMT19} cells are populated). Grouping by capability
category (QA / CoT / NMT) gives a more honest single-row-per-LLM summary at
a glance, while the extended per-dataset table preserves the raw numbers for
readers who want them. The user asked for both — the summary in the main
text, the extended version in the ablations.

The aggregation script keeps the table generation reproducible: when new
per-dataset cells become available, re-running the script regenerates the
aggregate CSVs and the latex cell values can be re-pasted directly.

## Data scope (today)
Only Mistral-7B-Instruct-v0.2 × {MMLU, GSM8k, WMT19} CSVs exist. So:

- Mistral **QA** aggregate = MMLU value (single dataset present).
- Mistral **CoT** aggregate = GSM8k value (CoT category has only GSM8k).
- Mistral **NMT** aggregate = WMT19 value (single dataset present).
- Llama-2-13B / Llama-2-70B rows: every cell stays `---`.

The aggregation script must compute mean over *present* datasets per
category (skip-NaN), so the table values continue to update correctly when
TriviaQA / CoQA / WMT14 CSVs are added later.

## Files to Change
- `.artifacts/polygraph-benchmark/aggregate_by_category.py` — **new**.
  Reads the three per-dataset CSVs, joins them by `estimator`, classifies
  each dataset into QA / CoT / NMT, and writes two aggregate CSVs.
  Stdlib only (csv, pathlib, statistics).
- `.artifacts/polygraph-benchmark/prr_by_category.csv` — **new**. Schema:
  `method, llm, qa_prr, qa_n, cot_prr, cot_n, nmt_prr, nmt_n`. The `*_n`
  columns record how many datasets contributed to each aggregate.
- `.artifacts/polygraph-benchmark/ece_by_category.csv` — **new**. Same
  schema but `*_ece` columns.
- `paper/figs/tab2_ood.tex` — replace 18-col per-dataset header with
  9-col per-category header (QA / CoT / NMT × 3 LLMs); refill cells using
  the aggregate values from the script; update caption to say "per-category
  aggregate (mean over datasets present in each category)".
- `paper/figs/tab12_polygraph_ece.tex` — same restructure (ECE values).
- `paper/figs/tab13_polygraph_extended.tex` — **new**. Verbatim copy of
  today's per-dataset 18-col layout for `tab2_ood.tex` (with the PRR
  values), labelled `tab:polygraph_extended`. This becomes the
  per-dataset ablation referenced from `09_ablations.tex`.
- `paper/sections/07_polygraph_efficiency.tex` — update prose: "per-dataset
  PRR" → "per-category PRR (QA / CoT / NMT)"; "wins WMT19 ($0.816$)" →
  "wins NMT ($0.816$)"; "edges the Act-ViT mechanistic baseline on MMLU"
  → "...on QA"; the parenthetical list of three Mis-7B cells gets reworded
  to enumerate categories rather than datasets, with the constituent
  datasets in parentheses.
- `paper/sections/09_ablations.tex` — add a new paragraph
  `\paragraph{Per-dataset LM-Polygraph results (Table~\ref{tab:polygraph_extended}).}`
  that points at the extended table; add `\input{figs/tab13_polygraph_extended}`
  to the tail input block.

## Key Decisions
- **Category assignment** (per user instruction):
  - QA: TriviaQA, CoQA, MMLU.
  - CoT: GSM8k.
  - NMT: WMT14, WMT19.
- **Aggregation = arithmetic mean** over present datasets (skip-NaN /
  skip-`---`). With only one dataset present per category today, the
  aggregates equal the per-dataset values, so existing bold/underline
  positions for Mis-7B are preserved.
- **Bolding/underlining**: same convention (per-column best/second), just
  applied to the new 3-column-per-LLM layout. For PRR higher = bold; for
  ECE lower = bold.
- **Script first, table values second**: the script writes both
  `prr_by_category.csv` and `ece_by_category.csv`. The latex cells are
  filled from those CSVs (3 decimals). When the script is re-run after
  new data lands, the values to paste into latex are the script output.
- **Extended ablation = per-dataset PRR only** (not ECE). The user picked
  "Yes — same QA/CoT/NMT layout" for the ECE table without asking for an
  extended ECE ablation; adding one would inflate the appendix without
  any new information not already in the per-dataset PRR table + the
  aggregated ECE table.
- **Caption call-out**: both restructured captions explicitly say
  "per-category aggregate (mean over datasets in category)" so a reader
  knows the cell is an aggregate rather than a single number. Caption
  also names the datasets per category.
- **Llama bands stay**: keep the LlaMa-13B-Inst and LlaMa-70B-Inst
  multicolumn headers in the new table (all `---`) so the table layout
  doesn't change visually when those LLMs are filled later.

## Aggregate cell values (3 decimals; today's Mis-7B values)

### PRR (higher is better; `tab2_ood.tex`)
| Method | QA | CoT | NMT |
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

### ECE (lower is better; `tab12_polygraph_ece.tex`)
| Method | QA | CoT | NMT |
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

(FactProbe, Feature-Gaps, HaMI, all Llama-2-13B and Llama-2-70B cells:
all `---`, same as the per-dataset tables.)

## Validation
- `python3 .artifacts/polygraph-benchmark/aggregate_by_category.py` runs
  with stdlib only and writes both CSVs.
- The script's printed per-method aggregates for the Mis-7B row match
  the tables above to 3 decimals.
- `cd paper && PATH=/usr/local/texlive/2024/bin/x86_64-linux:$PATH latexmk -pdf main.tex`
  builds cleanly.
- `pdftotext -layout main.pdf -`:
  - Table 3 caption now mentions "per-category aggregate" and the new
    headers say `QA CoT NMT` (not the six dataset names).
  - Table 10 (ECE ablation) has the same new headers.
  - A new ablation table (rendered as Table 11 or 12 depending on float
    order) appears with the per-dataset 18-column layout and PRR values.
- `grep -nE "tab:polygraph(_ece|_extended)?" paper/sections/*.tex
  paper/figs/tab*.tex` shows each label resolved exactly once.
