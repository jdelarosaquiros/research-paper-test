# Task: Add a Hybrid baseline category for CSL / AttentionScore / RAUQ

## What
Introduce a fourth baseline band — **Hybrid** — to the paper. Move CSL,
AttentionScore, and RAUQ out of the Mechanistic group (where they currently
sit) into Hybrid in:

1. The `\paragraph{Baselines.}` block of `paper/sections/05_experiments.tex` —
   split off a new `\paragraph{Hybrid.}` between Confidence and Mechanistic.
2. The three result tables: `tab1_main.tex`, `tab2_ood.tex`, `tab3_sentence.tex`
   — insert a new `\textit{Hybrid}` band between the existing Confidence and
   Mechanistic bands and move the three rows there.

## Why
CSL, AttentionScore, and RAUQ all combine next-token confidence signals with
attention-based mechanistic features — they're a distinct genre from both the
pure confidence baselines (output-distribution only) and the pure mechanistic
baselines (hidden-state probes / activation encoders / MIL detectors).
Currently they're shoved into Mechanistic, which the earlier
`baselines-section-update.md` plan flagged as a known compromise (note: "CSL is
'information-based' in the LM-Polygraph taxonomy but kept under Mechanistic
here because it mixes log-probs with attention weights"). A separate Hybrid
band reflects that mixture honestly and makes the Mechanistic comparison
cleaner.

## Files to Change
- `paper/sections/05_experiments.tex` — split the Mechanistic paragraph; add
  `\paragraph{Hybrid.}` containing CSL, AttentionScore, RAUQ with their
  existing citations.
- `paper/figs/tab1_main.tex` — add a `Hybrid` band between Confidence and
  Mechanistic; move the CSL / AttentionScore / RAUQ rows there.
- `paper/figs/tab2_ood.tex` — same.
- `paper/figs/tab3_sentence.tex` — same.

## Key Decisions
- **Band order**: Confidence → Hybrid → Mechanistic → Ours.
  Rationale: ordering follows degree of access to model internals (output-
  distribution only → output + attention → hidden states / activation maps /
  MIL on internals → ours). This is the natural reading order.
- **No bold/underline recomputation needed**:
  - `tab1_main.tex` and `tab3_sentence.tex` only bold/underline within the
    "Ours" band, so moving the three rows to Hybrid doesn't affect any
    bolding.
  - `tab2_ood.tex` (Table 3, PRR) bolds per-column across all bands, but
    CSL / AttentionScore / RAUQ have no bolded or underlined cells today
    (their PRR values sit well below the best/second-best on every column);
    moving them between bands changes nothing.
- **Prose grouping**: keep the three methods in the same paragraph order
  (CSL, AttentionScore, RAUQ) used today; just relabel the heading.
- **Mechanistic paragraph after move**: keeps Fact-Probe, Feature-Gaps,
  HaMI, Act-ViT — all pure hidden-state / activation-map / MIL methods.
- **Citations unchanged**: `lin2024csl`, `sriramanan2024attention`,
  `vazhentsev2025rauq` stay where they are in `references.bib`.
- **Caption convention** in tables: existing captions say "Method groupings
  (\emph{Confidence}, \emph{Mechanistic}, \emph{Ours}) follow Section X" in
  `tab1_main.tex` — update to also list `\emph{Hybrid}`. `tab2_ood.tex` and
  `tab3_sentence.tex` say "Method groupings follow Section X" without
  enumerating, so no caption change there.

## Validation
- `cd paper && PATH=/usr/local/texlive/2024/bin/x86_64-linux:$PATH latexmk -pdf main.tex`
  builds with no new errors / warnings.
- `pdftotext -layout main.pdf -` shows a `Hybrid` row separator in all three
  tables, with CSL / AttentionScore / RAUQ underneath it and no longer under
  `Mechanistic`.
- `grep -n "CSL\|AttentionScore\|RAUQ" paper/figs/tab[123]*.tex` shows each
  method exactly once per table, positioned after the Confidence band header
  and before the Mechanistic band header.
- `grep -nE "Hybrid|Mechanistic" paper/sections/05_experiments.tex` shows two
  separate `\paragraph` blocks: Hybrid (3 methods) and Mechanistic (4 methods:
  FactProbe, Feature-Gaps, HaMI, Act-ViT).
