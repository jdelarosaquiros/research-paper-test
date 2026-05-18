# Task: Add HaMI (Niu et al., NeurIPS 2025) as a baseline

## What
Add **HaMI** — "Robust Hallucination Detection in LLMs via Adaptive Token Selection"
(Niu, Haddadi, Pang; NeurIPS 2025) — to the paper as:

1. A cited method in the Mechanistic subsection of Related Work
   (`paper/sections/02_related_work.tex`).
2. A new entry in the Mechanistic baseline paragraph
   (`paper/sections/05_experiments.tex`, `\paragraph{Mechanistic.}`).
3. A new "HaMI" row in tables 1, 2, and 3, with all-`---` placeholders matching
   the existing Fact-Probe / Feature-Gaps convention ("---" = not yet run).
4. A new bib entry `niu2025hami` in `paper/references.bib`.

## Why
HaMI is highly relevant prior work: it is a mechanistic / internal-representation
detector that uses **top-$k$ MIL on token hidden states** — the same Multiple-Instance
Learning machinery this paper uses in its Stage-2 windowed top-$k$ aggregation.
Citing and benchmarking it is necessary for the Mechanistic comparison to be
complete; without it, a reviewer can plausibly object that the paper's MIL
formulation is not contextualised against the closest published MIL approach.

The user picked "All `---` placeholders" — HaMI was evaluated by its authors on
short-form QA only (Trivia QA, SQuAD, NQ, BioASQ × LLaMA-3.1-8B / Mistral-Nemo-12B /
LLaMA-3.3-70B); none of those cells line up with the paper's Mis-7B-Inst /
Llama-2-13B / Llama-2-70B × RAGTruth / FactScore / LongFact grid (Tables 1, 3) or
its short-form Polygraph grid (Table 2: TriviaQA / CoQA / MMLU / GSM8k / WMT14 /
WMT19). Code at https://github.com/mala-lab/HaMI is public if a follow-up wants to
fill cells.

## Files to Change
- `paper/references.bib` — add `@inproceedings{niu2025hami, ...}` (NeurIPS 2025).
- `paper/sections/02_related_work.tex` — add one or two sentences in the
  "Mechanistic hallucination detection" subsection citing HaMI as the closest
  MIL-based mechanistic detector; differentiate from this paper's window-pooled
  formulation. Place near the existing claim-level / per-token probe block.
- `paper/sections/05_experiments.tex` — add HaMI to the `\paragraph{Mechanistic.}`
  baseline list with its citation.
- `paper/figs/tab1_main.tex` — add a HaMI row in the Mechanistic band, all-`---`.
- `paper/figs/tab2_ood.tex` — same, all-`---`.
  (Note: this is the LM-Polygraph short-form table, labelled `tab:polygraph`; the
  file is named `tab2_ood.tex` for historical reasons.)
- `paper/figs/tab3_sentence.tex` — same, all-`---`.

## Key Decisions
- **Row placement**: insert HaMI in the Mechanistic band, alphabetically right
  before Act-ViT (so order becomes: Fact-Probe, Feature-Gaps, HaMI, Act-ViT).
  Rationale: keeps Act-ViT last in the band because Section 4 describes Temp-ViT
  as building on Act-ViT; HaMI sits with the other "not-yet-run" rows.
- **All-`---` cells**: matches Fact-Probe / Feature-Gaps. Captions already
  document "---" = not yet run, so no caption change needed.
- **Bib key**: `niu2025hami` — matches the project's `surname{year}{shortname}`
  convention (e.g. `han2025factprobe`, `bakman2025featuregaps`).
- **Related-work treatment**: 1–2 sentences max. Frame HaMI as an *adaptive
  top-$k$ MIL on raw token representations* and contrast with this paper's
  *window-pooled top-$k$ MIL on Act-ViT activations*. Cite under Mechanistic
  (not Uncertainty), because HaMI's core signal is hidden-state representation;
  its uncertainty-augmentation module is a bonus, not the primary signal.
- **Authors / venue for bib**: Mengjia Niu, Hamed Haddadi, Guansong Pang;
  NeurIPS 2025 (per the PDF footer "39th Conference on Neural Information
  Processing Systems (NeurIPS 2025)").
- **Do not run HaMI here**: scope is paper-writing. Running it requires
  pulling the public repo and adapting to long-form Factscore/LongFact/RAGTruth
  with the paper's generators — out of scope for this task.

## Validation
- `cd paper && PATH=/usr/local/texlive/2024/bin/x86_64-linux:$PATH latexmk -pdf main.tex`
  succeeds with no new errors / no undefined-citation warning for `niu2025hami`.
- `grep -n "HaMI\|niu2025hami" paper/sections/*.tex paper/figs/tab[123]*.tex paper/references.bib`
  shows the new mentions in each target file.
- Spot-check the rendered PDF: HaMI appears as a row in tables 1, 2, 3, in the
  Mechanistic band right before Act-ViT, with `---` in every cell.
- Related Work paragraph compiles and renders cleanly (no broken line wraps or
  citation overflow).
