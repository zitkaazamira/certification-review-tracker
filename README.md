# Certification Review Tracker

A simple tool for checking certification records and organizing records that may need further review.

This project was inspired by my experience working with IT product certification data during my internship at Badan Siber dan Sandi Negara (BSSN). The application uses fully synthetic data and does not contain or reproduce internal BSSN records.

## What this project does

Certification records can contain missing information, duplicate certificate numbers, outdated dates, or verification statuses that still need to be checked.

This app helps review those records in one place.

Users can:

* use the sample dataset provided in this repository
* upload their own Excel or CSV file
* check records using predefined validation rules
* identify incomplete or inconsistent records
* filter records that need attention
* review issue details and priority levels
* download the checked results as an Excel file

## Validation checks

The current version checks for:

| Check | Description |
|---|---|
| Required fields | Finds missing vendor, algorithm, certificate number, CMVP status, or Postel status |
| Duplicate certificate | Finds certificate numbers that appear more than once |
| Expired certificate | Checks whether the certificate has passed its expiry date |
| Status mismatch | Finds records marked Active even though the expiry date has passed |
| Verification status | Flags CMVP or Postel records marked Pending or Not Found |
| Revoked certificate | Identifies certificates with Revoked status |
| Expiring soon | Finds certificates that will expire within 30 days |

## How it works

```text
Certification Records
        ↓
Data Validation
        ↓
Issue Detection
        ↓
Priority Assignment
        ↓
Review Queue
        ↓
Checked Results
```

Records with no detected issues are marked **Clear**.

Records with missing information, inconsistent values, verification issues, or certificate problems are placed in **Need Review**.

The app also assigns a priority level to help organize the review process.

## Sample data

The sample dataset contains 1,200 synthetic IT product certification records.

Some records intentionally contain data quality issues so the validation process can be demonstrated.

The dataset includes fields such as:

* product name
* vendor
* product category
* cryptographic module
* algorithm
* certificate number
* certificate status
* CMVP verification status
* Postel verification status
* issue date
* expiry date
* last verification date

## Project structure

```text
certification-review-tracker/
│
├── zitka_certification_tracker.py
├── requirements.txt
│
├── sample_data/
│   └── certification_review_sample_data.xlsx
│
├── README.md
└── .gitignore
```

## Tools

**Python**

Used for the validation logic and data processing.

**Pandas**

Used to clean, check, filter, and summarize certification records.

**Streamlit**

Used to build the interactive application.

**Excel**

Used as one of the supported input and output formats.

## Try the app

A live demo is available through Streamlit.

**Live Demo:** Coming soon

You can use the sample dataset directly from the app, so no file upload is required to try the project.

## About the data

All records used in this project are synthetic and were created specifically for portfolio purposes.

This project does not contain confidential information, internal documents, certification records, or datasets belonging to BSSN or any other institution.

The workflow is a simplified portfolio simulation based on general data validation and administrative review tasks.

## About me

I am a Mathematics graduate interested in data analysis, administration, risk management, and compliance.

My previous experience includes working with data validation, technical documentation, administrative records, IT product certification data, and government information systems.

I enjoy working with structured data and finding practical ways to make checking and monitoring processes easier.
