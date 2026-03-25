# Step 4 — SQL Analysis (Churn KPI + Segmentation)

This step operationalizes churn analysis directly in SQL so stakeholders can monitor churn continuously and run retention campaigns from database outputs.

---

## 1) What This Step Produces

- Executive churn KPIs
- Segment-level churn tables
- High-risk customer extraction query
- Dashboard-ready matrix outputs
- Join pattern for campaign personalization

All production queries are in: `sql/churn_analysis.sql`.

---

## 2) Query-by-Query Explanation

## Query 1: Executive KPI Snapshot
**What it does:** Calculates total customers, churned customers, churn rate %, and average charges in one row.

**Why it matters:** Gives leadership a fast health check of churn performance.

---

## Query 2: Churn by Contract
**What it does:** Groups by `Contract` and computes churn rate per contract type.

**Why it matters:** Contract structure is often the strongest retention lever.

---

## Query 3: Churn by TenureGroup
**What it does:** Computes churn concentration across lifecycle bands.

**Why it matters:** Helps retention teams prioritize early-life churn interventions.

---

## Query 4: Payment Method + Paperless Billing
**What it does:** Uses a two-dimensional `GROUP BY` (`PaymentMethod`, `PaperlessBilling`) and a `HAVING` threshold.

**Why it matters:** Reveals billing-friction segments and avoids noisy low-volume groups.

---

## Query 5: Add-on Service Protection Analysis
**What it does:** Measures churn rates across combinations of `TechSupport`, `OnlineSecurity`, and `DeviceProtection`.

**Why it matters:** Identifies which add-on bundles protect against churn.

---

## Query 6: High-Risk Cohort Extraction (CTE)
**What it does:** Uses a CTE for average monthly price and filters likely high-risk customers (month-to-month, early tenure, above-average charge, low add-ons).

**Why it matters:** Produces an actionable target list for save campaigns.

---

## Query 7: Executive Segment Matrix
**What it does:** Builds a compact matrix by `Contract`, `InternetService`, and `TenureGroup` with churn and revenue signals.

**Why it matters:** Can feed directly into Power BI heatmaps and drill-through views.

---

## Query 8: Join Example with Offers Table
**What it does:** Demonstrates joining churn data to a `retention_offers` table using contract, tenure group, and price criteria.

**Why it matters:** Turns analysis into decision automation for personalized offers.

---

## 3) Performance & Production Notes

1. Add indexes for frequent filters/grouping:
   - `(Contract)`
   - `(TenureGroup)`
   - `(PaymentMethod, PaperlessBilling)`
   - `(Churn)`

2. Materialize a daily table/view for heavy dashboards.

3. Keep `HAVING COUNT(*) >= N` thresholds to avoid unstable small-sample segments.

4. Use consistent churn definition (`Churn = 1`) across SQL, Python, and BI.

---

## 4) Suggested Validation Checks

- Compare SQL churn rate with Python KPI output (should match).
- Confirm row counts before/after preprocessing exports.
- Spot-check top 20 high-risk records from Query 6 with business rules.

---

## 5) Next Step
Proceed to **Step 5: Machine Learning Model** (Logistic Regression + Random Forest), using SQL insights for feature and segment prioritization.
