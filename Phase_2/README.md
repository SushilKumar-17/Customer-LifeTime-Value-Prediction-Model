# Phase 2 – CLV Modeling & Feature Analysis

## Overview

In **Phase 2**, we transitioned from feature engineering to model building using the dataset prepared in Phase 1. This involved deep exploration of feature importance, multiple modeling experiments, and rigorous performance evaluations to finalize a high-performing CLV prediction model.

The process spanned **three core notebooks**, each representing a distinct phase of trial, analysis, and refinement:

- `CLTV_Modeling_1.ipynb`: Initial exploration, linear modeling setup
- `CLTV_Modeling_2.ipynb`: Feature selection, base modeling, tree model evaluation
- `CLTV_Modeling_3.ipynb`: Composite features, tree-based tuning, brute-force search, final model

---

## Dataset Evolution

### 1. **Initial Dataset (From Phase 1)**

**Shape**: ~4251 rows → after dropping NaN CLVs → **~2700 rows**  
**Columns** (select):  
`Customer ID`, `TotalSpend`, `PurchaseFrequency`, `OrderHabit`, `Recency`, `AvgPurchaseGap`, `Tenure`, `Trend`, `Churn`, `ReturnRate`, `CLV`  
→ Refer to `Initial_dataset.csv` for full details.

---

### 2. **Transformed Dataset**

Created during linear model preparation with:

- Log/Box-Cox transformations (e.g., `Log_TotalSpend`, `BC_Recency`)
- Label encodings and quantile binning
- Derived columns like `SpendPerOrder`, `SpendRate`, `GapPerOrder`, etc.

→ Designed specifically for `LinearRegression` testing.  
→ Refer to `Transformed_data.csv` for full list of ~30 engineered features.

---

### 3. **Final Dataset (Used for Final Modeling)**

After empirical testing and modeling, a refined set of features was derived:

- `TotalSpend`, `OrderHabit`, `Tenure`
- `SpendPerOrder`, `SpendRate`
- `EngagementScore`, `ReturnImpact`
- `RecencySpendRatio`, `RecentEngagement`
- `GapEngagement`, `GapHabitScore`
- `CLV` (Target)

→ See `Final_Dataset.csv` for exact structure.

---

## Notebook-wise Modeling Process

### `CLTV_Modeling_1.ipynb` – Initial Exploration & Linear Setup

- Conducted **distribution checks** and **skewness analysis**.
- Applied **log transformations** and **label encoding** to prepare for `LinearRegression`.
- Noticed poor interpretability and performance; dataset and logic became cluttered, so moved to a cleaner notebook for further trials.

> **Key Insight**: Linear models struggled despite preprocessing; transformed features were not yielding significant improvement.

---

### `CLTV_Modeling_2.ipynb` – Feature Selection & Base Models

- Dropped log-transformed columns and re-evaluated models.
- Ran **base regressors**: Linear, Ridge, Lasso, Random Forest, Decision Tree.
- Performed **feature importance ranking** using tree-based models.
- Found **no single subset of features consistently strong**, even after standard selection techniques.

> **Key Insight**: Feature selection techniques (like Recursive-Eliminating-Feature, model-based) were not producing valuable results, suggesting that interactions were non-linear and complex.

---

### 📘 `CLTV_Modeling_3.ipynb` – Tree Models & Custom Feature Refinement

This notebook marked the **turning point** of the modeling process:

- Droped the log_transformed, and label_encoded features,used earlier as tree based model doesnt care about skewness.
- Engineered **composite features** from strong base attributes (e.g., `SpendPerOrder`, `EngagementScore`).
- Initial `DecisionTreeRegressor`: R² ≈ **0.75** → but overfitting confirmed via poor validation.
- Switched to **Random Forest**:
  - Train R²: **~0.53**, Validation R²: **~0.54**
- Tried **XGBoost Regressor**:
  - R²: **0.54**, and consistent across folds.

### Brute-Force Feature Subset Testing

- Abandoned classical feature selection methods due to their linear assumption bias.
- **Custom brute-force approach**:
  - Tested **all combinations** of features (size 3 to 14)
  - Achieved R² scores of **0.90+** in training on certain combinations
  - Validated these combinations with **cross-validation** to avoid overfitting
  - Isolated **one robust feature set** that generalized well

> **Key Insight**: Manual, iterative testing outperformed automated selection.

---

## Final Model

- **Model Used**: `XGBoost Regressor`
- **Selected Features**: Final engineered set from `Final_Dataset.csv`
- **Hyperparameter Tuning**: RandomizedSearchCV with validation strategy
- **Performance**:
  - Train R²: ~0.61
  - Cross-Validation R²: ~0.57 (on 5 folds)

---

## Visual Analysis

To validate interpretability and feature impact:

### 1. **Correlation Heatmap**

![Correlation Heatmap](<assets/img(3).png>)

> Showed multicollinearity between engagement-related metrics and spend-related metrics.

### 2. **SHAP Analysis (Final Model)**

![SHAP Summary Plot](<assets/img(2).png>)

> Validated the impact of features like `SpendRate`, `ReturnImpact`, `GapHabitScore`.

---

## Key Learnings & Efforts

- Explored **multiple modeling approaches**, starting from traditional to ensemble.
- Conducted **extensive feature testing**, both automated and manual.
- Faced and mitigated **overfitting** with cross-validation and tuning.
- Built custom **feature interaction logic** based on business understanding, not just stats.
- Employed **brute-force subset analysis** to uncover hidden patterns not captured by default methods.
- Practiced **model interpretability** via SHAP.

---

## Files in This Phase

| File Name               | Purpose                                          |
| ----------------------- | ------------------------------------------------ |
| `CLTV_Modeling_1.ipynb` | Initial linear model attempts and preprocessing  |
| `CLTV_Modeling_2.ipynb` | Feature selection, base models, tree insights    |
| `CLTV_Modeling_3.ipynb` | Final dataset creation, model tuning, evaluation |
| `Initial_dataset.csv`   | Cleaned raw data from Phase 1                    |
| `Transformed_data.csv`  | Data prepared for linear models                  |
| `Final_Dataset.csv`     | Optimized dataset for final modeling             |
| `assets/`               | Visuals for correlation and SHAP                 |

---

## Next Steps

Proceeding to **Phase 3**, where the final model is packaged, tested on holdout or live data, and integrated for further deployment.
