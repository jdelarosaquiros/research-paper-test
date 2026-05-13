# Hallu-signal ROC-AUC versus token offset relative to hallucinated span (Llama-2-13b-chat-hf, RAGTruth)

## Caption (figure-level)

**Figure.** Per-offset ROC-AUC of a linear probe (logistic regression, layer
L=1 of the L=8 pre-pooled hidden-state grid; class-weighted, lbfgs) measured on
each token offset relative to a hallucinated span in RAGTruth. Each bar is a
single pooled ROC-AUC computed over the cohort of hallu-span events
(positives = probe scores at the indicated offset; negatives = matched
supported-sample tokens at the same task_type and relative response position).
Teal bars use tokens from the **continuous non-hallucinated run immediately
adjacent to the span**; the chart never crosses an earlier or later hallu span.
Coral bars (F, M, L) are the **first, middle, and last token of the
hallucinated span itself**. The dashed line marks chance (AUC = 0.5).

The shape decomposes into three regimes:

1. **Pre-span ramp (offset −24 to −1).** Anticipatory signal builds smoothly
   from near chance (AUC 0.53 at −24) to 0.66 at the token immediately
   before the span. Adjacent context already carries the signal one token
   ahead of any hallucinated emission.
2. **In-span monotone rise (F → M → L; 0.71 → 0.77 → 0.79).** The probe
   becomes increasingly confident as it reads tokens deeper into the
   hallucinated span. Peak AUC is at the last hallu token.
3. **Post-span persistence and decay (+1 to +24).** The token immediately
   after the span is nearly as informative as the last hallu token
   (AUC 0.76). The signal then decays smoothly back toward chance over the
   next ~24 tokens (AUC 0.51 at +24). Compared to the pre-span ramp at the
   same absolute distance, the post-span trail is consistently higher — the
   residual stream retains the hallu component longer after the event than
   it announced it beforehand.

## Protocol details

- **Probe.** sklearn `LogisticRegression(solver='lbfgs', C=1.0,
  class_weight='balanced', max_iter=200)` trained on per-token features at
  layer L=1 of the L=8 max-pool grid, k=0 (the standard reactive cell).
  Training subsampled to 25 000 stratified pairs.
- **Hallu spans.** Maximal contiguous runs of hallucinated tokens, derived
  from `passage_atom_spans_all.jsonl` per-token `is_supported` labels in the
  RAGTruth × Llama-2-13b-chat-hf split. The same response can contribute
  multiple hallu-span events (here 393 events from 207 hallu test samples).
- **Pre-/post-context bounds.** For each hallu span, the pre-context is the
  maximal contiguous non-hallu run ending at `hallu_start − 1`; analogously
  for post-context. The chart never crosses an adjacent hallu span: if the
  immediately-preceding non-hallu run is shorter than 24 tokens, the
  far-negative slots simply have fewer contributing events.
- **In-span sampling.** F = `hallu_start`, L = `hallu_end`, M =
  `hallu_start + span_len // 2`. Single-token spans contribute F = M = L
  (the same token three times); two-token spans contribute F at the first
  token and M = L at the second.
- **Negative matching.** Each positive at offset *k* is paired with one
  random supported-sample token of the same `task_type` and same
  relative-position bin (width 0.1 in `t / T_resp`). Seed = 0 throughout.

## Event counts per slot (omitted from the chart; included for completeness)

The lower panel showing per-slot event counts has been dropped from this
figure. The counts decay smoothly with offset because pre- and post-context
runs of the maximum 24-token length are not always available:

| slot  | events | slot   | events |
|------:|------:|------:|------:|
| −24   | 278   |  F    | 393   |
| −20   | 293   |  M    | 393   |
| −16   | 304   |  L    | 393   |
| −12   | 317   | +1    | 375   |
| −8    | 332   | +4    | 328   |
| −4    | 347   | +8    | 312   |
| −1    | 391   | +16   | 278   |
|       |       | +24   | 247   |

Total events: 393 (from 207 hallu test samples). Slot **−1** has 391 of 393
events (the two missing are spans starting at token 0 of their response);
slots ±24 retain about 70 % of events. Any apparent AUC fluctuations at far
offsets should be read against these slightly smaller and re-weighted
sub-cohorts.

## Reading guide

- Compare **+1 vs −1**: 0.76 vs 0.66. The probe is *more* confident at the
  token right after the span ends than at the token right before it starts —
  the signal is asymmetric, with stronger post-span persistence than
  pre-span anticipation.
- Compare **F vs L**: 0.71 vs 0.79. Within a span, the probe sharpens as it
  reads more hallucinated context. Uncertainty *accumulates* through the
  emission.
- Compare extreme offsets **−24 (0.53) and +24 (0.51)**: both back near
  chance. The signal is fully localised to a window of roughly ±20 tokens
  around the span.

## Reproduction

```bash
# From workspace root
ENV=/root/miniconda/envs/ACT_ViT_env/bin/python
$ENV research-repo-template/.artifacts/signal-propagation-chart/gen_signal_propagation.py
```

Requires the upstream per-token-lag pipeline's probe pickles and the
per-offset CSV at
`papers/repos/temp-vit/artifacts/per_token_signal_identity/results/per_offset_auc_span_aligned.csv`.

## Related artifacts

- Raw multi-panel version (Mistral + Llama, with the lower count panel):
  `.claude/docs/per_token_pre_hallu_signal/figs/signal/per_offset_auc_span_aligned_{mistral,llama}.png`.
- Full study writeup: `.claude/docs/per_token_pre_hallu_signal/signal_identity.md`.
