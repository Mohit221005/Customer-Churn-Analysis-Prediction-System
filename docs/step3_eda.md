# Step 3 — Exploratory Data Analysis (EDA) for Churn Drivers

This step translates cleaned data into clear churn patterns, risk segments, and retention actions.

---

## 1) EDA Objectives

1. Measure overall churn rate and understand class balance.
2. Identify which customer segments churn disproportionately.
3. Quantify pricing, tenure, and add-on behavior differences between churned/non-churned cohorts.
4. Generate business-ready insights that can directly inform retention strategy.

---

## 2) Core EDA Questions (Business-First)

1. Which contract type has the highest churn rate?
2. Is churn concentrated among low-tenure customers?
3. Do monthly charges differ materially between churned and retained customers?
4. Which services (e.g., TechSupport/OnlineSecurity) are associated with lower churn?
5. Which payment methods correlate with elevated churn risk?

---

## 3) Required Visuals (Portfolio-Ready)

1. **KPI cards**
   - Total customers
   - Total churned customers
   - Overall churn rate

2. **Bar chart: churn rate by `Contract`**
   - Business use: reveals impact of contract structure on retention.

3. **Bar chart: churn rate by `TenureGroup`**
   - Business use: lifecycle cohorts for proactive retention campaigns.

4. **Box/violin plot: `MonthlyCharges` by `Churn`**
   - Business use: price-sensitivity signal and billing strategy input.

5. **Bar chart: churn rate by service add-ons**
   - Columns: `OnlineSecurity`, `TechSupport`, `DeviceProtection`.
   - Business use: identify protective products to bundle in save offers.

6. **Heatmap of numeric correlations**
   - Focus: `tenure`, `MonthlyCharges`, `TotalCharges`, `AvgChargePerMonth`, `NumAddOnServices`, `Churn`.
   - Business use: understand interaction strengths before modeling.

7. **Stacked bar: churn by `PaymentMethod` and `PaperlessBilling`**
   - Business use: identify friction-prone billing journeys.

---

## 4) Insight Template (Use This Format)

For every chart, produce:

- **Observation:** What does the data show?
- **Business implication:** Why does this matter commercially?
- **Recommended action:** What should the retention team do next?

Example:

- Observation: Month-to-month customers churn 2-3x more than two-year contract customers.
- Business implication: Contract flexibility likely increases switching behavior.
- Recommended action: Offer tenure-based incentives to migrate eligible high-risk month-to-month customers to longer-term plans.

---

## 5) Analysis Workflow (Python)

Use `src/churn/eda.py` functions in this order:

1. Load cleaned data (from Step 2 workflow).
2. Compute KPI summary.
3. Generate churn-rate tables for segment columns.
4. Save visual artifacts to `artifacts/eda/`.
5. Export key aggregated tables to CSV for SQL/Power BI parity.

---

## 6) Step-3 Deliverables

1. `src/churn/eda.py` plotting and summary utilities.
2. `artifacts/eda/*.png` chart outputs.
3. `artifacts/eda/*.csv` segment-level churn tables.
4. `docs/eda_business_insights.md` (top findings + actions).

---

## 7) What “Good” Looks Like in Interviews

A strong EDA story should clearly connect:

- **Who churns** (segments/cohorts),
- **Why likely churn happens** (pricing/support/tenure patterns),
- **What action to take** (targeted offers, support bundles, billing improvements),
- **What business KPI will improve** (reduced churn, improved LTV, reduced save-cost).

---

## 8) Next Step
Proceed to **Step 4: SQL Analysis**, where you will compute churn KPIs, segment-level metrics, and executive summary tables directly in SQL.
