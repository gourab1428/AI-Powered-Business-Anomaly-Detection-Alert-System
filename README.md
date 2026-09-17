# AI-Powered Business Anomaly Detection & Alert System

> An end-to-end Business Analytics and AI automation system that detects unusual business performance using statistical analysis, machine learning, and business rules, generates an AI-powered business explanation using Google Gemini, and automatically sends anomaly alerts through Gmail.

---

## 📌 Overview

Businesses generate large amounts of operational data every day. Metrics such as revenue, orders, traffic, conversion rate, cost, and refunds can change significantly over time.

Manually monitoring these metrics can be difficult and time-consuming. A business analyst may need to determine not only whether a value is unusual, but also which business metric requires attention and what should be investigated.

This project provides an automated anomaly detection and alerting pipeline that combines:

- Statistical anomaly detection
- Machine learning
- Business-specific rules
- Generative AI
- Email automation

### Complete Workflow

```text
Dataset.xlsx
     ↓
Data Loading & Preprocessing
     ↓
Z-Score + IQR + Isolation Forest + Business Rules
     ↓
Final Anomalies
     ↓
Google Gemini
     ↓
AI Business Summary
     ↓
Gmail SMTP
     ↓
Multiple Recipients
```

---

# Objectives

The main objectives of this project are:

1. Automatically identify unusual business observations.
2. Combine multiple anomaly detection techniques.
3. Apply business-specific rules to business metrics.
4. Separate anomaly detection from AI-based explanation.
5. Generate understandable summaries for business stakeholders.
6. Automatically distribute anomaly alerts through email.
7. Demonstrate an end-to-end Data Analytics + Machine Learning + Generative AI workflow.

---

#  Problem Statement

Traditional business monitoring often requires analysts or managers to manually inspect spreadsheets, dashboards, or reports.

This can result in:

- Important anomalies being overlooked.
- Slow identification of unusual business performance.
- Difficulty interpreting statistical results.
- Repetitive manual reporting.
- Delayed communication with stakeholders.

For example, a sudden revenue decline may be statistically unusual. However, a manager may still want to know:

- What changed?
- Which metric is concerning?
- Why might the change matter?
- What should be investigated?

This project addresses these requirements by combining automated anomaly detection with AI-assisted explanation and email notification.

---

#  System Architecture

```text
┌─────────────────────────────┐
│        Dataset.xlsx         │
│                             │
│ Revenue | Orders | Traffic  │
│ Conversion | Cost | Refunds │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│    Data Preprocessing       │
│                             │
│ • Data Cleaning             │
│ • Numeric Conversion        │
│ • Column Handling           │
│ • Missing Value Handling    │
└──────────────┬──────────────┘
               │
               ▼
┌────────────────────────────────────┐
│       Anomaly Detection Layer      │
│                                    │
│  ┌─────────┐   ┌──────────────┐   │
│  │ Z-Score │   │     IQR      │   │
│  └─────────┘   └──────────────┘   │
│                                    │
│  ┌──────────────────────────────┐  │
│  │      Isolation Forest        │  │
│  └──────────────────────────────┘  │
│                                    │
│  ┌──────────────────────────────┐  │
│  │       Business Rules         │  │
│  └──────────────────────────────┘  │
└──────────────────┬─────────────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ Final Anomaly List  │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │    Google Gemini    │
        │    LLM Explainer    │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │ AI Business Summary │
        └──────────┬──────────┘
                   │
                   ▼
        ┌─────────────────────┐
        │     Gmail SMTP      │
        │   Email Automation  │
        └──────────┬──────────┘
                   │
                   ▼
          ┌────────────────┐
          │ Stakeholders   │
          │ / Team Members │
          └────────────────┘
```

---

#  Dataset

The current project uses:

```text
Dataset.xlsx
```

The dataset contains business observations with metrics including:

```text
Date
Revenue
Orders
Traffic
Conversion
Cost
Refunds
```

The implementation also supports a conversion column represented as either:

```text
Conversion
```

or:

```text
Conversion Rate
```

---

#  Business Metrics

| Metric | Description | Business Context |
|---|---|---|
| Date | Business observation date | Identifies the observation period |
| Revenue | Revenue generated | Overall financial performance |
| Orders | Number of orders | Customer purchasing activity |
| Traffic | Website/business traffic | Business reach or activity |
| Conversion | Conversion rate | Ability to convert traffic |
| Cost | Business expenditure | Operational/marketing spending |
| Refunds | Refund amount | Returned revenue/customer issue indicator |

---

#  Anomaly Detection Methodology

The project uses four complementary approaches.

## 1. Z-Score

Z-score measures how far a value is from the mean in terms of standard deviations.

Conceptually:

```text
Z = (X - Mean) / Standard Deviation
```

The project uses:

```text
Z_THRESHOLD = 3
```

An observation is flagged by the Z-score method when its absolute Z-score reaches the configured threshold.

### Purpose

Z-score is useful for identifying observations that are significantly different from the overall distribution of a metric.

---

## 2. IQR — Interquartile Range

The IQR method detects observations outside the expected statistical range.

The project uses:

```text
IQR_MULTIPLIER = 1.5
```

The boundaries are:

```text
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

Values outside these boundaries are treated as potential outliers.

### Purpose

IQR provides an additional statistical approach for identifying extreme observations and complements the Z-score method.

---

## 3. Isolation Forest

Isolation Forest is an unsupervised machine-learning algorithm used to identify unusual observations.

The model analyzes multiple business metrics:

```text
Revenue
Orders
Traffic
Conversion
Cost
Refunds
```

Configuration:

```text
IF_CONTAMINATION = 0.05
IF_RANDOM_STATE = 42
```

The model generates an anomaly prediction and an Isolation Forest score.

### Purpose

Isolation Forest allows the system to analyze multiple business metrics together rather than evaluating every metric independently.

For example:

```text
Low Revenue
+
High Cost
+
High Refunds
```

may represent an unusual business pattern even when the individual metrics are not equally extreme.

---

## 4. Business Rule Detection

Statistical methods identify mathematically unusual values, but businesses may also define specific expectations for how metrics should change.

The project therefore compares the current observation with the previous observation using percentage change.

The configured threshold is:

```text
THRESHOLD = 30%
```

Conceptually:

```text
Percentage Change =
((Current Value - Previous Value) / Previous Value) × 100
```

A movement beyond the configured threshold can trigger a business-rule alert.

---

# 📋 Business Rules

Different metrics have different business interpretations.

```text
Revenue
→ Increase is generally positive

Orders
→ Increase is generally positive

Traffic
→ Neutral

Conversion
→ Increase is generally positive

Cost
→ Increase can be concerning

Refunds
→ Increase can be concerning
```

These rules provide business context instead of treating every numerical change identically.

---

#  Final Anomaly Logic

The project combines statistical and business-rule results.

```text
Final Anomaly
=
Statistical Anomaly
OR
Business Rule Alert
```

The statistical anomaly is:

```text
Statistical Anomaly
=
Z-Score Anomaly
OR
IQR Anomaly
OR
Isolation Forest Anomaly
```

Therefore, an observation can become a final anomaly because:

- Z-score identifies it.
- IQR identifies it.
- Isolation Forest identifies it.
- Business rules identify it.
- Multiple methods identify it simultaneously.

---

#  Generative AI Layer

After the Python pipeline identifies an anomaly, the detected information is passed to Google Gemini.

Gemini is used as an **explanation layer**, not as the primary anomaly detector.

### Architecture

```text
Detection Layer
      ↓
Detected Anomaly
      ↓
Gemini LLM
      ↓
AI Business Explanation
```

The LLM receives information such as:

```text
Date
Revenue
Orders
Traffic
Conversion
Cost
Refunds

Z-Score Status
IQR Status
Isolation Forest Status
Isolation Forest Score

Business Rule Status
Detected Category
```

Gemini then generates a concise business-oriented explanation.

---

#  Important AI Design Principle

The LLM does **not** independently decide whether an observation is anomalous.

Instead:

```text
❌ Incorrect

Raw Dataset
    ↓
Gemini
    ↓
"Maybe this is an anomaly"
```

The project uses:

```text
✅ Implemented

Raw Dataset
    ↓
Statistical + ML + Business Detection
    ↓
Detected Anomaly
    ↓
Gemini
    ↓
Business Explanation
```

This keeps the anomaly decision in the analytical pipeline while using the LLM for explanation and communication.

---

# AI Prompt Design

The Gemini prompt is designed to:

- Use only the supplied information.
- Avoid inventing facts.
- Not perform anomaly detection itself.
- Explain what changed.
- Identify concerning metrics.
- Explain why the situation may matter.
- Suggest what a manager should investigate.
- Avoid presenting an unproven cause as a fact.
- Generate a concise business summary.

For possible causes, the prompt encourages cautious language such as:

```text
"may indicate"
"could indicate"
"may be related to"
```

This is important because an anomaly detector can identify an unusual pattern, but the available data may not prove the exact business cause.

---

# Automated Email Alert System

Once the AI summary is generated, the project automatically sends an email using Gmail SMTP.

The email contains:

```text
🚨 BUSINESS ANOMALY ALERT

Date

Business Values

Statistical Detection

Z-Score
IQR
Isolation Forest
Isolation Forest Score

Business Rule

Caused By / Detected Category

AI Business Summary
```

---

# 👥 Multiple Recipients

The email module supports multiple recipients.

Example:

```python
RECIPIENTS = [
    "recipient1@gmail.com",
    "recipient2@gmail.com",
    "recipient3@gmail.com"
]
```

This allows the same anomaly report to be delivered to multiple stakeholders.

---

# Complete Project Workflow

### Step 1 — Load Data

`Dataset.xlsx` is loaded using Pandas.

### Step 2 — Clean and Prepare Data

The system prepares numerical columns, removes formatting such as commas, converts values to numerical types, and handles the conversion column.

### Step 3 — Analyze Business Metrics

The system extracts:

```text
Revenue
Orders
Traffic
Conversion
Cost
Refunds
```

### Step 4 — Run Z-Score Detection

Statistically unusual observations are identified.

### Step 5 — Run IQR Detection

Values outside the IQR boundaries are identified.

### Step 6 — Run Isolation Forest

The machine-learning model identifies unusual combinations of business metrics.

### Step 7 — Apply Business Rules

Current and previous observations are compared using the configured percentage-change threshold.

### Step 8 — Create Final Anomaly List

All detection results are combined.

### Step 9 — Prepare Anomaly Information

For each detected anomaly, the system collects:

```text
Date
Business Values
Detection Status
Isolation Forest Score
Business Rule Status
Detected Category
```

### Step 10 — Generate AI Explanation

The detected information is sent to Gemini.

### Step 11 — Send Email Alert

The final report and AI summary are sent to configured recipients.

---

# 📂 Project Structure

```text
AI-Business-Anomaly-Detection/
│
├── Dataset.xlsx
│
├── anomaly_detector.py
│   └── Main anomaly detection pipeline
│
├── llm_explainer.py
│   └── Gemini API and AI business summary
│
├── email_alert.py
│   └── Gmail SMTP email notification
│
├── requirements.txt
│
├── .gitignore
│
├── README.md
│
└── screenshots/
    ├── detection_output.png
    ├── ai_summary.png
    └── email_alert.png
```

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Pandas | Data manipulation and analysis |
| NumPy | Numerical operations |
| SciPy | Statistical analysis |
| Scikit-learn | Isolation Forest |
| Requests | Gemini API communication |
| Google Gemini | AI-powered business explanation |
| Gmail SMTP | Automated email delivery |
| OpenPyXL | Excel file processing |
| Microsoft Excel | Input dataset |

---

# 📦 Requirements

Create a `requirements.txt` file:

```text
pandas
numpy
scipy
scikit-learn
requests
openpyxl
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Business-Anomaly-Detection.git
```

Navigate into the project:

```bash
cd AI-Business-Anomaly-Detection
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

The project requires:

```text
GEMINI_API_KEY
GMAIL_SENDER_EMAIL
GMAIL_APP_PASSWORD
```

These credentials are intentionally kept outside the source code.

---

# 🪟 Windows PowerShell Configuration

In PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_GEMINI_API_KEY"

$env:GMAIL_SENDER_EMAIL="your-email@gmail.com"

$env:GMAIL_APP_PASSWORD="YOUR_GMAIL_APP_PASSWORD"
```

Then run:

```powershell
python anomaly_detector.py
```

> These `$env:` variables apply to the current PowerShell session. If you close the terminal, you need to set them again unless you configure them as persistent Windows environment variables.

---

# Running the Project

After configuring the required environment variables:

```powershell
python anomaly_detector.py
```

Expected workflow:

```text
Loading Dataset
      ↓
Cleaning Data
      ↓
Running Z-Score
      ↓
Running IQR
      ↓
Running Isolation Forest
      ↓
Applying Business Rules
      ↓
Finding Final Anomalies
      ↓
Calling Gemini
      ↓
Generating AI Summary
      ↓
Sending Email
      ↓
Alert Delivered
```

---

# Security

Never commit API keys or passwords to GitHub.

Do not upload:

```text
.env
GEMINI_API_KEY
GMAIL_APP_PASSWORD
```

Recommended `.gitignore`:

```gitignore
.env
*.env
__pycache__/
*.pyc
```

For Gmail authentication, use a Google App Password where applicable instead of exposing your normal account password.

---

# Example Detection Result

During testing, the system identified five final anomaly dates:

```text
2026-08-04
2026-08-09
2026-08-13
2026-08-16
2026-08-17
```

These observations were identified using the project's combined anomaly-detection logic.

---

# Example Detected Observation

One detected observation contained:

```text
Date: 2026-08-17

Revenue: 17745
Orders: 127
Traffic: 4000
Conversion: 3.175
Cost: 47000
Refunds: 3500
```

The detection results included an IQR anomaly and a business-rule issue associated with the revenue metric.

The detected information was then provided to Gemini for a business-oriented explanation.

---

#  Example AI Business Summary

A Gemini-generated summary can follow a structure such as:

```text
The business experienced a significant change in revenue on the
detected date. Revenue is the primary metric requiring attention,
while the observed cost and refund values provide additional
context for investigating the situation. The pattern may indicate
a change in business performance and should be reviewed alongside
transaction activity, pricing, customer behavior, and operational
factors to determine what contributed to the unusual result.
```

> The actual summary is dynamically generated from the detected anomaly and supplied business values.

---

# Example Email Alert

```text
🚨 BUSINESS ANOMALY ALERT
======================================================================

Date: 2026-08-17

BUSINESS VALUES
----------------------------------------------------------------------
Revenue: 17745
Orders: 127
Traffic: 4000
Conversion: 3.175
Cost: 47000
Refunds: 3500

STATISTICAL DETECTION
----------------------------------------------------------------------
Z-Score: Normal
IQR: 🚨 Anomaly
Isolation Forest: Normal
Isolation Forest Score: 0.XXXX

BUSINESS RULE
----------------------------------------------------------------------
Status: Issue
Caused By: Revenue

🤖 AI BUSINESS SUMMARY
----------------------------------------------------------------------
[Gemini-generated business explanation]

======================================================================
```

---

# End-to-End Testing

The project has been tested through the complete workflow:

```text
Excel Dataset
      ↓
Anomaly Detection
      ↓
Gemini API
      ↓
AI Business Summary
      ↓
Gmail SMTP
      ↓
Multiple Recipients
```

The working implementation has demonstrated:

- Successful dataset processing
- Multiple anomaly identification
- Gemini API integration
- AI-generated business summaries
- Gmail SMTP integration
- Delivery to multiple recipients

---

#  Why Use Multiple Detection Methods?

A single anomaly detection method may not capture every type of unusual business behavior.

This project combines:

```text
Z-Score
   +
IQR
   +
Isolation Forest
   +
Business Rules
```

Each method provides a different perspective.

### Statistical Methods

Identify values that are unusual within the observed distribution.

### Machine Learning

Identifies unusual observations using multiple business metrics together.

### Business Rules

Introduce business-specific expectations and thresholds.

Combining these approaches creates a broader anomaly detection pipeline.

---

#  Key Features

### 📊 Automated Data Analysis

Processes business data without requiring manual inspection of every observation.

### 🔍 Multi-Method Anomaly Detection

Uses statistical, machine-learning, and business-rule approaches.

### 📋 Business-Aware Detection

Metric-specific rules provide additional business context.

### 🤖 AI Explanation

Gemini converts technical detection results into a concise business summary.

### 📧 Automated Notification

Anomaly reports are delivered automatically to configured recipients.

### 🧩 Modular Design

The system separates:

```text
Detection
AI Explanation
Email Notification
```

into dedicated Python modules.

---

# 🌍 Real-World Applications

## 🛒 E-Commerce

Monitor:

- Revenue
- Orders
- Traffic
- Conversion
- Refunds
- Business costs

##  Digital Marketing

Monitor:

- Website traffic
- Conversion rate
- Campaign cost
- Revenue
- Customer acquisition metrics

##  Financial Analytics

Monitor:

- Revenue
- Expenses
- Transaction patterns
- Refunds
- Financial KPIs

##  Business Operations

Monitor:

- Operational costs
- Sales
- Orders
- Customer activity
- Business KPIs

---

#  Limitations

The current implementation is a working prototype and has several limitations.

### 1. Excel-Based Input

The current input is an Excel file rather than a live database or API.

### 2. Dataset Size

The current dataset is relatively small and primarily demonstrates the project architecture.

### 3. Fixed Detection Parameters

Some parameters are configured manually:

```text
Z_THRESHOLD = 3
IQR_MULTIPLIER = 1.5
THRESHOLD = 30
IF_CONTAMINATION = 0.05
```

These values may require tuning for different datasets and business environments.

### 4. Historical Distribution

Z-score and IQR results depend on the distribution of the available data.

### 5. LLM Dependency

AI explanations depend on Gemini API availability and quota.

### 6. No Guaranteed Root Cause

An anomaly detector identifies an unusual pattern, but an unusual observation does not automatically prove its business cause.

The AI summary should therefore be treated as an analytical interpretation rather than proof of causality.

---

#  Future Improvements

##  1. Interactive Dashboard

Build a Streamlit dashboard containing:

- KPI cards
- Revenue trends
- Order trends
- Traffic trends
- Conversion trends
- Cost trends
- Refund trends
- Anomaly history
- AI explanations

##  2. Database Integration

Replace Excel with:

```text
MySQL
PostgreSQL
SQL Server
Cloud Database
```

##  3. Scheduled Monitoring

Automatically execute the anomaly pipeline:

```text
Hourly
Daily
Weekly
```

depending on business requirements.

##  4. Cloud Deployment

Deploy the system using:

```text
AWS
Microsoft Azure
Google Cloud
```

##  5. Additional Alert Channels

Future versions could support:

```text
Email
Slack
Microsoft Teams
SMS
```

##  6. Advanced Anomaly Detection

Future versions could include:

```text
Time-Series Models
Autoencoders
LSTM
Prophet
Clustering
Advanced Isolation Forest tuning
```

##  7. Historical Anomaly Database

Store anomaly results for:

- Historical analysis
- Repeated anomaly investigation
- Trend analysis
- Model evaluation
- Reporting

---

#  Future Production Architecture

```text
              ┌───────────────────┐
              │ Database / API    │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Data Ingestion    │
              │ / ETL Pipeline    │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Data Processing   │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Anomaly Detection │
              │                   │
              │ Z-Score           │
              │ IQR               │
              │ Isolation Forest  │
              │ Business Rules    │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Anomaly Database  │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Gemini LLM        │
              │ Explanation       │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ BI Dashboard      │
              └─────────┬─────────┘
                        │
                        ▼
              ┌───────────────────┐
              │ Alert System      │
              │ Email / Slack     │
              └───────────────────┘
```

---

#  Skills Demonstrated

## Python

- Data processing
- Functions
- Loops
- Exception handling
- API integration
- Automation

## Data Analytics

- Data cleaning
- Statistical analysis
- Outlier detection
- Business KPI analysis
- Percentage-change analysis

## Statistics

- Z-score
- IQR
- Quartiles
- Standard deviation
- Percentage change

## Machine Learning

- Isolation Forest
- Unsupervised anomaly detection
- Multi-feature analysis

## Generative AI

- Gemini API
- Prompt engineering
- LLM integration
- AI-assisted business explanation

## Automation

- SMTP
- Gmail integration
- Automated alerts
- Multiple recipients

## Business Intelligence

- KPI monitoring
- Business rules
- Anomaly reporting
- Action-oriented insights

---

#  Resume Project Description

### AI-Powered Business Anomaly Detection & Alert System

Developed an automated business anomaly detection pipeline using Python, Z-score, IQR, Isolation Forest, and business rules to identify unusual changes across revenue, orders, traffic, conversion, cost, and refunds. Integrated Google Gemini to generate concise business explanations for detected anomalies and implemented Gmail SMTP automation to distribute alerts to multiple stakeholders.

---

#  Interview Explanation

> "I developed an AI-powered business anomaly detection system that combines statistical analysis, machine learning, business rules, generative AI, and email automation. The system reads business data from Excel and analyzes revenue, orders, traffic, conversion, cost, and refunds. I used Z-score, IQR, and Isolation Forest for anomaly detection and added business-specific percentage-change rules. Once an anomaly is detected, the information is sent to Google Gemini, which generates a business-friendly explanation. Finally, the system automatically sends the anomaly report and AI summary to multiple recipients through Gmail SMTP."

---

#  Conclusion

The **AI-Powered Business Anomaly Detection & Alert System** demonstrates how traditional data analytics, machine learning, business logic, generative AI, and automation can be combined into a single end-to-end workflow.

The project moves beyond simple anomaly identification by transforming detected anomalies into understandable business information and automatically communicating the results to stakeholders.

The current implementation provides a foundation that can be extended with:

- Real-time data sources
- Databases
- Interactive dashboards
- Cloud deployment
- Advanced anomaly detection models
- Historical anomaly tracking
- Additional notification channels

The overall concept can be summarized as:

```text
Detect
  ↓
Analyze
  ↓
Explain
  ↓
Alert
```

---

# 👨‍💻 Author

## Gourab Tikadar

**BCA Graduate | Data Analytics | Python | AI/ML**

### Areas of Interest

- Data Analytics
- Python
- Machine Learning
- Artificial Intelligence
- Business Intelligence
- SQL
- Cloud Technologies

---

# 📌 Project Status

```text
🟢 Working Prototype
```

### Current Capabilities

```text
✅ Excel Data Input
✅ Data Cleaning
✅ Z-Score Detection
✅ IQR Detection
✅ Isolation Forest
✅ Business Rule Detection
✅ Combined Anomaly Detection
✅ Gemini AI Integration
✅ AI Business Summary
✅ Gmail SMTP Integration
✅ Multiple Email Recipients
```

### Planned Improvements

```text
🔄 Streamlit Dashboard
🔄 Database Integration
🔄 Real-Time Data
🔄 Scheduled Monitoring
🔄 Cloud Deployment
🔄 Advanced Anomaly Detection
🔄 Additional Alert Channels
```

---

## ⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.
