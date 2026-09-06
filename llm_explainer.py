# import os
# import requests


# # ============================================================
# # GEMINI API CONFIGURATION
# # ============================================================

# API_KEY = os.getenv("GEMINI_API_KEY")

# if not API_KEY:
#     raise ValueError(
#         "GEMINI_API_KEY not found.\n"
#         "Please set your Google AI Studio API key."
#     )


# # ============================================================
# # GEMINI AI SUMMARY FUNCTION
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

#     prompt = f"""
# You are an experienced business data analyst.

# A separate anomaly detection system has already detected
# a suspicious business-data record.

# Your job is ONLY to explain the detected anomaly
# to a business manager.

# IMPORTANT RULES:

# 1. Do NOT perform anomaly detection yourself.

# 2. Use ONLY the information provided.

# 3. Do NOT invent facts.

# 4. Do NOT change the detection result.

# 5. Do NOT claim a specific cause unless the data proves it.

# 6. If suggesting a possible cause, use:
#    "may indicate",
#    "could indicate",
#    or
#    "may be related to".

# 7. Explain:
#    - What is unusual?
#    - Which metric is concerning?
#    - Why could this matter?
#    - What should the manager investigate?

# 8. Keep the summary between 60 and 100 words.

# 9. Use simple professional business language.

# 10. Do not explain the technical algorithms.

# Generate ONLY the business summary.

# ============================================================
# DETECTED ANOMALY
# ============================================================

# Date:
# {date}

# BUSINESS VALUES:

# Revenue: {business_values["Revenue"]}
# Orders: {business_values["Orders"]}
# Traffic: {business_values["Traffic"]}
# Conversion: {business_values["Conversion"]}
# Cost: {business_values["Cost"]}
# Refunds: {business_values["Refunds"]}

# ============================================================
# DETECTION RESULTS
# ============================================================

# Z-Score:
# {zscore_status}

# IQR:
# {iqr_status}

# Isolation Forest:
# {isolation_forest_status}

# Isolation Forest Score:
# {isolation_forest_score}

# Business Rule:
# {business_rule_status}

# Caused By:
# {caused_by}

# ============================================================

# Generate the business summary now.
# """


#     # ========================================================
#     # GEMINI API
#     # ========================================================

#     url = (
#         "https://generativelanguage.googleapis.com/"
#         "v1beta/models/gemini-3.6-flash:generateContent"
#     )

#     headers = {
#         "x-goog-api-key": API_KEY,
#         "Content-Type": "application/json"
#     }

#     data = {
#         "contents": [
#             {
#                 "parts": [
#                     {
#                         "text": prompt
#                     }
#                 ]
#             }
#         ]
#     }


#     # ========================================================
#     # SEND REQUEST
#     # ========================================================

#     try:

#         print("📡 Sending anomaly to Gemini...")

#         response = requests.post(
#             url,
#             headers=headers,
#             json=data,
#             timeout=30
#         )


#         # ----------------------------------------------------
#         # CHECK API
#         # ----------------------------------------------------

#         if response.status_code != 200:

#             return (
#                 "Gemini API Error:\n"
#                 + response.text
#             )


#         # ----------------------------------------------------
#         # READ RESPONSE
#         # ----------------------------------------------------

#         result = response.json()


#         # ----------------------------------------------------
#         # EXTRACT AI SUMMARY
#         # ----------------------------------------------------

#         summary = (
#             result["candidates"][0]
#             ["content"]
#             ["parts"][0]
#             ["text"]
#         )


#         return summary.strip()


#     except requests.exceptions.Timeout:

#         return "Gemini request timed out."


#     except Exception as e:

#         return f"Gemini error: {e}"

import os
import time
import requests

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found.\n"
        "Please set your Google AI Studio API key."
    )


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

A separate anomaly detection system has already detected
a suspicious business-data record.

Your job is ONLY to explain the detected anomaly
to a business manager.

IMPORTANT RULES:

1. Do NOT perform anomaly detection yourself.
2. Use ONLY the information provided.
3. Do NOT invent facts.
4. Do NOT change the detection result.
5. Do NOT claim a specific cause unless the data proves it.
6. If suggesting a possible cause, use:
   "may indicate", "could indicate", or "may be related to".
7. Explain:
   - What is unusual?
   - Which metric is concerning?
   - Why could this matter?
   - What should the manager investigate?
8. Keep the summary between 60 and 100 words.
9. Use simple professional business language.
10. Do not explain the technical algorithms.

Generate ONLY the business summary.

============================================================
DETECTED ANOMALY
============================================================

Date:
{date}

BUSINESS VALUES:

Revenue: {business_values["Revenue"]}
Orders: {business_values["Orders"]}
Traffic: {business_values["Traffic"]}
Conversion: {business_values["Conversion"]}
Cost: {business_values["Cost"]}
Refunds: {business_values["Refunds"]}

============================================================
DETECTION RESULTS
============================================================

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

============================================================

Generate the business summary now.
"""

    url = (
        "https://generativelanguage.googleapis.com/"
        "v1beta/models/gemini-3.6-flash:generateContent"
    )

    headers = {
        "x-goog-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    # ============================================
    # GEMINI REQUEST WITH RETRY
    # ============================================

    max_retries = 3

    for attempt in range(1, max_retries + 1):

        try:

            print(
                f"📡 Sending anomaly to Gemini "
                f"(attempt {attempt}/{max_retries})..."
            )

            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=90
            )

            # ------------------------------------
            # SUCCESS
            # ------------------------------------

            if response.status_code == 200:

                result = response.json()

                summary = (
                    result["candidates"][0]
                    ["content"]
                    ["parts"][0]
                    ["text"]
                )

                return summary.strip()

            # ------------------------------------
            # TEMPORARY ERRORS
            # ------------------------------------

            if response.status_code in [408, 429, 500, 502, 503, 504]:

                print(
                    f"⚠️ Gemini temporary error: "
                    f"HTTP {response.status_code}"
                )

                if attempt < max_retries:

                    wait_time = 2 ** attempt

                    print(
                        f"⏳ Retrying in "
                        f"{wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                    continue

                return (
                    f"Gemini request failed after "
                    f"{max_retries} attempts. "
                    f"HTTP {response.status_code}"
                )

            # ------------------------------------
            # OTHER API ERRORS
            # ------------------------------------

            return (
                "Gemini API Error:\n"
                + response.text
            )

        # ----------------------------------------
        # TIMEOUT
        # ----------------------------------------

        except requests.exceptions.Timeout:

            print(
                f"⏰ Gemini request timed out "
                f"(attempt {attempt}/{max_retries})"
            )

            if attempt < max_retries:

                wait_time = 2 ** attempt

                print(
                    f"⏳ Retrying in "
                    f"{wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:

                return (
                    "Gemini request timed out "
                    f"after {max_retries} attempts."
                )

        # ----------------------------------------
        # CONNECTION ERROR
        # ----------------------------------------

        except requests.exceptions.ConnectionError as e:

            print(
                "🌐 Connection error while "
                "connecting to Gemini."
            )

            if attempt < max_retries:

                wait_time = 2 ** attempt

                print(
                    f"⏳ Retrying in "
                    f"{wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:

                return f"Gemini connection error: {e}"

        # ----------------------------------------
        # OTHER ERROR
        # ----------------------------------------

        except Exception as e:

            return f"Gemini error: {e}"