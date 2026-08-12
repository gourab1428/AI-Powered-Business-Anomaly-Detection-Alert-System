import pandas as pd

# ============================================================
# CONFIG: threshold for "unusual" percentage change
# ============================================================
THRESHOLD = 30  # ±30% change is considered "unusual"

# ============================================================
# CONFIG: business direction rules for each metric
# ------------------------------------------------------------
# "good_up"   -> increase = Positive, decrease = Negative/Suspicious
#                (Revenue, Orders, Conversion)
# "bad_up"    -> increase = Negative/Suspicious, decrease = Positive
#                (Cost, Refunds)
# "neutral"   -> big change in either direction = Neutral/Unusual
#                (Traffic)
# ============================================================
METRIC_RULES = {
    "Revenue": "good_up",
    "Orders": "good_up",
    "Traffic": "neutral",
    "Conversion": "good_up",
    "Cost": "bad_up",
    "Refunds": "bad_up",
}


def classify_metric(metric_name, pct_change, threshold=THRESHOLD):
    """
    Decide the status of a single metric's change based on:
    1. Whether the change is big enough to matter (threshold)
    2. Whether an increase is normally good, bad, or doesn't matter
       for that particular metric (METRIC_RULES)
    Returns a simple text label.
    """
    # If there's no previous row to compare to, pct_change will be NaN
    if pd.isna(pct_change):
        return "Normal"

    # Small changes are just normal day-to-day movement
    if abs(pct_change) < threshold:
        return "Normal"

    rule = METRIC_RULES[metric_name]

    if rule == "neutral":
        # Big move, but we don't judge Traffic as good or bad
        return "Neutral/Unusual"

    if rule == "good_up":
        # Going up is good, going down is suspicious
        return "Positive" if pct_change > 0 else "Negative/Suspicious"

    if rule == "bad_up":
        # Going up is suspicious, going down is good
        return "Negative/Suspicious" if pct_change > 0 else "Positive"

    return "Normal"  # fallback, should not happen


# ============================================================
# Read Excel file
# ============================================================
df = pd.read_excel("Dataset.xlsx")

# Display first 5 rows
print(df)

# Dynamic handle for column naming ('Conversion' vs 'Conversion Rate')
conv_col = "Conversion" if "Conversion" in df.columns else "Conversion Rate"

# Map our internal metric name "Conversion" to the real column name in the sheet
COLUMN_MAP = {
    "Revenue": "Revenue",
    "Orders": "Orders",
    "Traffic": "Traffic",
    "Conversion": conv_col,
    "Cost": "Cost",
    "Refunds": "Refunds",
}

# ============================================================
# Calculate percentage change for every metric (same as before)
# ============================================================
df["Revenue_Change"] = df["Revenue"].pct_change() * 100
df["Orders_Change"] = df["Orders"].pct_change() * 100
df["Traffic_Change"] = df["Traffic"].pct_change() * 100
df["Conversion_Change"] = df[conv_col].pct_change() * 100
df["Cost_Change"] = df["Cost"].pct_change() * 100
df["Refunds_Change"] = df["Refunds"].pct_change() * 100

CHANGE_COL_MAP = {
    "Revenue": "Revenue_Change",
    "Orders": "Orders_Change",
    "Traffic": "Traffic_Change",
    "Conversion": "Conversion_Change",
    "Cost": "Cost_Change",
    "Refunds": "Refunds_Change",
}

# ============================================================
# NEW LOGIC: classify EVERY metric, for EVERY row
# Instead of one "Anomaly" True/False column based only on
# Conversion Rate, we now build one status column per metric.
# ============================================================
for metric_name in METRIC_RULES:
    change_col = CHANGE_COL_MAP[metric_name]
    status_col = f"{metric_name}_Status"
    df[status_col] = df[change_col].apply(lambda pct: classify_metric(metric_name, pct))

# A row is an overall "Business Issue" if ANY metric is Negative/Suspicious
status_cols = [f"{m}_Status" for m in METRIC_RULES]
df["Overall_Alert"] = df[status_cols].apply(
    lambda row: any(status == "Negative/Suspicious" for status in row), axis=1
)

anomalies = df[df["Overall_Alert"] == True]

# ============================================================
# 1. Print the table/list of anomaly dates (same style as before)
# ============================================================
print("\n🚨 Detected Anomalies:")
print(anomalies[["Date"] + status_cols])

# ============================================================
# 2. Print detailed, metric-by-metric logs for each flagged row
# ============================================================
for index, row in anomalies.iterrows():

    print("\n" + "=" * 50)
    print("Date:", row["Date"])
    print("=" * 50)

    # Which metrics caused this row to be flagged
    triggered_metrics = [
        m for m in METRIC_RULES if row[f"{m}_Status"] == "Negative/Suspicious"
    ]

    for metric_name in METRIC_RULES:
        real_col = COLUMN_MAP[metric_name]
        change_col = CHANGE_COL_MAP[metric_name]
        status_col = f"{metric_name}_Status"

        value = row[real_col]
        change = row[change_col]
        status = row[status_col]

        change_str = "N/A" if pd.isna(change) else f"{change:+.2f}%"
        print(f"{metric_name:<12} -> Value: {value:<10} Change: {change_str:<10} Status: {status}")

    print("-" * 50)
    if triggered_metrics:
        print("🚨 Business Issue Detected")
        print("Caused by:", ", ".join(triggered_metrics))
    else:
        print("✅ No suspicious metrics (should not happen in this loop)")