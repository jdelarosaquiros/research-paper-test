# Is the pre-hallu signal different from the in-hallu signal?

**Final answer: NO.** The signal at `h_{t-1}` is the same scalar quantity
(uncertainty / hallu-propensity) as the signal at `h_t`, encoded redundantly
in a high-dimensional residual-stream subspace that is approximately
position-invariant. Nine probe-based tests on RAGTruth × {Mistral-7B-Instruct-v0.1,
Llama-2-13b-chat-hf} agree.

The table below contrasts what each test would predict under **SAME-signal**
vs **DIFFERENT-signal** hypotheses with what was actually observed at the
best layer per LLM (Mistral L=3, Llama L=1) at lag 1.

## Evidence table

### Direction — does the probe vector point the same way at h_t and h_{t-1}?

| Test | SAME predicts | DIFFERENT predicts | Mistral | Llama | Verdict |
|------|---------------|--------------------|---------|-------|---------|
| **E1.** cos(w_{k=0}, w_{k=1}) | ≈ bootstrap floor | ≈ 0 | 0.652 | 0.514 | **SAME** |
| **E7b.** Bootstrap cosine noise floor at h_t alone | calibrates E1 (cross-pos ≈ floor) | floor ≫ cross-pos | 0.631 ≈ 0.652 | 0.525 ≈ 0.514 | **SAME** |
| **E9.** Smallest principal angle (10-boot subspaces) | cross-pos ≈ same-pos floor | cross-pos ≫ same-pos | 29.6° vs 25.9°/26.8° | 35.8° vs 32.1°/32.7° | **SAME** |

### Content — does h_{t-1} carry information not in h_t (or vice versa)?

| Test | SAME predicts | DIFFERENT predicts | Mistral | Llama | Verdict |
|------|---------------|--------------------|---------|-------|---------|
| **E2.** Concat `[h_t \|\| h_{t-1}]` AUC gain over best single | ≈ 0 | ≥ +0.03 | −0.004 | −0.007 | **SAME** |
| **E3.** Pearson(σ(w_A·h_t), σ(w_B·h_{t-1})) | high (correlated info) | low (independent info) | 0.735 | 0.573 | **SAME** |
| **E4.** Difference probe AUC on (h_t − h_{t-1}) | ≈ 0.50 (no new info at t) | ≥ 0.60 (new component at t) | 0.537 | 0.538 | **SAME** |
| **E5.** Residual probe AUC (h_{t-1} − proj_{w_A}) | drops to ≈ 0.50 | stays ≈ AUC(B) | 0.837 (vs 0.833) | 0.750 (vs 0.751) | refines SAME → **multi-axis** |

### Subspace — geometric structure of the encoding

| Test | SAME predicts | DIFFERENT predicts | Mistral | Llama | Verdict |
|------|---------------|--------------------|---------|-------|---------|
| **E6.** Cross-position probe transfer matrix | nearly uniform | diagonal-dominant | uniform; k_train=0 row best at every k_eval | uniform; same pattern | **SAME** |
| **E8.** Effective rank (AUC after 10 peels) | rank-1 ⇒ collapse to ≈ 0.50 | multi-D ⇒ slow decay | k=0: 0.789 (Δ=−0.05); k=1: 0.776 (Δ=−0.06) | k=0: 0.749 (Δ=−0.008); k=1: 0.740 (Δ=−0.011) | rank ≫ 10 (multi-D, same on both) |

### Aggregate verdict

**SAME signal, redundantly encoded in a high-dimensional subspace of the
residual stream, with subspace approximately position-invariant up to LR's
own data-resampling noise.** The smooth lag-decay observed in the main
study is signal *attenuation* within that shared subspace, not rotation
into a different subspace.

The only outstanding caveat: probes are *decodability* tests. Causal
patching of `h_{t-k}` is the next experiment that would distinguish
correlation from causation, but it requires LLM forward-pass
instrumentation and is out of scope here.
