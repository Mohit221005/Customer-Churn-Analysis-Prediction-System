# Power BI DAX Measures — Customer Churn Dashboard

Assume table name: `fact_churn_customers`.
Assume `Churn` is encoded as `1/0` and optional `churn_probability` is available.

```DAX
Total Customers =
COUNTROWS(fact_churn_customers)
```

```DAX
Churned Customers =
CALCULATE(
    COUNTROWS(fact_churn_customers),
    fact_churn_customers[Churn] = 1
)
```

```DAX
Churn Rate % =
DIVIDE([Churned Customers], [Total Customers], 0)
```

```DAX
Avg Monthly Charges =
AVERAGE(fact_churn_customers[MonthlyCharges])
```

```DAX
High Risk Customers =
CALCULATE(
    COUNTROWS(fact_churn_customers),
    fact_churn_customers[churn_probability] >= 0.7
)
```

```DAX
Expected Save Rate =
0.18
```

```DAX
Projected Saved Customers =
[High Risk Customers] * [Expected Save Rate]
```

```DAX
Projected Retained Revenue =
[Projected Saved Customers] * [Avg Monthly Charges] * 6
```

```DAX
Churn Rate by Segment % =
DIVIDE(
    CALCULATE(COUNTROWS(fact_churn_customers), fact_churn_customers[Churn] = 1),
    COUNTROWS(fact_churn_customers),
    0
)
```

```DAX
MoM Churn Rate Change % =
VAR CurrentRate = [Churn Rate %]
VAR PrevRate =
    CALCULATE(
        [Churn Rate %],
        DATEADD(dim_date[Date], -1, MONTH)
    )
RETURN
CurrentRate - PrevRate
```
