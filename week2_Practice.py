import pandas as pd

# Load dataset
file_path = r"c:\Users\amadh\OneDrive\Desktop\Intership\week 2\SQL_Sales_Dataset_200_Rows.xlsx - Sheet1.csv"
df = pd.read_csv(file_path)

print("=== 1) Dataset head ===")
print(df.head())

print("\n=== 2) Dataset info ===")
df.info()

print("\n=== 3) Missing values before cleaning ===")
print(df.isnull().sum())

# 2) Handle missing values and duplicates
df = df.drop_duplicates()

numeric_cols = df.select_dtypes(include=["number"]).columns
for col in numeric_cols:
    if df[col].isnull().any():
        df[col] = df[col].fillna(df[col].median())

categorical_cols = df.select_dtypes(include=["object"]).columns
for col in categorical_cols:
    if df[col].isnull().any():
        mode_value = df[col].mode()
        if not mode_value.empty:
            df[col] = df[col].fillna(mode_value[0])

print("\n=== 4) Missing values after cleaning ===")
print(df.isnull().sum())

# 3) Group by category and total revenue
print("\n=== 5) Total revenue by category ===")
revenue_by_category = df.groupby("category", as_index=False)["total_price"].sum()
revenue_by_category = revenue_by_category.rename(columns={"total_price": "total_revenue"})
print(revenue_by_category.sort_values(by="total_revenue", ascending=False))

# 4) Sort by multiple columns
print("\n=== 6) Sorted data by region, category, total_price ===")
sorted_df = df.sort_values(
    by=["region", "category", "total_price"],
    ascending=[True, True, False]
).reset_index(drop=True)
print(sorted_df.head(10))

# 5) Correlation matrix for numeric columns
print("\n=== 7) Correlation matrix ===")
numeric_df = df.select_dtypes(include=["number"])
print(numeric_df.corr())