import pandas as pd

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


# print(df.head())
# print(df.shape)
# print(df.info())