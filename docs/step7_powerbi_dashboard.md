# Step 7 — Power BI Dashboard Guidance (Executive + Operational)

This step defines the exact dashboard layout, KPIs, visuals, filters, and navigation so churn insights become decision-ready for business teams.

---

## 1) Dashboard Structure (3 Pages)

## Page 1 — Executive Overview
**Goal:** give leadership a 30-second churn health snapshot.

### Top KPI cards
1. Total Customers
2. Churned Customers
3. Churn Rate %
4. Avg Monthly Charges
5. Projected Retained Revenue (from intervention plan)

### Main visuals
1. **Line chart:** monthly churn trend
2. **Bar chart:** churn rate by Contract
3. **Bar chart:** churn rate by TenureGroup
4. **Donut chart:** churn distribution by InternetService

### Recommended slicers
- Month/Year
- Contract
- TenureGroup
- InternetService

---

## Page 2 — Driver Analysis
**Goal:** explain *why* churn is happening.

### Visuals
1. **Heatmap / matrix:** churn rate by PaymentMethod x PaperlessBilling
2. **Clustered bar:** churn rate by TechSupport / OnlineSecurity / DeviceProtection
3. **Box plot equivalent** (custom visual) or column chart bins: MonthlyCharges by churn status
4. **Scatter plot:** AvgChargePerMonth vs churn probability (if scored data is available)

### Slicers
- Churn (Yes/No)
- SeniorCitizen
- Partner
- Dependents
- PaymentMethod

---

## Page 3 — Retention Action Center
**Goal:** enable operations to act.

### Visuals
1. **Table:** top high-risk customers (customerID, churn probability, contract, tenure, monthly charges)
2. **Stacked bar:** risk tier distribution (High / Medium / Low)
3. **Matrix:** recommended action by risk tier (playbook)
4. **KPI cards:** expected save rate, projected saved customers, projected retained revenue

### Slicers
- Risk tier
- Campaign type
- Region (if available)
- PaymentMethod

### Drill-through
- From high-risk table -> Customer Profile page (optional page 4)
  - show services, charges, tenure, support status, last intervention

---

## 2) Data Model (Recommended)

Tables:
1. `fact_churn_customers` (grain: customer-month or current customer snapshot)
2. `dim_date`
3. `dim_contract`
4. `dim_services`
5. `fact_campaign_results` (optional for closed-loop KPI tracking)

Relationships:
- `fact_churn_customers[date_key]` -> `dim_date[date_key]`
- `fact_churn_customers[contract_key]` -> `dim_contract[contract_key]`
- `fact_churn_customers[service_key]` -> `dim_services[service_key]`

---

## 3) DAX Measures (Core)

Use `powerbi/dax_measures.md` for ready-to-copy measures, including:
- `Total Customers`
- `Churned Customers`
- `Churn Rate %`
- `Avg Monthly Charges`
- `High Risk Customers`
- `Projected Saved Customers`
- `Projected Retained Revenue`

---

## 4) Design Standards (Portfolio Quality)

1. Keep one visual answer per chart (avoid overloaded visuals).
2. Use a consistent color language:
   - High risk/churn: red
   - Medium risk: amber
   - Low risk/retained: green
3. Add dynamic titles (respect slicers).
4. Add tooltip pages for segment context (customers, churn rate, avg charges).
5. Limit each page to 6–8 visuals for readability.

---

## 5) Storytelling Sequence for Demos/Interviews

1. Start Page 1: “Here is overall churn health and trend.”
2. Move to Page 2: “These are the strongest churn drivers and risky behaviors.”
3. Move to Page 3: “These customers should be targeted now, and here’s expected business impact.”

This sequence demonstrates analytics maturity from **descriptive -> diagnostic -> prescriptive**.

---

## 6) Next Step
Proceed to **Step 8: Final Output Packaging** (README, resume bullets, interview narrative).
