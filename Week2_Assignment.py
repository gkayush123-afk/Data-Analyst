import pandas as pd
import os

# File path
csv_path = r"c:\Users\amadh\OneDrive\Desktop\Intership\week 2\SQL_Sales_Dataset_200_Rows.xlsx - Sheet1.csv"

# Check if file exists
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"File not found: {csv_path}")

# 1) Load CSV using Pandas and display basic info
df = pd.read_csv(csv_path)

print("=== 1. Dataset Head ===")
print(df.head())

print("\n=== 2. Dataset Info ===")
df.info()

print("\n=== 3. Basic Summary ===")
print(df.describe(include="all"))

# 2) Handle missing values and duplicates
print("\n=== 4. Missing values before cleaning ===")
print(df.isnull().sum())

df = df.drop_duplicates()

# Fill numeric missing values with median
numeric_cols = df.select_dtypes(include=["number"]).columns
for col in numeric_cols:
    if df[col].isnull().any():
        df[col] = df[col].fillna(df[col].median())

# Fill categorical missing values with mode
categorical_cols = df.select_dtypes(include=["object"]).columns
for col in categorical_cols:
    if df[col].isnull().any():
        mode_value = df[col].mode()
        if not mode_value.empty:
            df[col] = df[col].fillna(mode_value[0])

print("\n=== 5. Missing values after cleaning ===")
print(df.isnull().sum())
print("Duplicate rows removed:", df.duplicated().sum())

# 3) Group by category and find total revenue
print("\n=== 6. Total Revenue by Category ===")
revenue_by_category = df.groupby("category", as_index=False)["total_price"].sum()
revenue_by_category = revenue_by_category.rename(columns={"total_price": "total_revenue"})
print(revenue_by_category.sort_values(by="total_revenue", ascending=False))

# 4) Sort data by multiple columns
print("\n=== 7. Sorted Data by Region, Category, Total Price ===")
sorted_df = df.sort_values(
    by=["region", "category", "total_price"],
    ascending=[True, True, False]
).reset_index(drop=True)
print(sorted_df.head(10))

# 5) Create correlation matrix for numeric columns
print("\n=== 8. Correlation Matrix ===")
numeric_df = df.select_dtypes(include=["number"])
print(numeric_df.corr())