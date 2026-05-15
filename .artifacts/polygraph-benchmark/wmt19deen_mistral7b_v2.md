# wmt19 de->en × Mistral-7B-Instruct-v0.2 — UE Benchmark

- n_test = 2998
- gen_metric = Comet
- binary threshold y=(gen_metric < train_median) = (Comet < 0.8233)
- Top-10 rows highlighted (bold).

| Rank | Estimator | AUROC | PRR | ECE | Brier |
|---:|:---|---:|---:|---:|---:|
| 1 | **TempViT_Stage1** | 0.8069 | 0.8178 | 0.3945 | 0.3112 |
| 2 | **TempViT_Stage2** | 0.7989 | 0.8185 | 0.1049 | 0.1551 |
| 3 | **TempViT_PRR_Stage2** | 0.7926 | 0.8170 | 0.2668 | 0.2448 |
| 4 | **EncoderOnly_PRR_Stage2** | 0.7899 | 0.8162 | 0.1541 | 0.2037 |
| 5 | **TempViT_PRR_Stage1** | 0.7861 | 0.8158 | 0.2646 | 0.2481 |
| 6 | **EncoderOnly_PRR_Stage1** | 0.7861 | 0.8158 | 0.2646 | 0.2481 |
| 7 | **TempViT_Stage3** | 0.7835 | 0.8155 | 0.1619 | 0.1788 |
| 8 | **ActViT_Foundation_Neff6** | 0.7775 | 0.8150 | 0.1696 | 0.1823 |
| 9 | **SelfCertainty** | 0.7766 | 0.8160 | 0.1766 | 0.1854 |
| 10 | **CocoaMTE** | 0.7722 | 0.8146 | 0.2327 | 0.2332 |
| 11 | EncoderOnly_PRR_Stage3 | 0.7695 | 0.8150 | 0.0748 | 0.1650 |
| 12 | CocoaPPL | 0.7565 | 0.8131 | 0.2331 | 0.2336 |
| 13 | SAR | 0.7523 | 0.8129 | 0.1378 | 0.1839 |
| 14 | LUQ | 0.7501 | 0.8108 | 0.2167 | 0.2211 |
| 15 | DegMat_NLI_score_contra | 0.7499 | 0.8105 | 0.2274 | 0.2296 |
| 16 | TempViT_PRR_Stage3 | 0.7468 | 0.8126 | 0.1775 | 0.2158 |
| 17 | BoostedProbSequence | 0.7459 | 0.8122 | 0.2003 | 0.2141 |
| 18 | KernelLanguageEntropy | 0.7458 | 0.8111 | 0.1482 | 0.1841 |
| 19 | GreedyAveDissimilarity | 0.7457 | 0.8121 | 0.2131 | 0.2175 |
| 20 | Eccentricity_NLI_score_entail | 0.7453 | 0.8116 | 0.1197 | 0.1803 |
| 21 | DegMat_NLI_score_entail | 0.7452 | 0.8110 | 0.1527 | 0.1847 |
| 22 | EigValLaplacian_NLI_score_contra | 0.7433 | 0.8108 | 0.2376 | 0.2383 |
| 23 | EigValLaplacian_NLI_score_entail | 0.7419 | 0.8110 | 0.2236 | 0.2255 |
| 24 | Eccentricity_NLI_score_contra | 0.7419 | 0.8102 | 0.2137 | 0.2258 |
| 25 | CocoaMSP | 0.7407 | 0.8134 | 0.2441 | 0.2431 |
| 26 | SemanticDensity | 0.7377 | 0.8101 | 0.2147 | 0.2196 |
| 27 | MeanTokenEntropy | 0.7330 | 0.8102 | 0.0900 | 0.1745 |
| 28 | LexicalSimilarity_rouge1 | 0.7307 | 0.8109 | 0.1036 | 0.1735 |
| 29 | LexicalSimilarity_rougeL | 0.7285 | 0.8107 | 0.0891 | 0.1699 |
| 30 | LexicalSimilarity_rouge2 | 0.7202 | 0.8098 | 0.0390 | 0.1648 |
| 31 | EigValLaplacian_Jaccard_score | 0.7198 | 0.8095 | 0.1718 | 0.2000 |
| 32 | DegMat_Jaccard_score | 0.7194 | 0.8097 | 0.0420 | 0.1635 |
| 33 | MonteCarloNormalizedSequenceEntropy | 0.7190 | 0.8092 | 0.0202 | 0.1649 |
| 34 | SemanticEntropy | 0.7100 | 0.8099 | 0.1783 | 0.2035 |
| 35 | LexicalSimilarity_BLEU | 0.7089 | 0.8073 | 0.0935 | 0.1759 |
| 36 | Perplexity | 0.7030 | 0.8065 | 0.0947 | 0.1784 |
| 37 | TokenSAR | 0.7013 | 0.8054 | 0.0808 | 0.1764 |
| 38 | Eccentricity_Jaccard_score | 0.6957 | 0.8072 | 0.1155 | 0.1801 |
| 39 | CSL | 0.6931 | 0.8051 | 0.1624 | 0.1997 |
| 40 | MonteCarloSequenceEntropy | 0.6931 | 0.8082 | 0.1700 | 0.2011 |
| 41 | RAUQ (entropy) | 0.6837 | 0.8070 | 0.2105 | 0.2136 |
| 42 | EigenScore | 0.6833 | 0.8056 | 0.1707 | 0.2000 |
| 43 | SentenceSAR | 0.6811 | 0.8061 | 0.0951 | 0.1803 |
| 44 | MaximumSequenceProbability | 0.6796 | 0.8064 | 0.1902 | 0.2114 |
| 45 | CCP | 0.6669 | 0.8038 | 0.1320 | 0.1950 |
| 46 | RAUQ | 0.6561 | 0.8047 | 0.3249 | 0.2815 |
| 47 | SemanticEntropy (Direct) | 0.6061 | 0.7950 | 0.6107 | 0.5757 |
| 48 | MeanPointwiseMutualInformation | 0.5470 | 0.7906 | 0.3276 | 0.2969 |
| 49 | NumSemSets | 0.5276 | 0.7872 | 0.2418 | 0.2437 |
| 50 | AttentionScore (layer=23) | 0.5100 | 0.7877 | 0.3038 | 0.2919 |
| 51 | PTrue | 0.4577 | 0.7819 | 0.1994 | 0.2400 |
| 52 | PTrueSampling | 0.3841 | 0.7768 | 0.3074 | 0.3017 |
| 53 | MeanConditionalPointwiseMutualInformation | 0.3083 | 0.7658 | 0.5070 | 0.4772 |
| 54 | RenyiNeg | 0.2270 | 0.7597 | 0.3805 | 0.3472 |
| 55 | FisherRao | 0.2140 | 0.7587 | 0.5332 | 0.4938 |
