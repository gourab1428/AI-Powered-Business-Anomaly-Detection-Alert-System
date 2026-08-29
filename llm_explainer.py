# import os

# from google import genai
# from google.genai import types


# # ============================================================
# # GEMINI API CONFIGURATION
# # ============================================================

# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError(
#         "GEMINI_API_KEY not found.\n"
#         "Please set your Google AI Studio API key first."
#     )


# client = genai.Client(
#     api_key=api_key
# )


# # ============================================================
# # FUNCTION: GENERATE AI BUSINESS SUMMARY
# # ============================================================

# def generate_ai_summary(
#     date,
#     business_values,
#     zscore_status,
#     iqr_status,
#     isolation_forest_status,
#     isolation_forest_score,
#     business_rule_status,
#     caused_by
# ):

#     # --------------------------------------------------------
#     # PROMPT
#     # --------------------------------------------------------

#     prompt = f"""
# You are an experienced business data analyst.

# Your job is to explain a detected business-data anomaly
# to a manager in simple and professional language.

# IMPORTANT RULES:

# 1. Do NOT detect an anomaly yourself.
#    The detection has already been done by the statistical
#    and business-rule system.

# 2. Use ONLY the information provided below.

# 3. Do NOT invent facts.

# 4. Do NOT claim a specific cause unless the data proves it.

# 5. If you mention a possible cause, use:
#    "may indicate",
#    "could indicate",
#    or
#    "may be related to".

# 6. Explain:

#    - What changed?
#    - Which metrics are concerning?
#    - Why could this matter to the business?
#    - What should the manager investigate?

# 7. Keep the answer between 60 and 100 words.

# 8. Use simple and professional business language.

# 9. Do not explain Z-score, IQR, or Isolation Forest
#    in detail.

# 10. Focus on the business meaning.

# ------------------------------------------------------------
# ANOMALY INFORMATION
# ------------------------------------------------------------

# Date:
# {date}

# Business Values:

# Revenue:
# {business_values["Revenue"]}

# Orders:
# {business_values["Orders"]}

# Traffic:
# {business_values["Traffic"]}

# Conversion:
# {business_values["Conversion"]}

# Cost:
# {business_values["Cost"]}

# Refunds:
# {business_values["Refunds"]}


# ------------------------------------------------------------
# STATISTICAL DETECTION
# ------------------------------------------------------------

# Z-Score:
# {zscore_status}

# IQR:
# {iqr_status}

# Isolation Forest:
# {isolation_forest_status}

# Isolation Forest Score:
# {isolation_forest_score}


# ------------------------------------------------------------
# BUSINESS RULE
# ------------------------------------------------------------

# Business Rule:
# {business_rule_status}

# Caused By:
# {caused_by}


# ------------------------------------------------------------

# Generate ONLY the AI business summary.

# Do not add a title.
# Do not repeat the input data.
# """


#     # --------------------------------------------------------
#     # SEND REQUEST TO GEMINI
#     # --------------------------------------------------------

#     try:

#             # SEND REQUEST TO GEMINI
#     # --------------------------------------------------

#         print("🎤 Sending request to Gemini...")

#         response = client.models.generate_content(
#             model="gemini-3.7-flash",
#             contents=prompt
#         )

#         print("✅ Response received from Gemini.")

#         if response.text:
#             return response.text.strip()

#         return "Gemini returned an empty response."

#     except Exception as e:
#         return f"Gemini error: {e}"

#     # --------------------------------------------------
#     # GET AI RESPONSE
#     # --------------------------------------------------

#         # ----------------------------------------------------
#         # GET AI RESPONSE
#         # ----------------------------------------------------

#         if response.text:

#             return response.text.strip()

#         else:

#             return (
#                 "AI summary could not be generated: "
#                 "Gemini returned an empty response."
#             )


#     except Exception as e:

#         return (
#             f"AI summary could not be generated:\n{e}"
#         )


# # ============================================================
# # DIRECT TEST
# # ============================================================

# if __name__ == "__main__":

#     print("\n" + "=" * 60)
#     print("🤖 GEMINI LLM EXPLAINER TEST")
#     print("=" * 60)


#     # --------------------------------------------------------
#     # SAMPLE ANOMALY DATA
#     # --------------------------------------------------------

#     test_values = {

#         "Revenue": 17745.0,

#         "Orders": 127.0,

#         "Traffic": 4000.0,

#         "Conversion": 3.175,

#         "Cost": 47000.0,

#         "Refunds": 3500.0

#     }


#     # --------------------------------------------------------
#     # SEND TEST DATA TO GEMINI
#     # --------------------------------------------------------

#     summary = generate_ai_summary(

#         date="2026-08-17 00:00:00",

#         business_values=test_values,

#         zscore_status="Normal",

#         iqr_status="🚨 Anomaly",

#         isolation_forest_status="Normal",

#         isolation_forest_score=0.0258,

#         business_rule_status="🚨 Business Issue",

#         caused_by="Revenue"
#     )


#     # --------------------------------------------------------
#     # DISPLAY AI RESULT
#     # --------------------------------------------------------

#     print("\n🤖 AI BUSINESS SUMMARY:")

#     print("-" * 60)

#     print(summary)

#     print("-" * 60)

#     print("✅ GEMINI TEST COMPLETED")

#     print("=" * 60)

import os
import requests


# ============================================================
# GEMINI API CONFIGURATION
# ============================================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found.\n"
        "Please set your Google AI Studio API key."
    )


# ============================================================
# GEMINI FUNCTION
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

Explain this detected business anomaly to a manager.

Use simple and professional language.

Rules:

- Do not perform anomaly detection yourself.
- Use only the information provided.
- Do not invent facts.
- Do not claim a specific cause unless the data proves it.
- If suggesting a possible cause, use "may indicate",
  "could indicate", or "may be related to".
- Explain what changed.
- Explain which metrics are concerning.
- Explain why it may matter.
- Explain what the manager should investigate.
- Keep the answer between 60 and 100 words.
- Do not explain Z-score, IQR, or Isolation Forest.
- Generate only the business summary.

DATE:
{date}

BUSINESS VALUES:

Revenue: {business_values["Revenue"]}
Orders: {business_values["Orders"]}
Traffic: {business_values["Traffic"]}
Conversion: {business_values["Conversion"]}
Cost: {business_values["Cost"]}
Refunds: {business_values["Refunds"]}

STATISTICAL DETECTION:

Z-Score: {zscore_status}
IQR: {iqr_status}
Isolation Forest: {isolation_forest_status}
Isolation Forest Score: {isolation_forest_score}

BUSINESS RULE:

{business_rule_status}

Caused By:
{caused_by}
"""


    # ========================================================
    # GEMINI REST API
    # ========================================================

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/interactions"
    )

    headers = {
        "x-goog-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "model": "gemini-3.6-flash",
        "input": prompt
    }


    try:

        print("📡 Sending request directly to Gemini...")

        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=30
        )

        print(
            "HTTP Status:",
            response.status_code
        )


        # ----------------------------------------------------
        # CHECK API ERROR
        # ----------------------------------------------------

        if response.status_code != 200:

            return (
                "Gemini API Error:\n"
                + response.text
            )


        # ----------------------------------------------------
        # READ RESPONSE
        # ----------------------------------------------------

        result = response.json()


        # ----------------------------------------------------
        # GET OUTPUT TEXT
        # ----------------------------------------------------

        output_text = result.get(
            "output_text"
        )


        if output_text:

            return output_text.strip()


        # ----------------------------------------------------
        # FALLBACK: READ STEPS
        # ----------------------------------------------------

        for step in result.get(
            "steps",
            []
        ):

            if step.get("type") == "model_output":

                for content in step.get(
                    "content",
                    []
                ):

                    if content.get(
                        "type"
                    ) == "text":

                        return content.get(
                            "text",
                            ""
                        ).strip()


        return "Gemini returned an empty response."


    except requests.exceptions.Timeout:

        return (
            "Gemini request timed out after 30 seconds."
        )


    except Exception as e:

        return f"Gemini connection error: {e}"


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("🤖 GEMINI LLM EXPLAINER TEST")
    print("=" * 60)


    test_values = {

        "Revenue": 17745.0,

        "Orders": 127.0,

        "Traffic": 4000.0,

        "Conversion": 3.175,

        "Cost": 47000.0,

        "Refunds": 3500.0
    }


    print("\n📊 Test anomaly loaded.")


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

    print("✅ TEST FINISHED")

    print("=" * 60)