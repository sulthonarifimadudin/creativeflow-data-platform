# CreativeFlow Data Platform

<p align="center">
  <img src="dashboard/creativeflow-dashboard.png" width="900"/>
</p>

<h3 align="center">
End-to-End Data Engineering Project for Photography Business Analytics
</h3>

<p align="center">
Building a scalable data warehouse pipeline from raw business data into analytics-ready insights.
</p>


---

## 📌 Overview

CreativeFlow Data Platform is an end-to-end Data Engineering project that demonstrates how raw operational data can be transformed into a structured **Data Warehouse** and delivered as business intelligence dashboards.

The project simulates a photography service company that manages:

- Customer information
- Photography packages
- Photographer resources
- Booking transactions
- Payment transactions


The platform implements a complete data pipeline:

```
Raw Data
   |
   ↓
ETL Pipeline
   |
   ↓
Data Warehouse
   |
   ↓
Analytics Layer
   |
   ↓
Business Dashboard
```


---

# 🏗️ Architecture

```
                    CSV Data Sources
                          |
                          |
                          ↓

                Python ETL Pipeline

        ┌──────────────┬───────────────┐
        │ Extract      │ Transform     │
        │              │               │
        │ CSV Reader   │ Cleaning      │
        │              │ Validation    │
        │              │ Key Mapping  │
        └──────────────┴───────────────┘

                          |
                          ↓

              PostgreSQL Data Warehouse

                          |
                          ↓

                 Analytics SQL Layer

                          |
                          ↓

                  Metabase Dashboard
```


---

# 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas |
| Database | PostgreSQL 16 |
| Database Container | Docker |
| ETL Framework | Custom Python ETL Pipeline |
| Database Connector | SQLAlchemy + Psycopg2 |
| Testing Framework | Pytest |
| BI Visualization | Metabase |


---

# 📂 Project Structure

```
CreativeFlow Data Platform
│
├── data
│   └── raw
│       ├── clients.csv
│       ├── packages.csv
│       ├── photographers.csv
│       ├── bookings.csv
│       └── payments.csv
│
├── database
│   └── schema.sql
│
├── etl
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── quality.py
│   ├── dim_date.py
│   └── database.py
│
├── analytics
│   └── queries.sql
│
├── tests
│   └── test_quality.py
│
├── dashboard
│   └── creativeflow-dashboard.png
│
├── docker-compose.yml
├── requirements.txt
└── README.md
```


---

# 🧱 Data Warehouse Design

This project uses a **Star Schema** dimensional modeling approach.

The warehouse consists of:

## Dimension Tables

### dim_client

Stores customer information.

Example attributes:

- client_key
- client_id
- name
- email
- phone
- city


---

### dim_package

Stores photography service packages.

Example attributes:

- package_key
- package_id
- package_name
- category
- price
- duration_hour


---

### dim_photographer

Stores photographer information.

Example attributes:

- photographer_key
- photographer_id
- name
- specialization
- experience_year


---

### dim_date

Date dimension for analytical time-based reporting.

Example attributes:

- date_key
- full_date
- year
- month
- quarter
- month_name


---

# Fact Tables

## fact_booking

Contains booking transactions.

Measures and relationships:

- booking_id
- client_key
- package_key
- photographer_key
- booking_date
- event_date
- status


---

## fact_payment

Contains payment transactions.

Measures and relationships:

- payment_id
- booking_key
- payment_date
- amount
- payment_method
- status


---

# 🔄 ETL Pipeline

## 1. Extract

Raw data is extracted from CSV files:

```
clients.csv
packages.csv
photographers.csv
bookings.csv
payments.csv
```


---

## 2. Transform

Data transformation includes:

### Data Cleaning

- Removing duplicates
- Handling missing values
- Standardizing data types


### Data Preparation

- Date normalization
- Numeric conversion
- Data validation


### Surrogate Key Mapping

Business keys are transformed into warehouse keys:

Example:

```
client_id
    |
    ↓
client_key
```


This enables efficient dimensional modeling.


---

## 3. Load

Processed data is loaded into PostgreSQL Data Warehouse.

The pipeline supports:

- Insert operation
- Upsert operation
- Duplicate prevention
- Referential integrity


---

# ✅ Data Quality Framework

The pipeline includes automated data quality validation.

Implemented checks:


## Completeness

Checking required fields:

```
client_id
booking_id
payment_id
```

---

## Uniqueness

Prevent duplicate business records:

```
client_id
booking_id
payment_id
```

---

## Validity

Example:

Payment amount must be positive.

```
amount > 0
```


---

## Referential Integrity

Ensuring relationships exist:

Example:

```
fact_booking.client_key
        |
        ↓
dim_client.client_key
```


---

## Business Rules

Examples:

Booking date validation:

```
booking_date <= event_date
```


Payment validation:

```
payment_date >= booking_date
```


---

# 🧪 Testing

Data quality functions are tested using Pytest.

Current test coverage:

```
10 passed
```


Run tests:

```bash
python -m pytest tests/test_quality.py -v
```


---

# 📊 Analytics Dashboard

The Metabase dashboard provides business insights:


## Executive Metrics

- Total Revenue
- Total Booking
- Repeat Customers


## Revenue Analysis

- Monthly Revenue Trend
- Revenue by Package


## Booking Analysis

- Booking Volume Trend
- Package Popularity


Example insights:

```
Total Revenue:
Rp 21,500,000

Total Booking:
6

Highest Revenue Package:
Wedding Premium
```


---

# 🚀 Getting Started

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/creativeflow-data-platform.git

cd creativeflow-data-platform
```


---

## 2. Start Database

Run PostgreSQL and Metabase:

```bash
docker compose up -d
```


Check containers:

```bash
docker ps
```


---

## 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```


---

## 4. Run ETL Pipeline

Execute pipeline:

```bash
python etl/load.py
```


Expected output:

```
Loaded clients
Loaded packages
Loaded photographers
Loaded bookings
Loaded payments
```


---

## 5. Run Data Quality Check

```bash
python etl/quality.py
```


Expected:

```
OVERALL DATA QUALITY: PASS
```


---

## 6. Open Dashboard

Metabase:

```
http://localhost:3000
```


---

# 📈 Future Improvements

Planned improvements:

- [ ] Implement Apache Airflow orchestration
- [ ] Add incremental data loading
- [ ] Add data lineage tracking
- [ ] Add Docker production deployment
- [ ] Add cloud deployment (AWS/GCP)
- [ ] Implement dbt transformation layer
- [ ] Add automated pipeline monitoring


---

# 🎯 Learning Objectives

Through this project, the following Data Engineering concepts are implemented:

✅ ETL Pipeline Development  
✅ Data Warehouse Architecture  
✅ Star Schema Modeling  
✅ Surrogate Key Management  
✅ Data Quality Engineering  
✅ SQL Analytics  
✅ BI Dashboard Development  
✅ Containerized Data Infrastructure  


---

# 👤 Author

**Muchlis Aryomukti**

AI Engineer | Data Engineer Enthusiast

GitHub:
https://github.com/muchlisam17


LinkedIn:
https://linkedin.com/in/muchlisam


---

⭐ If you find this project useful, feel free to explore and give feedback.