# Phase 3 – Final Model & Streamlit Deployment

## Overview

In Phase 3, we finalized our modeling pipeline using **XGBoost Regressor**, tuned hyperparameters, cleaned the final feature set, and deployed the solution via a custom-built **Streamlit application**.

---

## Final Model Summary

After detailed analysis and testing, the XGBoost model was selected due to its consistent performance and generalization ability.

### Model Performance:

```text
XGBoost Regressor Performance:
MAE:  1440.9326968717626
RMSE: 5659.7085882501315
R²:   0.6348780011120024 --> (63% Explainable)
```

> These scores reflect a well-generalized regressor built on composite features derived from raw transactional data.
>
> - In industry settings, such metrics are considered highly acceptable, especially given the absence of advanced behavioral or demographic data.
> - Minor improvements may be possible with richer datasets, but this performance is already competitive and production-grade.

## Streamlit App Features

The app predicts a customer's **12-month CLV** using real-time inputs. It accepts `intuitive inputs` (e.g., total spend, frequency, engagement), **_computes internal composite features_**, and returns the CLV prediction.

---

**App Interface**:  
![Customer LifeTime Value Prediction](<assets/img(5).png>)

**Data Visualisation**:  
![Customer LifeTime Value Prediction](<assets/img(4).png>)

**Wants to Try:**
[Click here to use the deployed app](https://customer-lifetime-value-prediction-model-wwq5m8hwz3vyphgpph6wf.streamlit.app/)

### Key Modules

#### 1. Risk Assessment

Calculates a customer-specific risk score based on:

- Purchase recency
- Return rate
- Engagement level
- Average purchase gap

Flags customers as: `*Low Risk*`, `*Medium Risk*`, `*High Risk*`

> Aids in targeting retention strategies for at-risk customers.

**Customer Status (Risk Assesment)**:  
![Risk Segment](<assets/img(6).jpg>)

---

#### 2. Prediction History

Stores past predictions locally during session and provides:

- CLV trendline
- Summary statistics (avg, max, min)
- CSV export option

**History**:  
![History](<assets/img(1).png>)

---

### Deployment Ready

- Fully interactive dashboard built with **Streamlit**
- Suitable for:
  - CRM integration
  - Sales/marketing operations
  - CLV analytics

> Designed for business users — no technical expertise required.

---
