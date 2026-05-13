# polygraph-benchmark — UE estimator leaderboards

Schema (one CSV row per UE estimator): `estimator, auroc, prr, ece, brier, n_examples, gen_metric`.

## Cell index

| Cell | LLM | Task | Dataset | gen_metric | n_test | CSV / MD |
|:---|:---|:---|:---|:---|---:|:---|
| wmt19 de->en | Mistral-7B-Instruct-v0.2 | NMT | `LM-Polygraph/wmt19, deen_simple_instruct` | `Comet` (continuous) | 2998 | [`wmt19deen_mistral7b_v2.csv`](wmt19deen_mistral7b_v2.csv) / [`.md`](wmt19deen_mistral7b_v2.md) |
| MMLU `simple_instruct` | Mistral-7B-Instruct-v0.2 | QA | `LM-Polygraph/mmlu, simple_instruct` | `Accuracy` (binary 0/1) | 1461 | [`mmlu_simple_instruct_mistral7b_v2.csv`](mmlu_simple_instruct_mistral7b_v2.csv) / [`.md`](mmlu_simple_instruct_mistral7b_v2.md) |

> **Note on Accuracy label** (MMLU): `Accuracy` is binary (the model answer matches the gold letter). Positive class for AUROC is `y_bin = 1 - Accuracy` (wrong/hallucinated). No median threshold is applied — `y_bin` is used directly. PRR is computed against the binary `Accuracy` (higher = more correct).

## wmt19 de->en × Mistral-7B-Instruct-v0.2

- **gen_metric** = `Comet` (continuous quality; higher = better).
- **Binary threshold**: y=1 (low-quality) iff `Comet < median(train_Comet) = 0.8233`.
- **n_examples**: 2998 (test manager rows).
- **AUROC**: sklearn ROC AUC of `estimator` scores against the binary low-quality label. Higher = better.
- **PRR**: `lm_polygraph.ue_metrics.pred_rej_area.PredictionRejectionArea(max_rejection=0.5)(scores, comet)` — area under the prediction–rejection curve over the cumulative continuous quality score. Higher = better.
- **ECE**: 15-bin expected calibration error of `p_high_quality = 1 - minmax(scores)` against `y_high_quality = 1 - y_binary`. Lower = better.
- **Brier**: mean squared error between `p_high_quality` and `y_high_quality`. Lower = better.

### Trained rows
- `TempViT_Stage1` — Act-ViT pipeline Stage 1 sequence-level classifier (`pooling_legacy_actvit` encoder + linear head) trained on the wmt19 de->en train manager activation cache (`[8, T, 4096]` fp16, max-pool over L=33→8 via `patch_down_sample`).
- `TempViT_Stage2` — Stage 2 windowed MIL with a Mamba-2 head, warm-started from Stage 1's encoder. Operates on the same per-sequence `[8, T, 4096]` cache as Stage 1 (each generation is a single atom). Inference aggregates per-token Mamba logits with `topk_mean` MIL over the full sequence (`k_ratio=1.0, min_k=1`).
- `TempViT_Stage3` — Stage 3 passage-level training over synthetic 4-atom passages built from train/val by concatenating two high-quality and two low-quality wmt19 generations in alternating order. Stage 3 warm-starts the encoder + WTAL head from Stage 2 and freezes the encoder. At inference each test sequence is a one-atom passage; the score is the sigmoid of the soft-top-k-mean logit over the whole span.
- `ActViT_Foundation_Neff6` — upstream `ACT_Vit_foundation` (N_eff=6, L_eff=8, `legacy_patch_v2` pool) warm-started from the LongFact Foundation v2 ckpt and fine-tuned 30 epochs on the same wmt19 cache.

### Stage 2 / Stage 3 protocol
Stage 2 trains the Mamba-2 windowed head on the same `[8, T, 4096]` per-sequence cache as Stage 1, treating each generation as a single atom. Sequence score = MIL `topk_mean` of the per-token Mamba logits with `k_ratio=1.0, min_k=1`, warm-started from the Stage-1 encoder.

Stage 3 trains on **synthetic 4-atom passages** built by concatenating two `comet>=median` and two `comet<median` wmt19 generations in alternating order along the token axis. The sidecar records the per-atom token spans and `is_supported = 1 - cache_label`. Stage 3 warm-starts from Stage 2's encoder + WTAL head, freezes the encoder, and trains the head for 15 epochs with per-atom BCE. At inference each test sequence is its own one-atom passage; the per-sequence uncertainty is `sigmoid(soft_topk_smoothed -> topk_mean_in_segments)` over the whole span.

Note on score polarity in this CSV: Stage 1/2 + Foundation v2 are trained on `y = 1 - cache_label` (sigmoid ≈ P(high quality)), so the CSV uses `uncertainty = 1 - sigmoid`. Stage 3 is trained on `atom_label = 1 - is_supported = cache_label` (sigmoid ≈ P(low quality)), so the CSV uses `uncertainty = sigmoid` directly.

### Reproduction
```
# 1. Extract activation cache (CPU, ~1-2h).
/root/miniconda/envs/supervised_cocoa/bin/python .claude/temp/polygraph_wmt19deen/scripts/extract_activations.py
# 2. Train Temp-ViT Stage 1 + Act-ViT Foundation v2 in parallel.
GPU=2 bash .claude/temp/polygraph_wmt19deen/scripts/run_tempvit.sh &
GPU=3 bash .claude/temp/polygraph_wmt19deen/scripts/run_actvit_foundation.sh &
wait
# 3. Build synthetic Stage-3 passages (CPU).
/root/miniconda/envs/ACT_ViT_env/bin/python .claude/temp/polygraph_wmt19deen/scripts/build_stage3_synthetic_passages.py
# 4. Train Stage 2 then Stage 3 on GPU 2.
bash .claude/temp/polygraph_wmt19deen/scripts/run_tempvit_stage2.sh
bash .claude/temp/polygraph_wmt19deen/scripts/run_tempvit_stage3.sh
# 5. Run inference for all four trained models.
bash .claude/temp/polygraph_wmt19deen/scripts/run_inference_both.sh
CUDA_VISIBLE_DEVICES=2 PYTHONPATH=.:.. /root/miniconda/envs/ACT_ViT_env/bin/python .claude/temp/polygraph_wmt19deen/scripts/infer_stages_2_3.py --which stage2 --config .../cfg_wmt19deen_stage2.yaml --actvit_ckpt .../stage2/actvit_best.pt --wtal_ckpt .../stage2/wtal_best.pt --out .../tempvit_stage2_scores.npy
CUDA_VISIBLE_DEVICES=2 PYTHONPATH=.:.. /root/miniconda/envs/ACT_ViT_env/bin/python .claude/temp/polygraph_wmt19deen/scripts/infer_stages_2_3.py --which stage3 --config .../cfg_wmt19deen_stage3.yaml --actvit_ckpt .../stage3/actvit_best.pt --wtal_ckpt .../stage3/wtal_best.pt --out .../tempvit_stage3_scores.npy
# 6. Build CSV.
/root/miniconda/envs/supervised_cocoa/bin/python .claude/temp/polygraph_wmt19deen/scripts/build_benchmark_csv.py
```

## MMLU `simple_instruct` × Mistral-7B-Instruct-v0.2

- **gen_metric** = `Accuracy` (binary 0/1; 1 = correct).
- **Binary label** (positive class for AUROC): `y_bin = 1 - Accuracy` (wrong/hallucinated). No median threshold — `Accuracy` is already binary. Class imbalance ~92% positive on test (mean Accuracy ≈ 0.083).
- **n_examples**: 1461 (test manager rows; train manager also n=1461, splits are disjoint — only 3 input-text duplicates).
- **PRR**: computed against `quality = Accuracy` (binary). Both AUROC and PRR work with a binary quality target — PRR magnitudes here are smaller because the cumulative quality area is bounded by the small positive rate.
- **ECE** / **Brier**: against `y_high_quality = 1 - y_bin = Accuracy` (1 = correct), with `p_high_quality = 1 - minmax(scores)`.

### Trained rows
Same four trained rows as wmt19, retrained on the MMLU activation cache (`[8, T=2, 4096]` fp16 per generation — T_response is uniformly 2 tokens). Stage 3 is trained on synthetic 4-atom passages from MMLU (55 train + 9 val passages × 4 atoms; T_total = 8). The polarity convention is identical to the wmt19 cell.

### Reproduction
```
# 1. Extract activation cache (CPU, ~3 min). Hash-checks train vs test inputs and aborts on >50% overlap.
/root/miniconda/envs/supervised_cocoa/bin/python .claude/temp/polygraph_mmlu/scripts/extract_activations.py
# 2. Build synthetic Stage-3 passages (CPU, ~1s).
/root/miniconda/envs/supervised_cocoa/bin/python .claude/temp/polygraph_mmlu/scripts/build_stage3_synthetic_passages.py
# 3. Train Temp-ViT Stage 1 + Act-ViT Foundation v2 in parallel.
GPU=2 bash .claude/temp/polygraph_mmlu/scripts/run_tempvit.sh &
GPU=3 bash .claude/temp/polygraph_mmlu/scripts/run_actvit_foundation.sh &
wait
# 4. Train Stage 2 then Stage 3 on GPU 2 (Stage 2 uses num_workers=0 to avoid a DataLoader hang seen on the small MMLU split).
GPU=2 bash .claude/temp/polygraph_mmlu/scripts/run_tempvit_stage2.sh
GPU=2 bash .claude/temp/polygraph_mmlu/scripts/run_tempvit_stage3.sh
# 5. Run inference for all four trained models.
CUDA_VISIBLE_DEVICES=3 PYTHONPATH=.:.. /root/miniconda/envs/ACT_ViT_env/bin/python .claude/temp/polygraph_mmlu/scripts/infer_models.py --which tempvit --ckpt .../stage1/actvit_best.pt --out .../tempvit_scores.npy
CUDA_VISIBLE_DEVICES=3 PYTHONPATH=.:.. /root/miniconda/envs/ACT_ViT_env/bin/python .claude/temp/polygraph_mmlu/scripts/infer_models.py --which actvit  --ckpt .../foundation_v2_mmlu_neff6/actvit_foundation_best.pt --out .../actvit_scores.npy
CUDA_VISIBLE_DEVICES=2 PYTHONPATH=.:.. /root/miniconda/envs/ACT_ViT_env/bin/python .claude/temp/polygraph_mmlu/scripts/infer_stages_2_3.py --which stage2 --config .../cfg_mmlu_stage2.yaml --actvit_ckpt .../stage2/actvit_best.pt --wtal_ckpt .../stage2/wtal_best.pt --out .../tempvit_stage2_scores.npy
CUDA_VISIBLE_DEVICES=2 PYTHONPATH=.:.. /root/miniconda/envs/ACT_ViT_env/bin/python .claude/temp/polygraph_mmlu/scripts/infer_stages_2_3.py --which stage3 --config .../cfg_mmlu_stage3.yaml --actvit_ckpt .../stage3/actvit_best.pt --wtal_ckpt .../stage3/wtal_best.pt --out .../tempvit_stage3_scores.npy
# 6. Build CSV.
/root/miniconda/envs/supervised_cocoa/bin/python .claude/temp/polygraph_mmlu/scripts/build_benchmark_csv.py
```
