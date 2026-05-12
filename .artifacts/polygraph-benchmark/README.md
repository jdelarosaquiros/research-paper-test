# polygraph-benchmark — wmt19 deen × Mistral-7B-Instruct-v0.2

Schema (one CSV row per UE estimator): `estimator, auroc, prr, ece, brier, n_examples, gen_metric`.

- **gen_metric** = `Comet` (continuous quality; higher = better).
- **Binary threshold**: y=1 (low-quality) iff `Comet < median(train_Comet) = 0.8233`.
- **n_examples**: 2998 (test manager rows).
- **AUROC**: sklearn ROC AUC of `estimator` scores against the binary low-quality label. Higher = better.
- **PRR**: `lm_polygraph.ue_metrics.pred_rej_area.PredictionRejectionArea(max_rejection=0.5)(scores, comet)` — area under the prediction–rejection curve over the cumulative continuous quality score. Higher = better.
- **ECE**: 15-bin expected calibration error of `p_high_quality = 1 - minmax(scores)` against `y_high_quality = 1 - y_binary`. Lower = better.
- **Brier**: mean squared error between `p_high_quality` and `y_high_quality`. Lower = better.

## Trained rows
- `TempViT_Stage1` — Act-ViT pipeline Stage 1 sequence-level classifier (`pooling_legacy_actvit` encoder + linear head) trained on the wmt19 de->en train manager activation cache (`[8, T, 4096]` fp16, max-pool over L=33→8 via `patch_down_sample`).
- `ActViT_Foundation_Neff6` — upstream `ACT_Vit_foundation` (N_eff=6, L_eff=8, `legacy_patch_v2` pool) warm-started from the LongFact Foundation v2 ckpt and fine-tuned 30 epochs on the same wmt19 cache.

## Reproduction
```
# 1. Extract activation cache (CPU, ~1-2h).
/root/miniconda/envs/supervised_cocoa/bin/python .claude/temp/polygraph_wmt19deen/scripts/extract_activations.py
# 2. Train both models (parallel on GPUs 2,3).
GPU=2 bash .claude/temp/polygraph_wmt19deen/scripts/run_tempvit.sh &
GPU=3 bash .claude/temp/polygraph_wmt19deen/scripts/run_actvit_foundation.sh &
wait
# 3. Run inference (GPUs 2 and 3 in parallel).
CUDA_VISIBLE_DEVICES=2 /root/miniconda/envs/ACT_ViT_env/bin/python ...infer_models.py --which tempvit --ckpt .../actvit_best.pt --out .../tempvit_scores.npy &
CUDA_VISIBLE_DEVICES=3 /root/miniconda/envs/ACT_ViT_env/bin/python ...infer_models.py --which actvit --ckpt .../actvit_foundation_best.pt --out .../actvit_scores.npy &
wait
# 4. Build CSV.
/root/miniconda/envs/supervised_cocoa/bin/python .claude/temp/polygraph_wmt19deen/scripts/build_benchmark_csv.py
```
