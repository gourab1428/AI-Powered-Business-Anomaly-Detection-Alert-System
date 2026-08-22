import os
from openai import OpenAI

# ============================================================
# OPENAI CONFIGURATION
# ============================================================

# Set your API key as an environment variable:
# Windows PowerShell:
# $env:OPENAI_API_KEY="your_api_key"

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# ============================================================
# FUNCTION: GENERATE BUSINESS EXPLANATION
# ============================================================

def generate_ai_summary(
    date,
    business_values,
    zscore_status,
    iqr_status,
    isolation_forest_status,
    isolation_forest_score,
    business_rule_status,
    caused_by
):

    prompt = f"""
You are an experienced business data analyst.

Your job is to explain a detected business-data anomaly
to a manager in simple and professional language.

IMPORTANT RULES:

1. Do NOT detect an anomaly yourself.
   The statistical and business detection has already been done.

2. Use ONLY the information provided below.

3. Do NOT invent facts.

4. Do NOT claim a specific cause unless the data proves it.

5. If you mention a possible cause, clearly use words such as:
   "may indicate", "could indicate", or "may be related to".

6. Explain:
   - What changed?
   - Which metrics are concerning?
   - Why could this matter to the business?
   - What should the manager investigate?

7. Keep the answer between 60 and 100 words.

8. Do not use unnecessary technical terms.

9. Do not explain Z-score, IQR, or Isolation Forest in detail.
   Focus on the business meaning.

------------------------------------------------------------
ANOMALY INFORMATION
------------------------------------------------------------

Date:
{date}

Business Values:

Revenue:
{business_values["Revenue"]}

Orders:
{business_values["Orders"]}

Traffic:
{business_values["Traffic"]}

Conversion:
{business_values["Conversion"]}

Cost:
{business_values["Cost"]}

Refunds:
{business_values["Refunds"]}


Statistical Detection:

Z-Score:
{zscore_status}

IQR:
{iqr_status}

Isolation Forest:
{isolation_forest_status}

Isolation Forest Score:
{isolation_forest_score}


Business Rule:
{business_rule_status}

Caused By:
{caused_by}

------------------------------------------------------------

Generate the business summary now.
"""

    try:

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text.strip()

    except Exception as e:

        return f"AI summary could not be generated: {e}"


# ============================================================
# TEST THE LLM
# ============================================================

if __name__ == "__main__":

    test_values = {
        "Revenue": 17745.0,
        "Orders": 127.0,
        "Traffic": 4000.0,
        "Conversion": 3.175,
        "Cost": 47000.0,
        "Refunds": 3500.0
    }

    summary = generate_ai_summary(
        date="2026-08-17 00:00:00",

        business_values=test_values,

        zscore_status="Normal",

        iqr_status="🚨 Anomaly",

        isolation_forest_status="Normal",

        isolation_forest_score=0.0258,

        business_rule_status="🚨 Business Issue",

        caused_by="Revenue"
    )

    print("\n" + "=" * 60)
    print("🤖 AI BUSINESS SUMMARY")
    print("=" * 60)
    print(summary)
    print("=" * 60)