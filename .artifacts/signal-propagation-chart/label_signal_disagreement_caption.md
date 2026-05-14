# Label / probe disagreement figure — caption

## Caption (figure-level)

**Figure.** Per-token disagreement between the canonical reactive linear
probe (`L*`, `k=0`) and the RAGTruth annotation, on the test split of two
LLMs. The threshold is the per-token F1-optimal value tuned on the val
split with the same (`L*`, `k=0`) scores (Mistral τ = 0.92, Llama
τ = 0.94 — high because per-token labels are heavily imbalanced).

**(a)** Frequencies of the three disagreement rates, overall, per LLM.
"Miss" is the rate at which probe σ falls below τ on a token whose
RAGTruth label is hallucinated; "false alarm (in hallu sample)" is the
rate of σ ≥ τ on a token labelled supported *but inside a sample that
also contains hallu spans*; "false alarm (in supported sample)" is the
rate of σ ≥ τ on a token labelled supported inside a sample with no
hallu at all. At this operating point the probe **misses ~50% of
labelled hallu** (Mistral 0.48 / Llama 0.55) but **fires on only
6–13% of labelled-supported tokens** — high specificity, moderate
sensitivity.

**(b)** Distance gradient of false alarms inside hallu samples. For
each labelled-supported token in a hallu sample we measure the
distance (in tokens) to the nearest annotated hallu span boundary,
bucket into four bands {1–4, 5–8, 9–16, 17+}, and plot the false-alarm
rate. The rate is **3.2× higher (Mistral) / 2.6× higher (Llama)** in
the nearest band than in the far band. The dotted reference lines
mark the false-alarm rate on supported samples (where there is no
hallu nearby, by construction) — for both LLMs the 17+ band converges
to that floor (Mistral: 0.06 ≈ 0.06; Llama: 0.11 ≈ 0.11), confirming
that the elevated false-alarm rate near hallu spans reflects
**signal bleed** from the labelled span rather than a global probe
bias.

## Reading

The probe is conservative: at the F1-optimal operating point it lets
through about half of the annotated hallu tokens. This is consistent
with the SAME-signal, multi-axis verdict from `signal_identity.md` —
hallu signal is redundantly distributed across positions within a span,
so individual tokens can carry weak signal even when the span as a
whole reads as hallu. False alarms inside hallu samples are dominated
by the bleed: distance-1–4 tokens are 3× more likely to fire than
distance-17+ tokens, and the distance-17+ rate matches the supported-
sample rate. The implication for downstream detector design: a
**window-aggregated** σ-score should beat token-by-token thresholding,
because the bleed adds *correlated* signal that smoothing exploits.

## What the figure does *not* claim

- It does not show that the probe is "wrong" wherever it fires on a
  labelled-supported token — many of those firings are consistent with
  signal bleed from a nearby labelled hallu (see panel **(b)**).
- It does not separate label noise from probe blindness in the miss
  set. Spot-checking miss tokens by hand is the next step.

## Reproduction

```bash
ENV=/root/miniconda/envs/ACT_ViT_env/bin/python
cd /workspace/storage/claude_code_test
# 1. Generate the underlying tables
$ENV papers/repos/temp-vit/artifacts/per_token_signal_identity/07_label_signal_disagreement.py
# 2. Render this figure
$ENV research-repo-template/.artifacts/signal-propagation-chart/gen_label_signal_disagreement.py
```

CSV sources:
- `papers/repos/temp-vit/artifacts/per_token_signal_identity/results/label_signal_disagreement.csv`
- `papers/repos/temp-vit/artifacts/per_token_signal_identity/results/label_signal_disagreement_distance.csv`

## Related artifacts in this folder

- `fig_directionality.{pdf,png}` — single-metric "is the signal different?"
  figure (cross-position cosine vs bootstrap noise floor).
- `evidence_table.{md,pdf,png}` — nine-test identity table.
- `fig_signal_propagation_llama.{pdf,png}` — span-aligned ROC-AUC trajectory,
  the qualitative figure this study quantifies.
- Findings doc: `.claude/docs/per_token_pre_hallu_signal/label_signal_disagreement.md`.
