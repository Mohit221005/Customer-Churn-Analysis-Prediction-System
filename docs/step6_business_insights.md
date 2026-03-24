# Step 6 — Business Insights & Retention Actions

This step converts model output into practical churn-reduction decisions and measurable business impact.

---

## 1) Business Questions This Step Answers

1. Which customers are at the highest risk right now?
2. Which intervention should we apply by risk tier?
3. What revenue can we realistically retain from targeted campaigns?
4. How should retention teams prioritize effort and budget?

---

## 2) Implementation Asset

Use: `src/churn/business_insights.py`

Key functions:
- `assign_risk_tiers(...)`
- `risk_summary(...)`
- `retention_playbook(...)`
- `high_risk_customer_extract(...)`
- `intervention_impact_estimate(...)`

---

## 3) Practical Workflow

1. Score customers using your best model (`churn_probability`).
2. Assign risk tiers:
   - High: >= 0.70
   - Medium: 0.40–0.69
   - Low: < 0.40
3. Export high-risk target list for campaign execution.
4. Use playbook matrix to map each risk tier to action/offer/channel.
5. Estimate expected retained revenue before launch.

---

## 4) Action Framework by Segment

### High Risk (urgent)
- Typical profile: month-to-month, low tenure, high monthly charges, low add-on adoption.
- Action: immediate outbound save campaign within 48 hours.
- Offer: contract migration incentive + support/security bundle.

### Medium Risk (preventive)
- Typical profile: moderate probability, mixed tenure, partial add-on use.
- Action: targeted nudges and value communication.
- Offer: limited-time add-on trial or small discount.

### Low Risk (growth/loyalty)
- Typical profile: long tenure, stable contracts, strong product adoption.
- Action: loyalty reinforcement and upsell.
- Offer: bundle upgrades, referral rewards.

---

## 5) KPI Dashboard Recommendations

Track these monthly:

1. **Overall churn rate**
2. **Churn rate by risk tier**
3. **Save rate (30-day, 60-day)**
4. **Campaign conversion rate by channel**
5. **Retained revenue (projected vs actual)**
6. **Cost per saved customer**

---

## 6) Example Business Impact Estimation

If 5,000 high-risk customers are targeted,
- expected save rate = 18%
- avg monthly revenue = $70
- retained months = 6

Projected retained revenue = `5000 * 0.18 * 70 * 6 = $378,000`.

This is a planning estimate that should be compared against actual campaign results.

---

## 7) Deliverables for Portfolio + Interview

1. Risk-tier distribution table
2. Top 200 high-risk customer sample
3. Intervention playbook matrix
4. Revenue impact estimate table
5. 3–5 concrete recommendations for retention leadership

---

## 8) Next Step
Proceed to **Step 7: Power BI Dashboard Guidance** to design the executive dashboard structure, visuals, filters, and drill-through flow.
