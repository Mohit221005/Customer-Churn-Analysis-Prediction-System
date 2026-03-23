"""EDA utilities for Telco churn analysis with business-focused outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

TARGET_COL = "Churn"


def ensure_output_dir(path: str | Path) -> Path:
    """Create output directory for EDA artifacts if it does not exist."""
    out = Path(path)
    out.mkdir(parents=True, exist_ok=True)
    return out


def kpi_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Return key churn KPIs as a one-row DataFrame."""
    total_customers = len(df)
    churned_customers = int(df[TARGET_COL].sum())
    churn_rate = churned_customers / total_customers if total_customers else 0.0

    return pd.DataFrame(
        {
            "total_customers": [total_customers],
            "churned_customers": [churned_customers],
            "churn_rate": [round(churn_rate, 4)],
        }
    )


def churn_rate_by_segment(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Compute segment-level churn rates and customer counts."""
    grouped = (
        df.groupby(column, dropna=False)[TARGET_COL]
        .agg(churn_rate="mean", customers="count", churned="sum")
        .reset_index()
        .sort_values(["churn_rate", "customers"], ascending=[False, False])
    )
    grouped["churn_rate"] = grouped["churn_rate"].round(4)
    return grouped


def save_segment_tables(
    df: pd.DataFrame,
    columns: Iterable[str],
    out_dir: str | Path,
) -> None:
    """Export segment-level churn tables as CSV for BI/SQL parity."""
    out = ensure_output_dir(out_dir)
    for col in columns:
        table = churn_rate_by_segment(df, col)
        table.to_csv(out / f"segment_{col}.csv", index=False)


def plot_churn_rate_bar(
    df: pd.DataFrame,
    column: str,
    out_path: str | Path,
    title: str | None = None,
) -> None:
    """Plot churn rate bar chart for a categorical segment."""
    plot_df = churn_rate_by_segment(df, column)

    plt.figure(figsize=(9, 5))
    sns.barplot(data=plot_df, x=column, y="churn_rate")
    plt.title(title or f"Churn Rate by {column}")
    plt.ylabel("Churn Rate")
    plt.xlabel(column)
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()


def plot_monthly_charges_by_churn(df: pd.DataFrame, out_path: str | Path) -> None:
    """Plot distribution of monthly charges by churn status."""
    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df, x=TARGET_COL, y="MonthlyCharges")
    plt.title("Monthly Charges by Churn")
    plt.xlabel("Churn (0=No, 1=Yes)")
    plt.ylabel("Monthly Charges")
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()


def plot_numeric_correlation_heatmap(
    df: pd.DataFrame,
    numeric_columns: Iterable[str],
    out_path: str | Path,
) -> None:
    """Plot correlation heatmap for selected numeric columns."""
    corr = df[list(numeric_columns)].corr(numeric_only=True)
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, cmap="Blues", fmt=".2f")
    plt.title("Numeric Feature Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()


def generate_eda_artifacts(df: pd.DataFrame, out_dir: str | Path = "artifacts/eda") -> None:
    """Generate all core EDA outputs for the churn project."""
    out = ensure_output_dir(out_dir)

    # KPI export
    kpi_summary(df).to_csv(out / "kpi_summary.csv", index=False)

    # Segment tables
    segment_cols = [
        "Contract",
        "TenureGroup",
        "InternetService",
        "PaymentMethod",
        "TechSupport",
        "OnlineSecurity",
    ]
    save_segment_tables(df, segment_cols, out)

    # Visuals
    plot_churn_rate_bar(df, "Contract", out / "churn_rate_by_contract.png")
    plot_churn_rate_bar(df, "TenureGroup", out / "churn_rate_by_tenure_group.png")
    plot_churn_rate_bar(df, "PaymentMethod", out / "churn_rate_by_payment_method.png")
    plot_monthly_charges_by_churn(df, out / "monthly_charges_by_churn.png")

    numeric_cols = [
        "tenure",
        "MonthlyCharges",
        "TotalCharges",
        "AvgChargePerMonth",
        "NumAddOnServices",
        TARGET_COL,
    ]
    plot_numeric_correlation_heatmap(df, numeric_cols, out / "numeric_correlation_heatmap.png")
