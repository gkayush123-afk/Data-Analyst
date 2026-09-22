import pandas as pd
import numpy as np

# 1) Read CSV
df = pd.read_csv(r"c:\Users\amadh\OneDrive\Desktop\Intership\week 3\data.csv")

print("Original shape:", df.shape)
print(df.head())
print(df.isna().sum())

# 2) Clean column names and empty strings
df.columns = [col.strip() for col in df.columns]
df = df.replace(r"^\s*$", np.nan, regex=True)

# 3) Fix mixed date formats like: '2020/12/01', 20201226
def parse_date(x):
    if pd.isna(x):
        return pd.NaT
    s = str(x).strip().replace("'", "")
    # if date is in format YYYYMMDD
    if s.isdigit() and len(s) == 8:
        return pd.to_datetime(s, format="%Y%m%d")
    return pd.to_datetime(s, errors="coerce")

df["Date"] = df["Date"].apply(parse_date)

# 4) Convert numeric columns
df["Duration"] = pd.to_numeric(df["Duration"], errors="coerce")
df["Pulse"] = pd.to_numeric(df["Pulse"], errors="coerce")
df["Maxpulse"] = pd.to_numeric(df["Maxpulse"], errors="coerce")
df["Calories"] = pd.to_numeric(df["Calories"], errors="coerce")

# 5) Remove duplicate rows
df = df.drop_duplicates(subset=["Duration", "Date", "Pulse", "Maxpulse", "Calories"], keep="first")

# 6) Handle missing values
median_pulse = df["Pulse"].median()
median_maxpulse = df["Maxpulse"].median()
median_calories = df["Calories"].median()

df["Pulse"] = df["Pulse"].fillna(median_pulse)
df["Maxpulse"] = df["Maxpulse"].fillna(median_maxpulse)
df["Calories"] = df["Calories"].fillna(median_calories)

# 7) Drop impossible/invalid rows
df = df.dropna(subset=["Date"])
df = df[(df["Duration"] > 0) & (df["Pulse"] > 0) & (df["Maxpulse"] > 0) & (df["Calories"] >= 0)]

# 8) Create new useful columns
df["Calories_per_minute"] = df["Calories"] / df["Duration"]
df["Pulse_difference"] = df["Maxpulse"] - df["Pulse"]
df["Workout_type"] = np.where(df["Duration"] >= 60, "Long", "Short")
df["Date_str"] = df["Date"].dt.strftime("%Y-%m-%d")

# 9) Example filtering
filtered = df[(df["Calories_per_minute"] > 4) & (df["Pulse_difference"] > 15)].copy()

print("\nCleaned data preview:")
print(df.head())
print("\nFiltered data preview:")
print(filtered.head())

print("\nFinal shape:", df.shape)

# 10) Save cleaned file
df.to_csv(r"c:\Users\amadh\OneDrive\Desktop\Intership\week 3\cleaned_data.csv", index=False)

print("\nCleaned CSV saved to: c:\\Users\\amadh\\OneDrive\\Desktop\\Intership\\week 3\\cleaned_data.csv")