# Step 1 — Data Understanding (Telco Customer Churn)

## 1) Dataset Objective
The Telco Customer Churn dataset is designed to explain and predict whether a customer will leave (churn) based on demographics, account details, subscription choices, and billing behavior. 

**Business question:** *Which types of customers are most likely to churn, and what levers can the business use to retain them?*

---

## 2) Column-by-Column Business Data Dictionary

### Customer identifier

| Column | Typical type | What it means | Business relevance |
|---|---|---|---|
| `customerID` | string | Unique customer identifier | Primary key for row-level joins and tracking; not predictive by itself |

### Target variable

| Column | Typical type | What it means | Business relevance |
|---|---|---|---|
| `Churn` | categorical (`Yes`/`No`) | Whether customer left the service | Core outcome for retention strategy and ML prediction |

### Demographic variables

| Column | Typical type | What it means | Business relevance |
|---|---|---|---|
| `gender` | categorical | Customer gender | Useful for fairness checks and segment reporting |
| `SeniorCitizen` | binary (`0`/`1`) | Whether customer is a senior citizen | Often linked to support needs and product simplicity |
| `Partner` | categorical (`Yes`/`No`) | Whether customer has a partner | Proxy for household stability and bundle behavior |
| `Dependents` | categorical (`Yes`/`No`) | Whether customer has dependents | Can indicate price sensitivity and service needs |

### Account and tenure variables

| Column | Typical type | What it means | Business relevance |
|---|---|---|---|
| `tenure` | integer (months) | How long customer has been with company | Strong churn driver (early-life churn is common) |
| `Contract` | categorical (`Month-to-month`, `One year`, `Two year`) | Contract type | Key retention lever; shorter contracts usually churn more |
| `PaperlessBilling` | categorical (`Yes`/`No`) | Whether billing is paperless | Operational preference; can correlate with digital behavior |
| `PaymentMethod` | categorical | Method used to pay bills | Failed payments, friction, and churn risk can vary by method |

### Service subscription variables

| Column | Typical type | What it means | Business relevance |
|---|---|---|---|
| `PhoneService` | categorical (`Yes`/`No`) | Whether customer has phone service | Base product adoption |
| `MultipleLines` | categorical (`Yes`/`No`/`No phone service`) | More than one phone line | ARPU and bundle complexity indicator |
| `InternetService` | categorical (`DSL`/`Fiber optic`/`No`) | Type of internet service | Often among strongest churn differentiators |
| `OnlineSecurity` | categorical | Security add-on status | Value-added protection; may reduce churn |
| `OnlineBackup` | categorical | Backup add-on status | Additional lock-in and customer value |
| `DeviceProtection` | categorical | Device protection status | Service value and perceived reliability |
| `TechSupport` | categorical | Tech support add-on status | Critical for reducing frustration-driven churn |
| `StreamingTV` | categorical | TV streaming add-on status | Entertainment bundle behavior |
| `StreamingMovies` | categorical | Movie streaming add-on status | Engagement and upsell signal |

> For several add-on fields, values include `No internet service` when internet is absent. That value carries structural meaning and should not be treated as missing.

### Billing and revenue variables

| Column | Typical type | What it means | Business relevance |
|---|---|---|---|
| `MonthlyCharges` | float | Monthly bill amount | Price sensitivity and perceived value |
| `TotalCharges` | numeric stored as text in many raw files | Lifetime billed amount | Revenue contribution, often tied to tenure |

---

## 3) Expected Data Quality Issues (and why they matter)

1. **`TotalCharges` may contain blanks (`" "`)**  
   - Common when `tenure = 0` for very new customers.  
   - If not cleaned, type conversion fails or introduces hidden nulls.

2. **Mixed categorical semantics**  
   - Values like `No internet service` and `No phone service` are not nulls; they are *state values*.  
   - Replacing them with `No` can remove useful signal.

3. **Target imbalance risk (`Churn`)**  
   - Churn is often minority class.  
   - Accuracy alone can be misleading; business should monitor recall/precision.

4. **Potential multicollinearity**  
   - `tenure` and `TotalCharges` are typically strongly correlated.  
   - This can affect linear model interpretation.

5. **Identifier leakage risk**  
   - `customerID` must never be used as model feature.  
   - It can overfit without business value.

6. **Contract/billing interaction effects**  
   - `Contract`, `PaymentMethod`, and `PaperlessBilling` often interact.  
   - Important to evaluate combinations, not only single columns.

---

## 4) Business Meaning You Should Validate with Stakeholders

Before modeling, confirm these assumptions with product/retention teams:

- **What exactly counts as churn?** (voluntary cancellation, non-payment disconnection, or both)
- **Observation window:** Is churn measured monthly, quarterly, or at contract renewal?
- **Actionability horizon:** How many days/weeks ahead should we predict churn?
- **Retention constraints:** Budget, discount policy, and channels available for intervention.

These clarifications convert a technical churn model into a deployable business decision system.

---

## 5) Step-1 Deliverables (Portfolio Standard)

For your project repository, Step 1 should produce:

1. **Data dictionary table** (as above, with business meaning).  
2. **Data quality checklist** (nulls, invalid categories, type issues).  
3. **Assumptions log** (explicit business definitions and modeling assumptions).  
4. **Initial hypothesis list**, e.g.:  
   - Month-to-month + high monthly charges -> higher churn likelihood  
   - Low-tenure users churn more than long-tenure users  
   - Customers lacking support/security add-ons churn more

---

## 6) Suggested Next Step
Proceed to **Step 2: Data Cleaning & Preprocessing**, where we will:

- Convert `TotalCharges` safely to numeric
- Handle null/blank values with rule-based logic
- Encode categorical variables for modeling
- Build a reusable preprocessing pipeline
