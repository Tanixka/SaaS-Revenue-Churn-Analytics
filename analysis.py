import pandas as pd

## LOAD & CLEAN DATASET

df = pd.read_csv("data/telco_churn.csv")


#Finding missing values in the dataset.

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors= "coerce")
# print(df["TotalCharges"].isna().sum())


#Filling missing values in the dataset.

df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"])

print(df["TotalCharges"].isna().sum())

# Cleaning churn column

df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
print(df["Churn"].unique())


# print(df.shape)
# print(df.info())
# print(df.head())

## FINDING ACTIVE CUSTOMERS

#Finding the number of active customers in the dataset.

active = df[df["Churn"] == 0]
print(active.shape)
print(active["Churn"].unique()) #should show only [0]

# Calculating MRR (Revenue from customers who are currently subscribed and paying, this month)

print(active.groupby("Contract")["MonthlyCharges"].sum())

# Total MRR and ARR

total_mrr = active["MonthlyCharges"].sum()
total_arr = total_mrr*12
print(total_mrr, total_arr)

mrr_by_contract = active.groupby("Contract")["MonthlyCharges"].sum().reset_index()
mrr_by_contract.columns = ["Contract", "MRR"]

print(mrr_by_contract)