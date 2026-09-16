import os
import smtplib
from email.message import EmailMessage


# ============================================================
# GMAIL CONFIGURATION
# ============================================================

SENDER_EMAIL = os.getenv("GMAIL_SENDER_EMAIL")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

RECIPIENTS = [
    "gtikadar2005@gmail.com",
    "kankanadas022@gmail.com",
    "jayitaroy2185@gmail.com"
]


# ============================================================
# SEND EMAIL
# ============================================================

def send_anomaly_email(
    date,
    business_values,
    zscore_status,
    iqr_status,
    isolation_forest_status,
    isolation_forest_score,
    business_rule_status,
    caused_by,
    ai_summary
):

    if not SENDER_EMAIL:
        raise ValueError("GMAIL_SENDER_EMAIL is not set.")

    if not APP_PASSWORD:
        raise ValueError("GMAIL_APP_PASSWORD is not set.")

    # --------------------------------------------------------
    # EMAIL SUBJECT
    # --------------------------------------------------------

    subject = f"🚨 Business Anomaly Alert - {date}"

    # --------------------------------------------------------
    # EMAIL BODY
    # --------------------------------------------------------

    body = f"""
🚨 BUSINESS ANOMALY ALERT
========================================

Date:
{date}


BUSINESS VALUES
========================================

Revenue        : {business_values["Revenue"]}
Orders         : {business_values["Orders"]}
Traffic        : {business_values["Traffic"]}
Conversion     : {business_values["Conversion"]}
Cost           : {business_values["Cost"]}
Refunds        : {business_values["Refunds"]}


STATISTICAL DETECTION
========================================

Z-Score          : {zscore_status}
IQR              : {iqr_status}
Isolation Forest : {isolation_forest_status}

Isolation Forest Score:
{isolation_forest_score}


BUSINESS RULE
========================================

Status:
{business_rule_status}

Caused By:
{caused_by}


🤖 AI BUSINESS SUMMARY
========================================

{ai_summary}


========================================
This alert was automatically generated
by the AI Business Anomaly Detection System.
========================================
"""

    # --------------------------------------------------------
    # CREATE EMAIL
    # --------------------------------------------------------

    message = EmailMessage()

    message["From"] = SENDER_EMAIL
    message["To"] = ", ".join(RECIPIENTS)
    message["Subject"] = subject

    message.set_content(body)

    # --------------------------------------------------------
    # SEND THROUGH GMAIL SMTP
    # --------------------------------------------------------

    try:

        print("📧 Sending email alert...")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:

            server.starttls()

            server.login(
                SENDER_EMAIL,
                APP_PASSWORD
            )

            server.send_message(message)

        print("✅ Email alert sent successfully!")

    except smtplib.SMTPAuthenticationError:

        print("❌ Gmail authentication failed.")
        print("Check your Gmail address and App Password.")

    except Exception as e:

        print(f"❌ Email sending failed: {e}")