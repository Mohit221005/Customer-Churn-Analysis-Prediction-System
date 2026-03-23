"""Reusable preprocessing pipeline for Telco customer churn modeling."""

from __future__ import annotations

from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

TARGET_COL = "Churn"
ID_COL = "customerID"
BINARY_MAP = {"Yes": 1, "No": 0}



def load_data(path: str) -> pd.DataFrame:
    """Load raw dataset from CSV."""
    return pd.read_csv(path)



def basic_standardization(df: pd.DataFrame) -> pd.DataFrame:
    """Trim leading/trailing whitespace for object columns."""
    out = df.copy()
    obj_cols = out.select_dtypes(include="object").columns
    for col in obj_cols:
        out[col] = out[col].astype(str).str.strip()
    return out



def clean_total_charges(df: pd.DataFrame) -> pd.DataFrame:
    """Convert TotalCharges to numeric and fill valid new-customer blanks."""
    out = df.copy()
    out["TotalCharges"] = pd.to_numeric(out["TotalCharges"], errors="coerce")
    mask_new = (out["tenure"] == 0) & (out["TotalCharges"].isna())
    out.loc[mask_new, "TotalCharges"] = 0.0
    return out



def normalize_target(df: pd.DataFrame) -> pd.DataFrame:
    """Map Churn from Yes/No to 1/0."""
    out = df.copy()
    out[TARGET_COL] = out[TARGET_COL].map(BINARY_MAP)
    return out



def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add business-friendly engineered features."""
    out = df.copy()

    out["AvgChargePerMonth"] = np.where(
        out["tenure"] > 0,
        out["TotalCharges"] / out["tenure"],
        out["MonthlyCharges"],
    )

    out["TenureGroup"] = pd.cut(
        out["tenure"],
        bins=[-1, 12, 24, 48, 72],
        labels=["0-12m", "13-24m", "25-48m", "49-72m"],
    )

    service_cols = [
        "PhoneService",
        "MultipleLines",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "StreamingTV",
        "StreamingMovies",
    ]

    for col in service_cols:
        out[col] = out[col].replace(
            {"No internet service": "No", "No phone service": "No"}
        )

    out["NumAddOnServices"] = (out[service_cols] == "Yes").sum(axis=1)

    return out



def split_feature_columns(df: pd.DataFrame) -> Tuple[List[str], List[str]]:
    """Create numeric/categorical feature lists."""
    numeric_features = [
        "SeniorCitizen",
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
        "AvgChargePerMonth",
        "NumAddOnServices",
    ]

    categorical_features = [
        col
        for col in df.columns
        if col not in numeric_features + [TARGET_COL, ID_COL]
    ]

    return numeric_features, categorical_features



def build_preprocessor(
    numeric_features: List[str], categorical_features: List[str]
) -> ColumnTransformer:
    """Build train/test-consistent preprocessing transformer."""
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "onehot",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ],
        remainder="drop",
    )



def run_preprocessing(path: str) -> Tuple[pd.DataFrame, ColumnTransformer]:
    """Execute full preprocessing workflow and return cleaned frame + transformer."""
    df = load_data(path)
    df = basic_standardization(df)
    df = clean_total_charges(df)
    df = normalize_target(df)
    df = add_features(df)
    numeric_features, categorical_features = split_feature_columns(df)
    preprocessor = build_preprocessor(numeric_features, categorical_features)
    return df, preprocessor
