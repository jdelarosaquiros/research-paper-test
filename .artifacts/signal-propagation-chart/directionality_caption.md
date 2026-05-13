# Directionality figure — caption

## Caption (figure-level)

**Figure.** Does the linear hallucination probe read the same direction at
`h_t` and at `h_{t-1}`? For each LLM we plot the **cosine of probe weight
vectors** under two conditions: (i) teal dots — ten pairwise cosines
obtained by refitting the **same** (`L*`, `k=0`) probe on five stratified
bootstrap resamples of the training pool, i.e. the noise floor for what
"same signal" looks like under data-resampling variance; (ii) coral diamond
— the **cross-position** cosine `cos(w_{k=0}, w_{k=1})` between the
reactive probe and the lag-1 anticipatory probe. Reference lines mark
the limits: cosine = 1 (probes are identical) and cosine = 0 (probes
point in orthogonal directions, which is what a "different signal"
hypothesis predicts).

**Reading.** On both LLMs the coral marker sits *inside* the teal cloud
(Mistral: 0.652 vs cloud 0.615–0.642; Llama: 0.514 vs cloud 0.505–0.538).
Cross-position direction agreement is statistically indistinguishable
from same-position data-resampling agreement — therefore the probe
directions at `h_t` and `h_{t-1}` are **not different**. Both markers
are also far from the "orthogonal" reference line. A *different*-signal
hypothesis would put the coral diamond near zero, well below the noise
floor; we observe the opposite.

This single comparison collapses the conclusion of nine probe-based
tests (see `evidence_table.md`) into one metric: under SAME-signal,
`cos(w_t, w_{t-1})` should land inside the bootstrap noise floor; under
DIFFERENT-signal, it should land near zero. It lands inside the floor.

## What the figure does *not* claim

- It does not establish causation. Probes are decodability tests; a
  causal-patching experiment (substitute `h_{t-k}` and observe next-token
  hallu probability) is the next test that would distinguish correlation
  from causation.
- It does not say the signal is encoded along a *single* axis. A separate
  test (the residual probe, E5 in the full table) shows the signal is
  multi-dimensional. But the multi-dim subspace is the **same** at both
  positions, up to LR's resampling noise.

## Reproduction

```bash
ENV=/root/miniconda/envs/ACT_ViT_env/bin/python
cd /workspace/storage/claude_code_test
$ENV research-repo-template/.artifacts/signal-propagation-chart/gen_directionality.py
```

Bootstrap data: `papers/repos/temp-vit/artifacts/per_token_signal_identity/results/e7b_bootstrap_noise_floor.csv`.
Cross-position cosine: `direction_cosine.csv` (same folder) filtered to the best layer per LLM.

## Related artifacts in this folder

- `evidence_table.{md,pdf,png}` — full 9-test table (one row per test).
- `fig_signal_propagation_llama.{pdf,png}` — companion shape figure of the
  ROC-AUC trajectory around each hallucinated span (single LLM).
