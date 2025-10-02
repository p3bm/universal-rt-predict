# AutoML Leaderboard

| Best model   | name                                                                                                               | model_type     | metric_type   |   metric_value |   train_time |
|:-------------|:-------------------------------------------------------------------------------------------------------------------|:---------------|:--------------|---------------:|-------------:|
|              | [1_Default_LightGBM](1_Default_LightGBM/README.md)                                                                 | LightGBM       | rmse          |      0.0555727 |      1203.66 |
|              | [2_Default_CatBoost](2_Default_CatBoost/README.md)                                                                 | CatBoost       | rmse          |      0.0543588 |       345.96 |
|              | [3_Default_NeuralNetwork](3_Default_NeuralNetwork/README.md)                                                       | Neural Network | rmse          |      0.0861957 |        35.07 |
|              | [2_Default_CatBoost_GoldenFeatures](2_Default_CatBoost_GoldenFeatures/README.md)                                   | CatBoost       | rmse          |      0.0542655 |       764.17 |
|              | [1_Default_LightGBM_GoldenFeatures](1_Default_LightGBM_GoldenFeatures/README.md)                                   | LightGBM       | rmse          |      0.0551621 |      1248.19 |
|              | [3_Default_NeuralNetwork_GoldenFeatures](3_Default_NeuralNetwork_GoldenFeatures/README.md)                         | Neural Network | rmse          |      0.215597  |        33.79 |
|              | [2_Default_CatBoost_GoldenFeatures_RandomFeature](2_Default_CatBoost_GoldenFeatures_RandomFeature/README.md)       | CatBoost       | rmse          |      0.0547595 |       529.61 |
|              | [2_Default_CatBoost_GoldenFeatures_SelectedFeatures](2_Default_CatBoost_GoldenFeatures_SelectedFeatures/README.md) | CatBoost       | rmse          |      0.0695777 |        14.05 |
|              | [1_Default_LightGBM_GoldenFeatures_SelectedFeatures](1_Default_LightGBM_GoldenFeatures_SelectedFeatures/README.md) | LightGBM       | rmse          |      0.0690747 |       215.94 |
|              | [3_Default_NeuralNetwork_SelectedFeatures](3_Default_NeuralNetwork_SelectedFeatures/README.md)                     | Neural Network | rmse          |      0.139971  |         4.31 |
| **the best** | [Ensemble](Ensemble/README.md)                                                                                     | Ensemble       | rmse          |      0.053358  |         0.22 |

### AutoML Performance
![AutoML Performance](ldb_performance.png)

### AutoML Performance Boxplot
![AutoML Performance Boxplot](ldb_performance_boxplot.png)

### Features Importance (Original Scale)
![features importance across models](features_heatmap.png)



### Scaled Features Importance (MinMax per Model)
![scaled features importance across models](features_heatmap_scaled.png)



### Spearman Correlation of Models
![models spearman correlation](correlation_heatmap.png)
