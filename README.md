# Customer Churn Analysis & Prediction System

An end-to-end customer churn project that moves from raw telco customer data to retention-ready business actions. The repository combines Python preprocessing and EDA, SQL KPI analysis, machine learning models, business insight packaging, and Power BI dashboard guidance.

## Project Goal

The goal of this project is to identify churn risk, explain the main drivers behind churn, and translate those findings into practical retention actions that business teams can use.

## What This Project Covers

1. Data understanding and business framing
2. Data cleaning and preprocessing
3. Exploratory data analysis
4. SQL-based churn KPI and segmentation analysis
5. Machine learning modeling with Logistic Regression and Random Forest
6. Business insights and retention playbooks
7. Power BI dashboard blueprint with DAX measures
8. Final portfolio packaging for GitHub, resume, and interviews

## Workflow

### 1. Preprocessing

Core logic lives in `src/churn/preprocessing.py`.

Highlights:
- Standardizes object columns
- Cleans `TotalCharges` with a rule for new customers
- Converts `Churn` from Yes/No to 1/0
- Engineers `AvgChargePerMonth`, `TenureGroup`, and `NumAddOnServices`
- Builds a reusable scikit-learn `ColumnTransformer`

Main functions:
- `run_preprocessing(...)`
- `build_preprocessor(...)`
- `split_feature_columns(...)`

### 2. Exploratory Data Analysis

EDA utilities live in `src/churn/eda.py`.

Highlights:
- KPI summary for total customers, churned customers, and churn rate
- Churn-rate breakdowns by contract, tenure, internet service, payment method, and support features
- Exportable CSV tables and chart artifacts for BI parity

Main functions:
- `kpi_summary(...)`
- `churn_rate_by_segment(...)`
- `generate_eda_artifacts(...)`

### 3. SQL Analysis

Production-style queries live in `sql/churn_analysis.sql`.

Highlights:
- Executive KPI snapshot
- Churn rate by contract and tenure band
- Payment-method and billing-friction analysis
- Add-on protection analysis
- High-risk cohort extraction using business rules
- Segment matrix for dashboard consumption

### 4. Machine Learning

Modeling utilities live in `src/churn/modeling.py`.

Models:
- Logistic Regression with class balancing for interpretability
- Random Forest for nonlinear benchmark performance

Evaluation metrics:
- Accuracy
- Precision
- Recall
- F1-score

Main functions:
- `train_models(...)`
- `evaluate_model(...)`
- `evaluate_both(...)`
- `logistic_feature_importance(...)`
- `rf_feature_importance(...)`

### 5. Business Insights

Retention action logic lives in `src/churn/business_insights.py`.

Highlights:
- Risk tier assignment from churn probability
- Risk summary tables
- Retention playbook mapping
- High-risk customer extraction
- Revenue impact estimation for save campaigns

Main functions:
- `assign_risk_tiers(...)`
- `risk_summary(...)`
- `retention_playbook(...)`
- `high_risk_customer_extract(...)`
- `intervention_impact_estimate(...)`

### 6. Power BI Design

Power BI guidance is documented in:
- `docs/step7_powerbi_dashboard.md`
- `powerbi/dax_measures.md`

The dashboard plan is structured across:
- Executive Overview
- Driver Analysis
- Retention Action Center

## Repository Structure

```text
Customer-Churn-Analysis-Prediction-System/
|-- docs/
|   |-- step1_data_understanding.md
|   |-- step2_data_cleaning_preprocessing.md
|   |-- step3_eda.md
|   |-- step4_sql_analysis.md
|   |-- step5_ml_model.md
|   |-- step6_business_insights.md
|   |-- step7_powerbi_dashboard.md
|   |-- step8_final_output_packaging.md
|   |-- resume_bullets.md
|   `-- interview_script.md
|-- powerbi/
|   `-- dax_measures.md
|-- sql/
|   `-- churn_analysis.sql
|-- src/
|   `-- churn/
|       |-- preprocessing.py
|       |-- eda.py
|       |-- modeling.py
|       `-- business_insights.py
`-- README.md
```

## Suggested Execution Flow

```python
from src.churn.preprocessing import run_preprocessing
from src.churn.eda import generate_eda_artifacts
from src.churn.modeling import train_models, evaluate_both

clean_df, _ = run_preprocessing("data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv")
generate_eda_artifacts(clean_df)

artifacts = train_models(clean_df)
metrics = evaluate_both(artifacts)
print(metrics)
```

After scoring customers with the selected model, use `src/churn/business_insights.py` to assign risk tiers and estimate campaign impact.

## Business Value

This project is designed to answer three practical questions:

1. Which customers are most likely to churn?
2. Why are they churning?
3. What should the business do next to reduce that churn?

The final output is not only a model, but a complete decision workflow that supports analytics, operations, and executive reporting.

## Portfolio Strengths

- Clear end-to-end analytics story from raw data to action
- Reusable Python modules instead of notebook-only analysis
- SQL and BI alignment for dashboard deployment
- Business-facing risk segmentation and intervention planning
- Interview-ready documentation across all project stages

## Supporting Documentation

- `docs/step1_data_understanding.md`
- `docs/step2_data_cleaning_preprocessing.md`
- `docs/step3_eda.md`
- `docs/step4_sql_analysis.md`
- `docs/step5_ml_model.md`
- `docs/step6_business_insights.md`
- `docs/step7_powerbi_dashboard.md`
- `docs/step8_final_output_packaging.md`
- `docs/resume_bullets.md`
- `docs/interview_script.md`

## Next Improvements

- Add a `requirements.txt` or `pyproject.toml` for reproducible setup
- Save trained model artifacts and scored customer outputs
- Add a notebook or script to run the full pipeline end-to-end
- Include sample dashboard screenshots once Power BI pages are built
