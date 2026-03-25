# Interview Script

## 60-90 Second Project Summary

"This project is an end-to-end customer churn analysis and prediction system built around telco customer data. I started by cleaning and standardizing the raw dataset, then engineered business-friendly features such as tenure bands, average charge per month, and number of add-on services. After that, I performed exploratory analysis to identify the main churn drivers, including contract type, tenure, pricing patterns, payment behavior, and support-service usage.

From there, I wrote SQL queries for executive churn KPIs and segment-level reporting, then trained Logistic Regression and Random Forest models to estimate churn risk. I evaluated both models using accuracy, precision, recall, and F1-score, with special attention to recall because missing churners is costly in a retention setting. Finally, I translated the model output into business actions by assigning risk tiers, defining retention playbooks, estimating retained revenue, and designing a Power BI dashboard structure for leadership and operations teams." 

## If They Ask: Why This Project?

"I chose churn because it is a strong business problem where analytics can directly influence revenue retention. It also lets me demonstrate a full workflow: data cleaning, EDA, SQL, machine learning, and business communication in one project."

## If They Ask: What Was the Most Important Data Cleaning Decision?

"One important decision was handling `TotalCharges`. In telco churn data, blank values often appear for brand-new customers with zero tenure. Instead of dropping those rows, I converted the column to numeric and filled those specific cases with 0.0, because that better reflects the business reality and preserves useful records."

## If They Ask: What Features Did You Engineer?

"I created `AvgChargePerMonth` to capture a customer's spend pace over time, `TenureGroup` to segment customers by lifecycle stage, and `NumAddOnServices` as a simple stickiness indicator. These features improved both interpretability and business usefulness."

## If They Ask: Why Use Logistic Regression and Random Forest?

"I wanted one interpretable baseline and one stronger nonlinear benchmark. Logistic Regression is easy to explain to stakeholders because coefficients show directional influence. Random Forest is useful for capturing more complex relationships and gives a second view of feature importance."

## If They Ask: Which Metric Matters Most?

"For churn, recall is especially important because false negatives mean we miss customers who are likely to leave. In many business settings, it is better to review a few extra customers than to miss high-risk customers entirely, so recall and F1 matter more than accuracy alone."

## If They Ask: How Did You Make It Actionable?

"I did not stop at model scores. I converted churn probabilities into High, Medium, and Low risk tiers, created a retention playbook for each tier, extracted high-risk customers for campaign targeting, and added a revenue impact estimate based on expected save rate and retained months."

## If They Ask: What Would You Improve Next?

"The next improvements would be calibrating probability thresholds based on campaign budget, saving trained model artifacts, adding a reproducible environment file, and connecting the scoring output directly to a Power BI dashboard or operational retention workflow."

## If They Ask: What Makes This More Than a Student Project?

"The project is structured like a real analytics workflow. The Python code is modular, the SQL layer mirrors business reporting needs, the modeling step includes explainability, and the final output includes risk segmentation and dashboard guidance for real stakeholders."

## Closing Line

"What I like most about this project is that it connects technical analysis to business action. It shows not only how to predict churn, but how to prioritize customers, support retention campaigns, and communicate results to decision-makers."
