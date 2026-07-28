import pandas as pd

## LOAD & CLEAN DATASET

df = pd.read_csv("data/telco_churn.csv")


#Finding missing values in the dataset.

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors= "coerce")
# print(df["TotalCharges"].isna().sum())


#Filling missing values in the dataset.

df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"])

# print(df["TotalCharges"].isna().sum())

# Cleaning churn column

df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
# print(df["Churn"].unique())


# print(df.shape)
# print(df.info())
# print(df.head())

## CALCULATING MRR

#Finding the number of active customers in the dataset.

active = df[df["Churn"] == 0]
# print(active.shape)
# print(active["Churn"].unique()) #should show only [0]

# Calculating MRR (Revenue from customers who are currently subscribed and paying, this month)

# print(active.groupby("Contract")["MonthlyCharges"].sum())

# Total MRR and ARR

total_mrr = active["MonthlyCharges"].sum()
total_arr = total_mrr*12
# print(total_mrr, total_arr)

mrr_by_contract = active.groupby("Contract")["MonthlyCharges"].sum().reset_index()
mrr_by_contract.columns = ["Contract", "MRR"]

# print(mrr_by_contract)
mrr_by_contract.to_csv("output/mrr_by_segment.csv", index=False)
## CALCULATING CHURN RATE PER CONTRACT

churn_contract = df.groupby("Contract").agg(
    customers = ("customerID", "count"),
    churned = ("Churn", "sum")
).reset_index()

churn_contract["Churn_rate"] = (churn_contract["churned"] / churn_contract["customers"] * 100).round(2)

# print(churn_contract)

## CALCULATING CHURN RATE PER TENURE_BUCKET

#Creating tenure_bucket function

def tenure_bucket(t):
    if t <= 6:
        return "0-6 mo"
    elif t <= 12:
        return "7-12 mo"
    elif t <= 24:
        return "13-24 mo"
    elif t <= 48:
        return "25-48 mo"
    else:
        return "49+ mo"

df["tenure_bucket"] = df["tenure"].apply(tenure_bucket)

churn_tenure = df.groupby("tenure_bucket").agg(
    customers = ("customerID", "count"),
    churned = ("Churn", "sum")
).reset_index()

churn_tenure["Churn_rate"] = (churn_tenure["churned"] / churn_tenure["customers"] * 100).round(2)

# print(churn_tenure)

## CALCULATING CHURN RATE PER PAYMENT_METHOD

churn_payment = df.groupby("PaymentMethod").agg(
    customers = ("customerID", "count"),
    churned = ("Churn", "sum")
).reset_index()

churn_payment["Churn_rate"] = (churn_payment["churned"]/churn_payment["customers"] *100 ).round(2)

# print(churn_payment)

#tidy/long format

churn_contract = churn_contract.rename(columns={"Contract": "segment_value"})
churn_contract["segment_type"] = "Contract"

churn_tenure = churn_tenure.rename(columns={"tenure_bucket": "segment_value"})
churn_tenure["segment_type"] = "Tenure"

churn_payment = churn_payment.rename(columns={"PaymentMethod": "segment_value"})
churn_payment["segment_type"] = "PaymentMethod"

churn_all = pd.concat([churn_contract, churn_tenure, churn_payment], ignore_index=True)

# print(churn_all)

# churn_all.to_csv("output/churn_by_segment.csv", index= False)


##COMPUTING COHORT RETENTION

def signup_month(tenure_months, ref_year=2026, ref_month=1):
    total_months = ref_year * 12 + (ref_month - 1)  # convert reference date to a single number
    signup_total = total_months - tenure_months       # subtract tenure
    year = signup_total // 12
    month = signup_total % 12 + 1
    return f"{year}-{month:02d}"

df["cohort_month"] = df["tenure"].apply(signup_month)
# print(df[["tenure", "cohort_month"]].head(10)) #Sanity check

cohort_rows = []

for i, (_, row) in enumerate(df.iterrows()):
    # if i % 1000 == 0:
        # print(f"Processing row {i}...")
    
    cohort = row["cohort_month"]
    tenure = row["tenure"]
    churned = row ["Churn"] == 1

    last_active_month = tenure - 1 if churned else tenure

    for m in range(0, tenure + 1):
        retained = 1 if m <= last_active_month else 0
        cohort_rows.append((cohort, m, retained))

# print("Loop done, building DataFrame...")
cohort_df = pd.DataFrame(cohort_rows, columns = ["cohort_month", "months_since_signup", "retained"])

# print(cohort_df.shape)
# print(cohort_df.head(15)) #one row per customer per month-checkpoint

#retention percentage per cohort per month

# Aggregating into retention rates

cohort_summary = (
    cohort_df.groupby(["cohort_month", "months_since_signup"])["retained"].agg(["sum", "count"]).reset_index()
)

cohort_summary = cohort_summary.rename(columns={"sum": "retained_customers", "count": "cohort_size_at_month"})

cohort_summary["retention_pct"] = (cohort_summary["retained_customers"] / cohort_summary["cohort_size_at_month"] * 100).round(1)

# print(cohort_summary[cohort_summary["cohort_month"] == "2025-07"])

cohort_month0_size = cohort_df[cohort_df["months_since_signup"] == 0].groupby("cohort_month")["retained"].count()

valid_cohorts = cohort_month0_size[cohort_month0_size >= 15].index

cohort_summary = cohort_summary[cohort_summary["cohort_month"].isin(valid_cohorts)]

cohort_summary = cohort_summary[cohort_summary["months_since_signup"] <= 24]

# print(cohort_summary.shape)
# print(cohort_summary.head(15))

cohort_summary.to_csv("output/cohort_retention.csv", index=False)

# print(df[df["cohort_month"]=="2020-01"]["tenure"].unique()) #oldest retained customers 


##Calculating LTV

ltv_contract = df.groupby("Contract").agg(
    avg_monthly_charge = ("MonthlyCharges", "mean"),
    churn_rate = ("Churn", "mean")
).reset_index()

ltv_contract["estimated_ltv"] = (ltv_contract["avg_monthly_charge"] / ltv_contract["churn_rate"]).round(2)

# print(ltv_contract)

ltv_payment = df.groupby("PaymentMethod").agg(
    avg_monthly_charge = ("MonthlyCharges", "mean"),
    churn_rate = ("Churn", "mean")
).reset_index()

ltv_payment["estimated_ltv"] = (ltv_payment["avg_monthly_charge"] / ltv_payment["churn_rate"]).round(2)

# print(ltv_payment)

ltv_contract = ltv_contract.rename(columns={"Contract": "segment_value"})
ltv_contract["segment_type"] = "Contract"

ltv_payment = ltv_payment.rename(columns= {"PaymentMethod":"segment_value"})
ltv_payment["segment_type"] = "PaymentMethod"

ltv_all = pd.concat([ltv_contract, ltv_payment], ignore_index=True)
ltv_all = ltv_all[["segment_type", "segment_value", "avg_monthly_charge", "churn_rate", "estimated_ltv"]]
ltv_all.to_csv("output/ltv_by_segment.csv", index=False)

# print(ltv_all)


##SUMMARY

kpis = pd.DataFrame([
    {"metric": "Total MRR", "value": round(total_mrr, 2)},
    {"metric": "Total ARR", "value": round(total_arr, 2)},
    {"metric": "Overall Churn Rate (%)", "value": round(df["Churn"].mean() *100, 2)}
])

kpis.to_csv("output/summary_kpis.csv", index = False)