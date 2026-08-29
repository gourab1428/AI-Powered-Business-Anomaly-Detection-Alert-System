
import pandas as pd
import numpy as np
from scipy.stats import zscore
from sklearn.ensemble import IsolationForest
from llm_explainer import generate_ai_summary

# ============================================================
# CONFIG
# ============================================================

Z_THRESHOLD = 3
IQR_MULTIPLIER = 1.5

IF_CONTAMINATION = 0.05
IF_RANDOM_STATE = 42

# Previous-day business rule threshold
THRESHOLD = 30

# ============================================================
# BUSINESS RULES
# ============================================================

METRIC_RULES = {
    "Revenue": "good_up",
    "Orders": "good_up",
    "Traffic": "neutral",
    "Conversion": "good_up",
    "Cost": "bad_up",
    "Refunds": "bad_up",
}


# ============================================================
# FUNCTION: BUSINESS RULE CLASSIFICATION
# ============================================================

def classify_metric(metric_name, pct_change, threshold=THRESHOLD):

    if pd.isna(pct_change):
        return "Normal"

    if abs(pct_change) < threshold:
        return "Normal"

    rule = METRIC_RULES[metric_name]

    if rule == "neutral":
        return "Neutral/Unusual"

    if rule == "good_up":
        return (
            "Positive"
            if pct_change > 0
            else "Negative/Suspicious"
        )

    if rule == "bad_up":
        return (
            "Negative/Suspicious"
            if pct_change > 0
            else "Positive"
        )

    return "Normal"


# ============================================================
# READ EXCEL FILE
# ============================================================

df = pd.read_excel("Dataset.xlsx")

print("\nDATASET")
print(df)


# ============================================================
# CONVERSION COLUMN
# ============================================================

conv_col = (
    "Conversion"
    if "Conversion" in df.columns
    else "Conversion Rate"
)


# ============================================================
# COLUMN MAP
# ============================================================

COLUMN_MAP = {
    "Revenue": "Revenue",
    "Orders": "Orders",
    "Traffic": "Traffic",
    "Conversion": conv_col,
    "Cost": "Cost",
    "Refunds": "Refunds",
}


# ============================================================
# CLEAN NUMERIC DATA
# ============================================================

for metric_name, real_col in COLUMN_MAP.items():

    df[real_col] = (
        df[real_col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .astype(float)
    )


# ============================================================
# ============================================================
# METHOD 1: Z-SCORE
# ============================================================
# Each value is compared with ALL values in its column.
#
# Example:
#
# Revenue value of one particular day
#              ↓
# Compared with the complete Revenue column
#
# Z-score >= 3 or <= -3 = statistical anomaly
# ============================================================

for metric_name, real_col in COLUMN_MAP.items():

    mean_value = df[real_col].mean()
    std_value = df[real_col].std()

    if std_value == 0:
        df[f"{metric_name}_ZScore"] = 0

    else:
        df[f"{metric_name}_ZScore"] = (
            (df[real_col] - mean_value)
            / std_value
        )


# ============================================================
# Z-SCORE ANOMALY
# ============================================================

zscore_columns = [
    f"{metric}_ZScore"
    for metric in METRIC_RULES
]

df["ZScore_Anomaly"] = (
    df[zscore_columns]
    .abs()
    .ge(Z_THRESHOLD)
    .any(axis=1)
)


# ============================================================
# ============================================================
# METHOD 2: IQR
# ============================================================
# Each value is compared with the complete distribution.
#
# Lower Bound = Q1 - 1.5 × IQR
# Upper Bound = Q3 + 1.5 × IQR
# ============================================================

iqr_anomaly_columns = []

for metric_name, real_col in COLUMN_MAP.items():

    Q1 = df[real_col].quantile(0.25)
    Q3 = df[real_col].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - IQR_MULTIPLIER * IQR
    upper_bound = Q3 + IQR_MULTIPLIER * IQR

    df[f"{metric_name}_IQR_Lower"] = lower_bound
    df[f"{metric_name}_IQR_Upper"] = upper_bound

    anomaly_column = f"{metric_name}_IQR_Anomaly"

    df[anomaly_column] = (
        (df[real_col] < lower_bound)
        |
        (df[real_col] > upper_bound)
    )

    iqr_anomaly_columns.append(anomaly_column)


# ============================================================
# IQR OVERALL ANOMALY
# ============================================================

df["IQR_Anomaly"] = (
    df[iqr_anomaly_columns]
    .any(axis=1)
)


# ============================================================
# ============================================================
# METHOD 3: ISOLATION FOREST
# ============================================================
# IMPORTANT:
#
# Isolation Forest now uses the ACTUAL BUSINESS VALUES.
#
# It does NOT use pct_change().
#
# It looks at:
# Revenue + Orders + Traffic + Conversion + Cost + Refunds
# together.
# ============================================================

if_features = df[
    list(COLUMN_MAP.values())
].copy()


# Fill missing values with column median

if_features = if_features.fillna(
    if_features.median()
)


iso_forest = IsolationForest(
    contamination=IF_CONTAMINATION,
    random_state=IF_RANDOM_STATE
)


raw_predictions = iso_forest.fit_predict(
    if_features
)


# -1 = anomaly
#  1 = normal

df["IF_Anomaly"] = (
    raw_predictions == -1
)


# Lower score = more unusual

df["IF_Anomaly_Score"] = (
    iso_forest.decision_function(
        if_features
    )
)


# ============================================================
# ============================================================
# METHOD 4: BUSINESS RULE
# ============================================================
# This part is OPTIONAL and separate.
#
# It compares each day with the previous day.
#
# This is NOT used for Z-score/IQR/Isolation Forest.
# ============================================================

df["Revenue_Change"] = (
    df["Revenue"].pct_change() * 100
)

df["Orders_Change"] = (
    df["Orders"].pct_change() * 100
)

df["Traffic_Change"] = (
    df["Traffic"].pct_change() * 100
)

df["Conversion_Change"] = (
    df[conv_col].pct_change() * 100
)

df["Cost_Change"] = (
    df["Cost"].pct_change() * 100
)

df["Refunds_Change"] = (
    df["Refunds"].pct_change() * 100
)


CHANGE_COL_MAP = {

    "Revenue":
        "Revenue_Change",

    "Orders":
        "Orders_Change",

    "Traffic":
        "Traffic_Change",

    "Conversion":
        "Conversion_Change",

    "Cost":
        "Cost_Change",

    "Refunds":
        "Refunds_Change",
}


# ============================================================
# BUSINESS STATUS
# ============================================================

for metric_name in METRIC_RULES:

    change_col = CHANGE_COL_MAP[
        metric_name
    ]

    status_col = (
        f"{metric_name}_Status"
    )

    df[status_col] = (
        df[change_col]
        .apply(
            lambda x:
            classify_metric(
                metric_name,
                x
            )
        )
    )


status_cols = [
    f"{metric}_Status"
    for metric in METRIC_RULES
]


df["Business_Rule_Alert"] = (
    df[status_cols]
    .apply(
        lambda row:
        any(
            status ==
            "Negative/Suspicious"
            for status in row
        ),
        axis=1
    )
)


# ============================================================
# FINAL ANOMALY
# ============================================================
#
# A row becomes a statistical anomaly if:
#
# Z-score OR IQR OR Isolation Forest detects it.
#
# Business rule is shown separately.
# ============================================================

df["Statistical_Anomaly"] = (
    df["ZScore_Anomaly"]
    |
    df["IQR_Anomaly"]
    |
    df["IF_Anomaly"]
)


# Combined result

df["Final_Anomaly"] = (
    df["Statistical_Anomaly"]
    |
    df["Business_Rule_Alert"]
)


# ============================================================
# GET ANOMALIES
# ============================================================

anomalies = df[
    df["Final_Anomaly"] == True
]


# ============================================================
# PRINT SUMMARY
# ============================================================

print("\n")
print("=" * 70)
print("🚨 ANOMALY DETECTION SUMMARY")
print("=" * 70)

print(
    "Total rows:",
    len(df)
)

print(
    "Total anomalies:",
    len(anomalies)
)


# ============================================================
# Z-SCORE RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("📊 Z-SCORE ANOMALIES")
print("=" * 70)

print(
    df[
        df["ZScore_Anomaly"] == True
    ][
        ["Date"] + zscore_columns
    ]
)


# ============================================================
# IQR RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("📦 IQR ANOMALIES")
print("=" * 70)

print(
    df[
        df["IQR_Anomaly"] == True
    ][
        ["Date"]
        + iqr_anomaly_columns
    ]
)


# ============================================================
# ISOLATION FOREST RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("🌲 ISOLATION FOREST ANOMALIES")
print("=" * 70)

if_anomalies = df[
    df["IF_Anomaly"] == True
].sort_values(
    "IF_Anomaly_Score"
)

print(
    if_anomalies[
        [
            "Date",
            "IF_Anomaly_Score"
        ]
    ]
)


# ============================================================
# BUSINESS RULE RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("🚨 BUSINESS RULE ANOMALIES")
print("=" * 70)

business_anomalies = df[
    df["Business_Rule_Alert"] == True
]

print(
    business_anomalies[
        ["Date"] + status_cols
    ]
)


# ============================================================
# FINAL RESULTS
# ============================================================

print("\n")
print("=" * 70)
print("🚨 FINAL ANOMALIES")
print("=" * 70)

print(
    anomalies[
        [
            "Date",
            "ZScore_Anomaly",
            "IQR_Anomaly",
            "IF_Anomaly",
            "Business_Rule_Alert",
            "Final_Anomaly"
        ]
    ]
)


# ============================================================
# DETAILED REPORT
# ============================================================

# ============================================================
# DETAILED REPORT + AI BUSINESS SUMMARY
# ============================================================

for index, row in anomalies.iterrows():

    print("\n")
    print("=" * 70)
    print("🚨 ANOMALY DETECTED")
    print("=" * 70)

    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    print("Date:", row["Date"])


    # --------------------------------------------------------
    # BUSINESS VALUES
    # --------------------------------------------------------

    business_values = {}

    for metric_name, real_col in COLUMN_MAP.items():

        value = row[real_col]

        business_values[metric_name] = value

        print(
            f"{metric_name:<15}: {value}"
        )


    # --------------------------------------------------------
    # STATISTICAL DETECTION
    # --------------------------------------------------------

    print("\nStatistical Detection:")

    print(
        "Z-Score:",
        "🚨 Anomaly"
        if row["ZScore_Anomaly"]
        else "Normal"
    )

    print(
        "IQR:",
        "🚨 Anomaly"
        if row["IQR_Anomaly"]
        else "Normal"
    )

    print(
        "Isolation Forest:",
        "🚨 Anomaly"
        if row["IF_Anomaly"]
        else "Normal"
    )


    # --------------------------------------------------------
    # ISOLATION FOREST SCORE
    # --------------------------------------------------------

    print("\nIsolation Forest Score:")

    print(
        round(
            row["IF_Anomaly_Score"],
            4
        )
    )


    # --------------------------------------------------------
    # BUSINESS RULE
    # --------------------------------------------------------

    print("\nBusiness Rule:")

    if row["Business_Rule_Alert"]:

        triggered_metrics = [

            metric_name

            for metric_name in METRIC_RULES

            if row[f"{metric_name}_Status"]
            == "Negative/Suspicious"

        ]

        business_rule_status = "🚨 Business Issue"

        caused_by = ", ".join(
            triggered_metrics
        )

        print("🚨 Business Issue")

        print(
            "Caused by:",
            caused_by
        )

    else:

        business_rule_status = (
            "✅ No business-rule issue"
        )

        caused_by = "None"

        print(
            "✅ No business-rule issue"
        )


    # ========================================================
    # GEMINI AI SUMMARY
    # ========================================================

    print("\n🤖 Generating AI Business Summary...")

    ai_summary = generate_ai_summary(

        # ----------------------------------------------------
        # DATE
        # ----------------------------------------------------

        date=row["Date"],


        # ----------------------------------------------------
        # REAL BUSINESS VALUES
        # ----------------------------------------------------

        business_values=business_values,


        # ----------------------------------------------------
        # Z-SCORE
        # ----------------------------------------------------

        zscore_status=(
            "🚨 Anomaly"
            if row["ZScore_Anomaly"]
            else "Normal"
        ),


        # ----------------------------------------------------
        # IQR
        # ----------------------------------------------------

        iqr_status=(
            "🚨 Anomaly"
            if row["IQR_Anomaly"]
            else "Normal"
        ),


        # ----------------------------------------------------
        # ISOLATION FOREST
        # ----------------------------------------------------

        isolation_forest_status=(
            "🚨 Anomaly"
            if row["IF_Anomaly"]
            else "Normal"
        ),


        # ----------------------------------------------------
        # ISOLATION FOREST SCORE
        # ----------------------------------------------------

        isolation_forest_score=round(
            row["IF_Anomaly_Score"],
            4
        ),


        # ----------------------------------------------------
        # BUSINESS RULE
        # ----------------------------------------------------

        business_rule_status=(
            business_rule_status
        ),

        caused_by=caused_by
    )


    # ========================================================
    # DISPLAY AI SUMMARY
    # ========================================================

    print("\n" + "_" * 60)

    print("🤖 AI BUSINESS SUMMARY:")

    print("_" * 60)

    print(ai_summary)

    print("_" * 60)