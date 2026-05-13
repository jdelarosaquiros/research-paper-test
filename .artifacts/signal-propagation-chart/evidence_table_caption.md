# Evidence table: is the pre-hallu signal *different* from the in-hallu signal?

## Caption (figure-level)

**Table.** Nine probe-based tests on RAGTruth × {Mistral-7B-Instruct-v0.1,
Llama-2-13b-chat-hf} that jointly answer whether the signal a logistic-regression
probe reads at the hidden state `h_{t-1}` is the *same* as the signal it reads
at `h_t`. Each row contrasts the prediction under a SAME-signal hypothesis with
the prediction under a DIFFERENT-signal hypothesis, then reports the observed
value at the best layer per LLM (Mistral L=3, Llama L=1) at lag 1.

The tests group into three structural questions:

- **Direction** (E1, E7b, E9) — do the probe-weight vectors point the same way?
  The cross-position cosine of 0.65 (Mistral) / 0.51 (Llama) is *inside* the
  bootstrap noise floor for refitting the *same* probe on resamples of the
  *same* data (0.63 / 0.53). The smallest principal angle between bootstrap
  subspaces at the two positions (29.6° / 35.8°) is statistically
  indistinguishable from the same-position bootstrap noise (25.9°/26.8° and
  32.1°/32.7°).
- **Content** (E2, E3, E4, E5) — does either position carry information the
  other lacks? Concat fusion gains nothing (−0.004 / −0.007), the σ-score
  Pearson is moderate (0.74 / 0.57), the difference probe is near chance
  (0.54 / 0.54), and removing the `h_t`-probe direction from `h_{t-1}`
  *doesn't* drop the residual probe's AUC (0.84 / 0.75 vs 0.83 / 0.75 baseline).
  The last result refines the picture: signal is multi-axial, not a single
  direction — but the same multi-axial information at both positions.
- **Subspace** (E6, E8) — what's the geometric structure? The cross-position
  probe-transfer matrix is nearly uniform on both LLMs, and an iterative
  peel-and-retrain procedure shows the hallu subspace has effective rank
  much greater than 10 (10 peels drop AUC by only 0.05–0.06 on Mistral and
  0.008–0.011 on Llama).

Every row's verdict points the same way: **SAME signal, redundantly encoded
in a high-dimensional residual-stream subspace, approximately position-
invariant up to LR's data-resampling noise**. The smooth lag-decay observed
in the main per-token study is signal attenuation within that shared
subspace — not rotation into a different one.

## Reading guide

- Two columns ("SAME predicts" / "DIFFERENT predicts") flank each row's
  observed values so that the table can be read as a decision check
  without needing the prose. If the observed values match the SAME column,
  the verdict on the right is **SAME**.
- The verdict column uses a single coral badge per row. Two rows have
  refined verdicts: E5 reads **MULTI** (signal lives in ≥ 2 directions, not
  just `w_A`'s direction) and E8 reads **MULTI** (signal subspace has rank
  much greater than 10). Both refinements are consistent with — and
  strengthen — the SAME-signal verdict.
- The footer banner restates the aggregate conclusion for paper-figure use.

## Caveats

The table summarises decodability tests; it does not establish that the
shared subspace is *causal* for the model's hallucinated output. Causal
patching (substitute `h_{t-k}` from a matched supported sample and observe
the next-token hallu probability) is the next experiment that would
distinguish correlation from causation, but it requires LLM forward-pass
instrumentation and is out of scope here.

## Reproduction

```bash
ENV=/root/miniconda/envs/ACT_ViT_env/bin/python
cd /workspace/storage/claude_code_test
$ENV research-repo-template/.artifacts/signal-propagation-chart/gen_evidence_table.py
```

All numbers cited in this table are pulled from
[`signal_identity.md`](../../../.claude/docs/per_token_pre_hallu_signal/signal_identity.md).
The Markdown source of the table is at
[`evidence_table.md`](evidence_table.md) in this folder.

## Related artifacts

- Companion figure (per-offset ROC-AUC anchored on hallu spans, Llama-only):
  `fig_signal_propagation_llama.{pdf,png}` in this folder.
- Multi-panel raw figures: `.claude/docs/per_token_pre_hallu_signal/figs/signal/`.
- Full study writeup: `.claude/docs/per_token_pre_hallu_signal/signal_identity.md`.
