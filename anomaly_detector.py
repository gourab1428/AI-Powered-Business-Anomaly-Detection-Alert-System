import pandas as pd

# Read Excel file
df = pd.read_excel("Dataset.xlsx")

# Display first 5 rows
print(df)

# heloo
# Dynamic handle for column naming ('Conversion' vs 'Conversion Rate')
conv_col = "Conversion" if "Conversion" in df.columns else "Conversion Rate"

# Calculate percentage change for metric printouts
df["Revenue_Change"] = df["Revenue"].pct_change() * 100
df["Orders_Change"] = df["Orders"].pct_change() * 100
df["Traffic_Change"] = df["Traffic"].pct_change() * 100
df["Conversion_Change"] = df[conv_col].pct_change() * 100
df["Cost_Change"] = df["Cost"].pct_change() * 100
df["Refunds_Change"] = df["Refunds"].pct_change() * 100

# Detect anomalies: ONLY when Conversion is less than 3.0
df["Anomaly"] = df[conv_col] < 3.0

anomalies = df[df["Anomaly"] == True]

# 1. First print the table/list of anomaly dates
print("\n🚨 Detected Anomalies:")
print(anomalies)

# 2. Then print the detailed logs for each anomaly
for index, row in anomalies.iterrows():

    print("\n🚨 ANOMALY DETECTED")
    print("Date:", row["Date"])
    print(f"Conversion Rate dropped to {row[conv_col]} (Change: {row['Conversion_Change']:.2f}%)")
    print(f"Revenue changed by {row['Revenue_Change']:.2f}%")
    print(f"Orders changed by {row['Orders_Change']:.2f}%")
    print(f"Traffic changed by {row['Traffic_Change']:.2f}%")
    print(f"Cost changed by {row['Cost_Change']:.2f}%")
    print(f"Refunds changed by {row['Refunds_Change']:.2f}%")