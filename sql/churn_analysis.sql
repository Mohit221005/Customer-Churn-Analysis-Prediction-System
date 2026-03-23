-- Step 4: SQL Analysis for Customer Churn
-- Assumes a cleaned table named `customer_churn_clean` with:
--   - Churn encoded as 1/0
--   - Engineered fields from preprocessing: TenureGroup, NumAddOnServices, AvgChargePerMonth

/* ============================================================
   1) Executive KPI Snapshot
   ============================================================ */
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    ROUND(AVG(TotalCharges), 2) AS avg_total_charges
FROM customer_churn_clean;

/* ============================================================
   2) Churn rate by contract (high business impact)
   ============================================================ */
SELECT
    Contract,
    COUNT(*) AS customers,
    SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM customer_churn_clean
GROUP BY Contract
ORDER BY churn_rate_pct DESC, customers DESC;

/* ============================================================
   3) Lifecycle churn by tenure band
   ============================================================ */
SELECT
    TenureGroup,
    COUNT(*) AS customers,
    SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM customer_churn_clean
GROUP BY TenureGroup
ORDER BY churn_rate_pct DESC, customers DESC;

/* ============================================================
   4) Payment + billing friction analysis (multi-dimensional)
   ============================================================ */
SELECT
    PaymentMethod,
    PaperlessBilling,
    COUNT(*) AS customers,
    SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges
FROM customer_churn_clean
GROUP BY PaymentMethod, PaperlessBilling
HAVING COUNT(*) >= 30
ORDER BY churn_rate_pct DESC, customers DESC;

/* ============================================================
   5) Service add-on effect (retention protectors)
   ============================================================ */
SELECT
    TechSupport,
    OnlineSecurity,
    DeviceProtection,
    COUNT(*) AS customers,
    SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct
FROM customer_churn_clean
GROUP BY TechSupport, OnlineSecurity, DeviceProtection
HAVING COUNT(*) >= 20
ORDER BY churn_rate_pct DESC, customers DESC;

/* ============================================================
   6) High-risk customer cohort extraction for retention campaign
   Logic:
     - Month-to-month
     - Early tenure (0-12m)
     - Higher monthly charges than overall average
     - Low add-on count
   ============================================================ */
WITH avg_price AS (
    SELECT AVG(MonthlyCharges) AS overall_avg_monthly FROM customer_churn_clean
)
SELECT
    c.customerID,
    c.Contract,
    c.TenureGroup,
    c.MonthlyCharges,
    c.NumAddOnServices,
    c.PaymentMethod,
    c.TechSupport,
    c.OnlineSecurity
FROM customer_churn_clean c
CROSS JOIN avg_price a
WHERE c.Contract = 'Month-to-month'
  AND c.TenureGroup = '0-12m'
  AND c.MonthlyCharges > a.overall_avg_monthly
  AND c.NumAddOnServices <= 2
ORDER BY c.MonthlyCharges DESC;

/* ============================================================
   7) Segment matrix for executive dashboard
   ============================================================ */
SELECT
    Contract,
    InternetService,
    TenureGroup,
    COUNT(*) AS customers,
    SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    ROUND(AVG(NumAddOnServices), 2) AS avg_addon_services
FROM customer_churn_clean
GROUP BY Contract, InternetService, TenureGroup
HAVING COUNT(*) >= 15
ORDER BY churn_rate_pct DESC, customers DESC;

/* ============================================================
   8) Optional join example with retention offers table
   retention_offers schema example:
     - offer_id
     - contract
     - tenure_group
     - max_price
     - offer_name
   ============================================================ */
SELECT
    c.customerID,
    c.Contract,
    c.TenureGroup,
    c.MonthlyCharges,
    o.offer_name
FROM customer_churn_clean c
JOIN retention_offers o
  ON c.Contract = o.contract
 AND c.TenureGroup = o.tenure_group
 AND c.MonthlyCharges <= o.max_price
WHERE c.Churn = 1;
