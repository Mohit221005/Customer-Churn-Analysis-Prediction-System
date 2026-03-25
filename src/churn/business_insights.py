"""Business insight and action-planning utilities for churn retention."""

from __future__ import annotations

from typing import Dict, List, Tuple

import pandas as pd



def assign_risk_tiers(
    scored_df: pd.DataFrame,
    proba_col: str = "churn_probability",
    high_threshold: float = 0.7,
    medium_threshold: float = 0.4,
) -> pd.DataFrame:
    """Assign High/Medium/Low risk tiers from churn probability."""
    out = scored_df.copy()

    conditions = [
        out[proba_col] >= high_threshold,
        (out[proba_col] >= medium_threshold) & (out[proba_col] < high_threshold),
    ]
    choices = ["High", "Medium"]

    out["risk_tier"] = pd.Series(pd.Categorical(["Low"] * len(out), categories=["Low", "Medium", "High"]))
    out.loc[conditions[0], "risk_tier"] = choices[0]
    out.loc[conditions[1], "risk_tier"] = choices[1]

    return out



def risk_summary(scored_df: pd.DataFrame) -> pd.DataFrame:
    """Summarize customers and expected churners by risk tier."""
    grouped = (
        scored_df.groupby("risk_tier", dropna=False)["churn_probability"]
        .agg(customers="count", avg_churn_probability="mean")
        .reset_index()
    )
    grouped["avg_churn_probability"] = grouped["avg_churn_probability"].round(4)
    grouped["expected_churners"] = (
        grouped["customers"] * grouped["avg_churn_probability"]
    ).round(0).astype(int)
    return grouped.sort_values("avg_churn_probability", ascending=False)



def retention_playbook() -> pd.DataFrame:
    """Static action matrix by risk tier for operations teams."""
    rows = [
        {
            "risk_tier": "High",
            "primary_action": "Immediate retention outreach within 48 hours",
            "offer_strategy": "Contract migration incentive + support bundle",
            "channel": "Outbound call + personalized email",
            "success_kpi": "save_rate_30d",
        },
        {
            "risk_tier": "Medium",
            "primary_action": "Nudge campaign with value education",
            "offer_strategy": "Light discount or add-on trial",
            "channel": "Email + in-app/web banner",
            "success_kpi": "engagement_to_save_conversion",
        },
        {
            "risk_tier": "Low",
            "primary_action": "Loyalty reinforcement",
            "offer_strategy": "Upsell bundle and referral program",
            "channel": "Lifecycle CRM automation",
            "success_kpi": "nps_and_upsell_rate",
        },
    ]
    return pd.DataFrame(rows)



def high_risk_customer_extract(
    scored_df: pd.DataFrame,
    min_probability: float = 0.7,
    top_n: int = 500,
) -> pd.DataFrame:
    """Extract top high-risk customers for immediate campaign execution."""
    cols = [
        "customerID",
        "churn_probability",
        "Contract",
        "TenureGroup",
        "MonthlyCharges",
        "NumAddOnServices",
        "PaymentMethod",
        "TechSupport",
    ]
    existing_cols = [c for c in cols if c in scored_df.columns]

    out = scored_df[scored_df["churn_probability"] >= min_probability].copy()
    out = out.sort_values("churn_probability", ascending=False)
    return out[existing_cols].head(top_n)



def intervention_impact_estimate(
    candidates_df: pd.DataFrame,
    avg_monthly_revenue: float,
    expected_save_rate: float,
    months_retained: int = 6,
) -> Dict[str, float]:
    """
    Estimate retained revenue from intervention.

    retained_revenue = targeted_customers * expected_save_rate * avg_monthly_revenue * months_retained
    """
    targeted_customers = len(candidates_df)
    projected_saved_customers = targeted_customers * expected_save_rate
    retained_revenue = (
        projected_saved_customers * avg_monthly_revenue * months_retained
    )

    return {
        "targeted_customers": float(targeted_customers),
        "expected_save_rate": float(expected_save_rate),
        "projected_saved_customers": round(projected_saved_customers, 2),
        "projected_retained_revenue": round(retained_revenue, 2),
    }
