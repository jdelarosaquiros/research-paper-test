# GSM8K simple_instruct × Mistral-7B-Instruct-v0.2 — UE Benchmark

- n_test = 1319
- gen_metric = Accuracy (binary 0/1)
- mean(Accuracy) = 0.4117
- binary label y=1 iff Accuracy==0 (wrong)
- Top-10 rows highlighted (bold).

| Rank | Estimator | AUROC | PRR | ECE | Brier |
|---:|:---|---:|---:|---:|---:|
| 1 | **ActViT_Foundation_Neff6** | 0.8643 | 0.5387 | 0.1105 | 0.1642 |
| 2 | **TempViT_Stage2** | 0.8604 | 0.5355 | 0.0801 | 0.1575 |
| 3 | **TempViT_Stage3** | 0.8509 | 0.5296 | 0.0657 | 0.1566 |
| 4 | **TempViT_Stage1** | 0.8421 | 0.5299 | 0.1745 | 0.2019 |
| 5 | **CocoaMSP** | 0.7689 | 0.5023 | 0.3887 | 0.3518 |
| 6 | **CocoaMTE** | 0.7645 | 0.5010 | 0.3191 | 0.3007 |
| 7 | **CocoaPPL** | 0.7623 | 0.4999 | 0.3156 | 0.2990 |
| 8 | **CCP** | 0.7453 | 0.5020 | 0.2999 | 0.3065 |
| 9 | **SemanticEntropy** | 0.7423 | 0.4982 | 0.3418 | 0.3242 |
| 10 | **MaximumSequenceProbability** | 0.7403 | 0.4991 | 0.3549 | 0.3314 |
| 11 | GreedyAveDissimilarity | 0.7306 | 0.4801 | 0.1118 | 0.2113 |
| 12 | MonteCarloSequenceEntropy | 0.7284 | 0.4916 | 0.2815 | 0.2869 |
| 13 | SAR | 0.7239 | 0.4832 | 0.0846 | 0.2089 |
| 14 | EigenScore | 0.7229 | 0.4923 | 0.1127 | 0.2196 |
| 15 | DegMat_Jaccard_score | 0.7189 | 0.4866 | 0.0694 | 0.2122 |
| 16 | EigValLaplacian_Jaccard_score | 0.7171 | 0.4861 | 0.1797 | 0.2404 |
| 17 | LexicalSimilarity_rougeL | 0.7169 | 0.4870 | 0.0317 | 0.2077 |
| 18 | Eccentricity_Jaccard_score | 0.7146 | 0.4891 | 0.0895 | 0.2186 |
| 19 | SentenceSAR | 0.7137 | 0.4887 | 0.3847 | 0.3628 |
| 20 | RAUQ | 0.7128 | 0.4883 | 0.1437 | 0.2312 |
| 21 | RAUQ (entropy) | 0.7105 | 0.4880 | 0.2104 | 0.2566 |
| 22 | LexicalSimilarity_rouge1 | 0.7084 | 0.4793 | 0.0385 | 0.2099 |
| 23 | LexicalSimilarity_rouge2 | 0.7050 | 0.4818 | 0.0659 | 0.2154 |
| 24 | MeanTokenEntropy | 0.7021 | 0.4877 | 0.3005 | 0.3054 |
| 25 | CSL | 0.7015 | 0.4846 | 0.4140 | 0.3877 |
| 26 | BoostedProbSequence | 0.7011 | 0.4880 | 0.4566 | 0.4300 |
| 27 | Perplexity | 0.6981 | 0.4864 | 0.2576 | 0.2808 |
| 28 | TokenSAR | 0.6963 | 0.4858 | 0.2568 | 0.2808 |
| 29 | LexicalSimilarity_BLEU | 0.6940 | 0.4762 | 0.1372 | 0.2327 |
| 30 | KernelLanguageEntropy | 0.6864 | 0.4675 | 0.1161 | 0.2290 |
| 31 | Eccentricity_NLI_score_entail | 0.6860 | 0.4723 | 0.1016 | 0.2320 |
| 32 | DegMat_NLI_score_entail | 0.6839 | 0.4658 | 0.1612 | 0.2442 |
| 33 | MonteCarloNormalizedSequenceEntropy | 0.6691 | 0.4718 | 0.1879 | 0.2564 |
| 34 | LUQ | 0.6622 | 0.4605 | 0.2621 | 0.3035 |
| 35 | SelfCertainty | 0.6610 | 0.4724 | 0.1416 | 0.2432 |
| 36 | EigValLaplacian_NLI_score_entail | 0.6592 | 0.4561 | 0.4111 | 0.3966 |
| 37 | DegMat_NLI_score_contra | 0.6560 | 0.4577 | 0.3059 | 0.3295 |
| 38 | Eccentricity_NLI_score_contra | 0.6536 | 0.4618 | 0.2121 | 0.3013 |
| 39 | EigValLaplacian_NLI_score_contra | 0.6427 | 0.4512 | 0.4187 | 0.4120 |
| 40 | SemanticDensity | 0.5606 | 0.4415 | 0.3777 | 0.3846 |
| 41 | NumSemSets | 0.5265 | 0.4231 | 0.4948 | 0.5029 |
| 42 | AttentionScore (layer=23) | 0.4920 | 0.4101 | 0.1446 | 0.2782 |
| 43 | PTrue | 0.4600 | 0.4075 | 0.1519 | 0.2760 |
| 44 | MeanPointwiseMutualInformation | 0.4533 | 0.4012 | 0.1493 | 0.2763 |
| 45 | RenyiNeg | 0.3463 | 0.3596 | 0.2276 | 0.3099 |
| 46 | FisherRao | 0.3431 | 0.3580 | 0.2300 | 0.3042 |
| 47 | PTrueSampling | 0.3247 | 0.3456 | 0.3465 | 0.3671 |
| 48 | MeanConditionalPointwiseMutualInformation | 0.3020 | 0.3446 | 0.2633 | 0.3210 |
| 49 | ACT_ViT_legacy_neff100 | 0.2957 | 0.3440 | 0.4429 | 0.4757 |
| 50 | ACT_ViT_legacy_factprobe_gsm8k_neff100 | 0.2957 | 0.3440 | 0.4429 | 0.4757 |
| 51 | SemanticEntropy (Direct) | 0.2923 | 0.3348 | 0.3514 | 0.3662 |
| 52 | ACT_ViT_legacy_neff1 | 0.2897 | 0.3349 | 0.4430 | 0.4569 |
| 53 | ACT_ViT_legacy_factprobe_gsm8k_neff50 | 0.2856 | 0.3379 | 0.4450 | 0.4775 |
| 54 | ACT_ViT_legacy_neff200 | 0.2817 | 0.3369 | 0.4268 | 0.4636 |
| 55 | ACT_ViT_legacy_factprobe_gsm8k_neff200 | 0.2817 | 0.3369 | 0.4268 | 0.4636 |
| 56 | ACT_ViT_legacy_mean_neff200 | 0.2749 | 0.3323 | 0.4322 | 0.4528 |
| 57 | ACT_ViT_legacy_neff20 | 0.2738 | 0.3309 | 0.4403 | 0.4665 |
| 58 | ACT_ViT_legacy_factprobe_gsm8k_neff20 | 0.2738 | 0.3309 | 0.4403 | 0.4665 |
| 59 | ACT_ViT_legacy_neff400 | 0.2712 | 0.3310 | 0.4575 | 0.4895 |
| 60 | ACT_ViT_legacy_mean_neff20 | 0.2667 | 0.3308 | 0.4558 | 0.4747 |
| 61 | ACT_ViT_legacy_mean_neff400 | 0.2662 | 0.3301 | 0.4531 | 0.4636 |
| 62 | ACT_ViT_legacy_mean_neff100 | 0.2638 | 0.3321 | 0.4694 | 0.4704 |
| 63 | ACT_ViT_legacy_mean_neff1 | 0.2542 | 0.3216 | 0.4787 | 0.4834 |
