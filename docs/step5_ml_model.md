# Step 5 — Machine Learning Model (Logistic Regression + Random Forest)

This step converts the cleaned dataset into predictive models that estimate churn risk and support retention targeting.

---

## 1) Modeling Objectives

1. Build two baseline-but-strong classifiers:
   - Logistic Regression (interpretable baseline)
   - Random Forest (nonlinear benchmark)
2. Evaluate with business-relevant metrics:
   - Accuracy
   - Precision
   - Recall
   - F1-score
3. Explain model behavior with feature importance outputs.

---

## 2) Implementation Assets

Primary implementation file:
- `src/churn/modeling.py`

Key functions:
- `train_models(...)`
- `evaluate_model(...)`
- `evaluate_both(...)`
- `logistic_feature_importance(...)`
- `rf_feature_importance(...)`

---

## 3) Modeling Workflow

1. Run Step-2 preprocessing to create cleaned dataframe.
2. Use `prepare_xy(...)` to split features and target.
3. Perform `train_test_split(..., stratify=y)` to preserve class ratio.
4. Train Logistic Regression + Random Forest pipelines.
5. Compare performance metrics in one summary table.
6. Review top risk drivers from feature-importance outputs.

---

## 4) Why Two Models?

- **Logistic Regression**
  - Pros: interpretable coefficients, faster training, easier stakeholder communication.
  - Use: baseline and policy explainability.

- **Random Forest**
  - Pros: captures non-linear interactions and mixed effects.
  - Use: performance benchmark and robust ranking of risk factors.

---

## 5) Metric Interpretation (Business Lens)

- **Accuracy**: useful overall, but can hide churn misses if classes are imbalanced.
- **Precision**: among customers flagged at-risk, how many actually churn.
- **Recall**: among customers who churn, how many were captured by the model.
- **F1**: balance between precision and recall.

For churn prevention, **recall is usually critical** because missed churners are lost-revenue risk.

---

## 6) Business Deployment Guidance

1. Set a probability threshold aligned with retention budget.
2. Route top-risk decile to save offers/call-center workflows.
3. Monitor monthly drift in churn rate, feature distributions, and model metrics.
4. Retrain quarterly (or monthly if churn dynamics shift quickly).

---

## 7) Suggested Output Artifacts

- `artifacts/modeling/model_metrics.csv`
- `artifacts/modeling/logistic_feature_importance.csv`
- `artifacts/modeling/rf_feature_importance.csv`
- `artifacts/modeling/scoring_sample.csv`

---

## 8) Example Usage Snippet

```python
from src.churn.preprocessing import run_preprocessing
from src.churn.modeling import train_models, evaluate_both, logistic_feature_importance, rf_feature_importance

clean_df, _ = run_preprocessing("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
artifacts = train_models(clean_df)
metrics = evaluate_both(artifacts)
log_imp = logistic_feature_importance(artifacts, top_n=20)
rf_imp = rf_feature_importance(artifacts, top_n=20)

print(metrics)
```

---

## 9) Next Step
Proceed to **Step 6: Business Insights** to transform model outputs into retention actions, risk tiers, and intervention playbooks.
