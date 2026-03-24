"""Model training and evaluation utilities for Telco churn prediction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.churn.preprocessing import TARGET_COL, build_preprocessor, split_feature_columns


@dataclass
class ModelArtifacts:
    """Container for fitted models and evaluation data."""

    logistic_pipeline: Pipeline
    rf_pipeline: Pipeline
    X_test: pd.DataFrame
    y_test: pd.Series



def prepare_xy(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
    """Split a cleaned DataFrame into features and target."""
    X = df.drop(columns=[TARGET_COL, "customerID"], errors="ignore")
    y = df[TARGET_COL]
    return X, y



def train_models(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> ModelArtifacts:
    """Train Logistic Regression and Random Forest pipelines."""
    X, y = prepare_xy(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state,
    )

    numeric_features, categorical_features = split_feature_columns(df)
    preprocessor = build_preprocessor(numeric_features, categorical_features)

    logistic_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "model",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=random_state,
                ),
            ),
        ]
    )

    rf_pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=400,
                    max_depth=None,
                    min_samples_leaf=2,
                    class_weight="balanced_subsample",
                    random_state=random_state,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    logistic_pipeline.fit(X_train, y_train)
    rf_pipeline.fit(X_train, y_train)

    return ModelArtifacts(
        logistic_pipeline=logistic_pipeline,
        rf_pipeline=rf_pipeline,
        X_test=X_test,
        y_test=y_test,
    )



def evaluate_model(model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, float]:
    """Return core classification metrics."""
    y_pred = model.predict(X_test)
    return {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred, zero_division=0), 4),
        "recall": round(recall_score(y_test, y_pred, zero_division=0), 4),
        "f1": round(f1_score(y_test, y_pred, zero_division=0), 4),
    }



def evaluate_both(artifacts: ModelArtifacts) -> pd.DataFrame:
    """Compare Logistic Regression and Random Forest in one table."""
    log_metrics = evaluate_model(
        artifacts.logistic_pipeline, artifacts.X_test, artifacts.y_test
    )
    rf_metrics = evaluate_model(artifacts.rf_pipeline, artifacts.X_test, artifacts.y_test)

    return pd.DataFrame(
        [
            {"model": "logistic_regression", **log_metrics},
            {"model": "random_forest", **rf_metrics},
        ]
    )



def get_feature_names(preprocessor) -> pd.Index:
    """Extract transformed feature names from fitted preprocessor."""
    names = preprocessor.get_feature_names_out()
    return pd.Index(names)



def logistic_feature_importance(artifacts: ModelArtifacts, top_n: int = 20) -> pd.DataFrame:
    """Return top absolute logistic regression coefficients."""
    pipeline = artifacts.logistic_pipeline
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    feat_names = get_feature_names(preprocessor)
    coefs = pd.Series(model.coef_.ravel(), index=feat_names, name="coefficient")
    out = (
        coefs.abs()
        .sort_values(ascending=False)
        .head(top_n)
        .to_frame("abs_coefficient")
        .join(coefs)
        .reset_index()
        .rename(columns={"index": "feature"})
    )
    return out



def rf_feature_importance(artifacts: ModelArtifacts, top_n: int = 20) -> pd.DataFrame:
    """Return top random forest feature importances."""
    pipeline = artifacts.rf_pipeline
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    feat_names = get_feature_names(preprocessor)
    importances = pd.Series(model.feature_importances_, index=feat_names, name="importance")
    out = (
        importances.sort_values(ascending=False)
        .head(top_n)
        .reset_index()
        .rename(columns={"index": "feature"})
    )
    return out
