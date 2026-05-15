# MMLU simple_instruct × Mistral-7B-Instruct-v0.2 — UE Benchmark

- n_test = 1461
- gen_metric = Accuracy (binary 0/1)
- mean(Accuracy) = 0.0828
- binary label y=1 iff Accuracy==0 (wrong)
- Top-10 rows highlighted (bold).

| Rank | Estimator | AUROC | PRR | ECE | Brier |
|---:|:---|---:|---:|---:|---:|
| 1 | **TempViT_PRR_Stage1** | 0.9240 | 0.1147 | 0.0471 | 0.0614 |
| 2 | **EncoderOnly_PRR_Stage1** | 0.9240 | 0.1147 | 0.0471 | 0.0614 |
| 3 | **TempViT_Stage1** | 0.9230 | 0.1147 | 0.0381 | 0.0568 |
| 4 | **TempViT_Stage3** | 0.9214 | 0.1147 | 0.3167 | 0.1601 |
| 5 | **ActViT_Foundation_Neff6** | 0.9165 | 0.1134 | 0.0613 | 0.0690 |
| 6 | **EncoderOnly_PRR_Stage2** | 0.9110 | 0.1140 | 0.0638 | 0.0682 |
| 7 | **TempViT_Stage2** | 0.9108 | 0.1130 | 0.0411 | 0.0594 |
| 8 | **TempViT_PRR_Stage2** | 0.8874 | 0.1126 | 0.0827 | 0.0844 |
| 9 | **EncoderOnly_PRR_Stage3** | 0.8630 | 0.1139 | 0.4429 | 0.2714 |
| 10 | **TempViT_PRR_Stage3** | 0.8223 | 0.1105 | 0.4484 | 0.2765 |
| 11 | MeanPointwiseMutualInformation | 0.8072 | 0.1131 | 0.2247 | 0.1102 |
| 12 | MeanConditionalPointwiseMutualInformation | 0.6967 | 0.0929 | 0.0958 | 0.0755 |
| 13 | FisherRao | 0.6524 | 0.1061 | 0.1026 | 0.1030 |
| 14 | RenyiNeg | 0.6371 | 0.1061 | 0.3690 | 0.2339 |
| 15 | EigenScore | 0.6313 | 0.0951 | 0.8659 | 0.8355 |
| 16 | PTrue | 0.6288 | 0.0989 | 0.4487 | 0.2902 |
| 17 | PTrueSampling | 0.5668 | 0.0890 | 0.4042 | 0.2533 |
| 18 | TokenSAR | 0.5238 | 0.0820 | 0.8584 | 0.8266 |
| 19 | AttentionScore (layer=23) | 0.4954 | 0.0836 | 0.3437 | 0.2392 |
| 20 | EigValLaplacian_NLI_score_contra | 0.4881 | 0.0757 | 0.8727 | 0.8494 |
| 21 | NumSemSets | 0.4853 | 0.0797 | 0.8668 | 0.8402 |
| 22 | SemanticDensity | 0.4521 | 0.0765 | 0.6053 | 0.4705 |
| 23 | LexicalSimilarity_BLEU | 0.4414 | 0.0755 | 0.7835 | 0.7452 |
| 24 | EigValLaplacian_Jaccard_score | 0.4403 | 0.0756 | 0.8582 | 0.8261 |
| 25 | LexicalSimilarity_rougeL | 0.4395 | 0.0751 | 0.8271 | 0.7916 |
| 26 | LexicalSimilarity_rouge1 | 0.4395 | 0.0751 | 0.8261 | 0.7916 |
| 27 | DegMat_Jaccard_score | 0.4369 | 0.0750 | 0.7974 | 0.7591 |
| 28 | Eccentricity_Jaccard_score | 0.4292 | 0.0735 | 0.7744 | 0.7328 |
| 29 | CCP | 0.4103 | 0.0764 | 0.8621 | 0.8351 |
| 30 | BoostedProbSequence | 0.4072 | 0.0728 | 0.9119 | 0.9083 |
| 31 | RAUQ | 0.4066 | 0.0722 | 0.7426 | 0.6388 |
| 32 | EigValLaplacian_NLI_score_entail | 0.3979 | 0.0708 | 0.8668 | 0.8387 |
| 33 | Eccentricity_NLI_score_entail | 0.3884 | 0.0674 | 0.7939 | 0.7602 |
| 34 | RAUQ (entropy) | 0.3730 | 0.0658 | 0.7730 | 0.6918 |
| 35 | DegMat_NLI_score_contra | 0.3624 | 0.0682 | 0.8376 | 0.8086 |
| 36 | SemanticEntropy | 0.3618 | 0.0658 | 0.8958 | 0.8817 |
| 37 | LUQ | 0.3613 | 0.0679 | 0.8233 | 0.7913 |
| 38 | MonteCarloSequenceEntropy | 0.3586 | 0.0653 | 0.9021 | 0.8916 |
| 39 | SemanticEntropy (Direct) | 0.3575 | 0.0650 | 0.7034 | 0.6887 |
| 40 | Perplexity | 0.3563 | 0.0649 | 0.9100 | 0.9052 |
| 41 | MaximumSequenceProbability | 0.3563 | 0.0649 | 0.9100 | 0.9052 |
| 42 | MeanTokenEntropy | 0.3554 | 0.0646 | 0.8340 | 0.7958 |
| 43 | SelfCertainty | 0.3525 | 0.0721 | 0.5302 | 0.3907 |
| 44 | MonteCarloNormalizedSequenceEntropy | 0.3508 | 0.0640 | 0.9065 | 0.8990 |
| 45 | CocoaMSP | 0.3395 | 0.0626 | 0.8918 | 0.8780 |
| 46 | CocoaPPL | 0.3395 | 0.0626 | 0.8918 | 0.8780 |
| 47 | CocoaMTE | 0.3356 | 0.0619 | 0.8872 | 0.8712 |
| 48 | CSL | 0.3349 | 0.0616 | 0.9077 | 0.9019 |
| 49 | Eccentricity_NLI_score_contra | 0.3293 | 0.0632 | 0.8382 | 0.8098 |
| 50 | KernelLanguageEntropy | 0.3182 | 0.0648 | 0.7621 | 0.7183 |
| 51 | DegMat_NLI_score_entail | 0.3141 | 0.0644 | 0.7646 | 0.7150 |
| 52 | SentenceSAR | 0.2762 | 0.0603 | 0.9005 | 0.8893 |
| 53 | SAR | 0.2693 | 0.0586 | 0.8368 | 0.8006 |
| 54 | GreedyAveDissimilarity | 0.2246 | 0.0490 | 0.8301 | 0.7968 |
| 55 | LexicalSimilarity_rouge2 | 0.0622 | 0.0176 | 0.7925 | 0.7550 |
