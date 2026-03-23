# Step 2 — Data Cleaning & Preprocessing (Production-Oriented)

This step converts raw Telco churn data into a modeling-ready dataset with consistent types, validated categories, and reproducible transformations.

---

## 1) Preprocessing Goals

1. Standardize data types and fix ingestion anomalies.
2. Handle missing values using business rules (not blind imputation).
3. Encode categorical features with an approach compatible with ML pipelines.
4. Add feature engineering that improves signal and interpretability.
5. Package all transformations into reusable, leakage-safe artifacts.

---

## 2) Recommended Folder Structure

```text
project/
  data/
    raw/
      WA_Fn-UseC_-Telco-Customer-Churn.csv
    processed/
      churn_clean.parquet
  src/
    churn/
      preprocessing.py
  notebooks/
    02_data_cleaning_preprocessing.ipynb
```

---

## 3) End-to-End Cleaning Pipeline (Pandas + scikit-learn)

```python
import pandas as pd
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Dict

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer


TARGET_COL = "Churn"
ID_COL = "customerID"

BINARY_MAP = {"Yes": 1, "No": 0}


def load_data(path: str) -> pd.DataFrame:
    """Load raw CSV with safe defaults."""
    return pd.read_csv(path)


def basic_standardization(df: pd.DataFrame) -> pd.DataFrame:
    """Trim strings and normalize known whitespace issues."""
    out = df.copy()
    obj_cols = out.select_dtypes(include="object").columns
    for col in obj_cols:
        out[col] = out[col].astype(str).str.strip()
    return out


def clean_total_charges(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert TotalCharges to numeric.
    Business rule: blank TotalCharges for tenure==0 is valid early lifecycle state.
    """
    out = df.copy()
    out["TotalCharges"] = pd.to_numeric(out["TotalCharges"], errors="coerce")

    # Optional explicit rule-based fill for new customers
    mask_new = (out["tenure"] == 0) & (out["TotalCharges"].isna())
    out.loc[mask_new, "TotalCharges"] = 0.0
    return out


def normalize_target(df: pd.DataFrame) -> pd.DataFrame:
    """Map churn target to 1/0."""
    out = df.copy()
    out[TARGET_COL] = out[TARGET_COL].map(BINARY_MAP)
    return out


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create explainable business features."""
    out = df.copy()

    # Average revenue per month (lifetime value pace)
    out["AvgChargePerMonth"] = np.where(
        out["tenure"] > 0,
        out["TotalCharges"] / out["tenure"],
        out["MonthlyCharges"],
    )

    # Tenure bands for business segmentation
    out["TenureGroup"] = pd.cut(
        out["tenure"],
        bins=[-1, 12, 24, 48, 72],
        labels=["0-12m", "13-24m", "25-48m", "49-72m"],
    )

    # Service count as a simple product stickiness proxy
    service_cols = [
        "PhoneService", "MultipleLines", "OnlineSecurity", "OnlineBackup",
        "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"
    ]

    # Count only active service flags
    for c in service_cols:
        out[c] = out[c].replace({"No internet service": "No", "No phone service": "No"})

    out["NumAddOnServices"] = (out[service_cols] == "Yes").sum(axis=1)

    return out


def split_columns(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """Define feature column groups for preprocessing."""
    numeric_features = [
        "SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges",
        "AvgChargePerMonth", "NumAddOnServices"
    ]

    categorical_features = [
        c for c in df.columns
        if c not in numeric_features + [TARGET_COL, ID_COL]
    ]

    return numeric_features, categorical_features


def build_preprocessor(numeric_features: List[str], categorical_features: List[str]) -> ColumnTransformer:
    """Build leakage-safe preprocessing transformer."""
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ],
        remainder="drop",
    )

    return preprocessor


def preprocessing_workflow(path: str) -> Tuple[pd.DataFrame, ColumnTransformer]:
    """Main workflow to create clean feature table and sklearn preprocessor."""
    df = load_data(path)
    df = basic_standardization(df)
    df = clean_total_charges(df)
    df = normalize_target(df)
    df = add_features(df)

    numeric_features, categorical_features = split_columns(df)
    preprocessor = build_preprocessor(numeric_features, categorical_features)

    return df, preprocessor
```

---

## 4) Why These Decisions Are Production-Grade

### A) `TotalCharges` handling is rule-based
- Blank values are often concentrated at `tenure = 0` and are expected for brand-new customers.
- Setting those records to `0.0` preserves business reality better than dropping rows.

### B) Categorical semantics are preserved before modeling
- Values like `No internet service` can be meaningfully collapsed to `No` for service-count features.
- For core model encoding, one-hot with `handle_unknown='ignore'` prevents runtime failures when new categories appear.

### C) Leakage prevention by design
- `customerID` is excluded from modeling features.
- Preprocessing is encapsulated in a scikit-learn `ColumnTransformer` for train/test consistency.

### D) Explainable feature engineering
- `AvgChargePerMonth`: identifies customers whose spend profile changes over lifecycle.
- `TenureGroup`: enables retention teams to target lifecycle cohorts.
- `NumAddOnServices`: approximates product stickiness and relationship depth.

---

## 5) Data Validation Checklist (Run Before EDA/Modeling)

1. Confirm unique key integrity: `customerID` should be unique.
2. Verify target integrity: `Churn` should only contain `0/1` after mapping.
3. Check nulls after cleaning (especially `TotalCharges`).
4. Validate category domains for major columns (`Contract`, `InternetService`, `PaymentMethod`).
5. Track class ratio for churned vs non-churned customers.

---

## 6) SQL-Friendly Output Strategy

To keep SQL + Python aligned:
- Save cleaned data to parquet or a SQL staging table.
- Keep engineered features (`TenureGroup`, `NumAddOnServices`) materialized for BI and model explainability.
- Maintain a data dictionary version in docs so business and analytics definitions remain consistent.

---

## 7) Step-2 Deliverables (Portfolio Standard)

1. Reproducible preprocessing script (`src/churn/preprocessing.py`).
2. Cleaned dataset artifact (`data/processed/churn_clean.parquet`).
3. QA report (row counts, null summary, category summary, churn ratio).
4. Preprocessing assumptions log (especially treatment of `TotalCharges`).

---

## 8) Next Step
Proceed to **Step 3: Exploratory Data Analysis (EDA)** to quantify churn drivers by contract type, tenure bands, pricing, support add-ons, and payment behavior.
