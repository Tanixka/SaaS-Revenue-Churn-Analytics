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

churn_all.to_csv("output/churn_by_segment.csv", index= False)