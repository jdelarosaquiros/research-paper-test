# wmt19 de->en × Mistral-7B-Instruct-v0.2 — UE Benchmark

- n_test = 2998
- gen_metric = Comet
- binary threshold y=(gen_metric < train_median) = (Comet < 0.8233)
- Top-10 rows highlighted (bold).

| Rank | Estimator | AUROC | PRR | ECE | Brier |
|---:|:---|---:|---:|---:|---:|
| 1 | **TempViT_Stage1** | 0.8069 | 0.8178 | 0.3945 | 0.3112 |
| 2 | **ActViT_Foundation_Neff6** | 0.7775 | 0.8150 | 0.1696 | 0.1823 |
| 3 | **SelfCertainty** | 0.7766 | 0.8160 | 0.1766 | 0.1854 |
| 4 | **CocoaMTE** | 0.7722 | 0.8146 | 0.2327 | 0.2332 |
| 5 | **CocoaPPL** | 0.7565 | 0.8131 | 0.2331 | 0.2336 |
| 6 | **SAR** | 0.7523 | 0.8129 | 0.1378 | 0.1839 |
| 7 | **LUQ** | 0.7501 | 0.8108 | 0.2167 | 0.2211 |
| 8 | **DegMat_NLI_score_contra** | 0.7499 | 0.8105 | 0.2274 | 0.2296 |
| 9 | **BoostedProbSequence** | 0.7459 | 0.8122 | 0.2003 | 0.2141 |
| 10 | **KernelLanguageEntropy** | 0.7458 | 0.8111 | 0.1482 | 0.1841 |
| 11 | GreedyAveDissimilarity | 0.7457 | 0.8121 | 0.2131 | 0.2175 |
| 12 | Eccentricity_NLI_score_entail | 0.7453 | 0.8116 | 0.1197 | 0.1803 |
| 13 | DegMat_NLI_score_entail | 0.7452 | 0.8110 | 0.1527 | 0.1847 |
| 14 | EigValLaplacian_NLI_score_contra | 0.7433 | 0.8108 | 0.2376 | 0.2383 |
| 15 | EigValLaplacian_NLI_score_entail | 0.7419 | 0.8110 | 0.2236 | 0.2255 |
| 16 | Eccentricity_NLI_score_contra | 0.7419 | 0.8102 | 0.2137 | 0.2258 |
| 17 | CocoaMSP | 0.7407 | 0.8134 | 0.2441 | 0.2431 |
| 18 | SemanticDensity | 0.7377 | 0.8101 | 0.2147 | 0.2196 |
| 19 | MeanTokenEntropy | 0.7330 | 0.8102 | 0.0900 | 0.1745 |
| 20 | LexicalSimilarity_rouge1 | 0.7307 | 0.8109 | 0.1036 | 0.1735 |
| 21 | LexicalSimilarity_rougeL | 0.7285 | 0.8107 | 0.0891 | 0.1699 |
| 22 | LexicalSimilarity_rouge2 | 0.7202 | 0.8098 | 0.0390 | 0.1648 |
| 23 | EigValLaplacian_Jaccard_score | 0.7198 | 0.8095 | 0.1718 | 0.2000 |
| 24 | DegMat_Jaccard_score | 0.7194 | 0.8097 | 0.0420 | 0.1635 |
| 25 | MonteCarloNormalizedSequenceEntropy | 0.7190 | 0.8092 | 0.0202 | 0.1649 |
| 26 | SemanticEntropy | 0.7100 | 0.8099 | 0.1783 | 0.2035 |
| 27 | LexicalSimilarity_BLEU | 0.7089 | 0.8073 | 0.0935 | 0.1759 |
| 28 | Perplexity | 0.7030 | 0.8065 | 0.0947 | 0.1784 |
| 29 | TokenSAR | 0.7013 | 0.8054 | 0.0808 | 0.1764 |
| 30 | Eccentricity_Jaccard_score | 0.6957 | 0.8072 | 0.1155 | 0.1801 |
| 31 | CSL | 0.6931 | 0.8051 | 0.1624 | 0.1997 |
| 32 | MonteCarloSequenceEntropy | 0.6931 | 0.8082 | 0.1700 | 0.2011 |
| 33 | RAUQ (entropy) | 0.6837 | 0.8070 | 0.2105 | 0.2136 |
| 34 | EigenScore | 0.6833 | 0.8056 | 0.1707 | 0.2000 |
| 35 | SentenceSAR | 0.6811 | 0.8061 | 0.0951 | 0.1803 |
| 36 | MaximumSequenceProbability | 0.6796 | 0.8064 | 0.1902 | 0.2114 |
| 37 | CCP | 0.6669 | 0.8038 | 0.1320 | 0.1950 |
| 38 | RAUQ | 0.6561 | 0.8047 | 0.3249 | 0.2815 |
| 39 | SemanticEntropy (Direct) | 0.6061 | 0.7950 | 0.6107 | 0.5757 |
| 40 | MeanPointwiseMutualInformation | 0.5470 | 0.7906 | 0.3276 | 0.2969 |
| 41 | NumSemSets | 0.5276 | 0.7872 | 0.2418 | 0.2437 |
| 42 | AttentionScore (layer=23) | 0.5100 | 0.7877 | 0.3038 | 0.2919 |
| 43 | PTrue | 0.4577 | 0.7819 | 0.1994 | 0.2400 |
| 44 | PTrueSampling | 0.3841 | 0.7768 | 0.3074 | 0.3017 |
| 45 | MeanConditionalPointwiseMutualInformation | 0.3083 | 0.7658 | 0.5070 | 0.4772 |
| 46 | RenyiNeg | 0.2270 | 0.7597 | 0.3805 | 0.3472 |
| 47 | FisherRao | 0.2140 | 0.7587 | 0.5332 | 0.4938 |
