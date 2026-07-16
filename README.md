# 🚀 Data Engineering PoC using Olist E-Commerce Dataset

![Python](https://img.shields.io/badge/Python-3.11-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-blue)
![Airflow](https://img.shields.io/badge/Apache-Airflow-red)
![Docker](https://img.shields.io/badge/Docker-Container-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📌 Project Overview

This project demonstrates an end-to-end **Data Engineering Pipeline** using the **Olist Brazilian E-Commerce Dataset**. It follows a modern data engineering architecture with data ingestion, validation, transformation, Slowly Changing Dimensions (SCD), Gold Layer creation, PostgreSQL integration, metadata tracking, auditing, and workflow orchestration using Apache Airflow.

The project simulates a real-world enterprise ETL pipeline used in data warehouses.

---

## 🏗️ Architecture

```
                 +----------------------+
                 |   Olist CSV Dataset  |
                 +----------+-----------+
                            |
                            ▼
                 +----------------------+
                 |  Data Ingestion      |
                 |  (Bronze Layer)      |
                 +----------+-----------+
                            |
                            ▼
                 +----------------------+
                 | Data Validation      |
                 +----------+-----------+
                            |
                            ▼
                 +----------------------+
                 |  Silver Layer        |
                 | Data Cleaning        |
                 +----------+-----------+
                            |
                            ▼
                 +----------------------+
                 | Business             |
                 | Transformations      |
                 +----------+-----------+
                            |
                  +---------+---------+
                  |                   |
                  ▼                   ▼
         +---------------+    +---------------+
         | SCD Type-1    |    | SCD Type-2    |
         +-------+-------+    +-------+-------+
                 \               /
                  \             /
                   ▼           ▼
              +----------------------+
              |    Gold Layer        |
              +----------+-----------+
                         |
                         ▼
              +----------------------+
              | PostgreSQL Data Mart |
              +----------+-----------+
                         |
                         ▼
              +----------------------+
              | Metadata & Audit     |
              +----------+-----------+
                         |
                         ▼
              +----------------------+
              | Apache Airflow DAG   |
              +----------------------+
```

---

# 📂 Project Structure

```
Data_Engineering_poc/
│
├── airflow/
│   ├── dags/
│   ├── logs/
│   └── docker-compose.yml
│
├── config/
│   └── config.py
│
├── datasets/
│
├── pipeline/
│   ├── ingestion.py
│   ├── validation.py
│   ├── silver.py
│   ├── transformation.py
│   ├── scd_type1.py
│   ├── scd_type2.py
│   ├── gold.py
│   ├── metadata.py
│   ├── audit.py
│   └── utils.py
│
├── sql/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🎯 Objectives

- Build a complete ETL pipeline
- Implement Medallion Architecture
- Perform data validation
- Clean and transform data
- Implement Slowly Changing Dimensions
- Create analytical Gold tables
- Load data into PostgreSQL
- Maintain Metadata & Audit tables
- Automate execution using Apache Airflow

---

# 🛠 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | ETL Development |
| Pandas | Data Processing |
| PostgreSQL | Data Warehouse |
| Apache Airflow | Workflow Orchestration |
| Docker | Containerization |
| SQLAlchemy | Database Connectivity |
| Git & GitHub | Version Control |

---

# ⚙️ ETL Pipeline

## 1️⃣ Bronze Layer

- Reads raw CSV files
- Adds metadata
- Converts to Parquet
- Stores raw data

---

## 2️⃣ Validation Layer

- Null checks
- Duplicate checks
- Data type validation
- Schema validation

---

## 3️⃣ Silver Layer

- Data Cleaning
- Standardization
- Missing value handling
- Remove duplicates

---

## 4️⃣ Transformation Layer

Business transformations include

- Table Joins
- Derived Columns
- Aggregations
- Window Functions
- Lookup Mapping

---

## 5️⃣ Slowly Changing Dimensions

### SCD Type 1

- Overwrites old values
- Maintains latest information

### SCD Type 2

- Preserves historical records
- Tracks Effective Date
- Tracks Expiry Date
- Active Flag

---

## 6️⃣ Gold Layer

Creates analytical tables ready for reporting.

Example KPIs

- Revenue
- Orders
- Customers
- Sellers
- Product Performance
- Delivery Analysis

---

# 🗄 Database

Database: PostgreSQL

Schemas

```
bronze
silver
gold
metadata
audit
```

---

# 🔄 Airflow Workflow

Pipeline execution order

```
Start
   │
   ▼
Ingestion
   │
   ▼
Validation
   │
   ▼
Silver
   │
   ▼
Transformation
   │
   ▼
SCD Type 1
   │
   ▼
SCD Type 2
   │
   ▼
Gold Layer
   │
   ▼
Metadata
   │
   ▼
Audit
   │
   ▼
End
```

---

# 📊 Dataset

Dataset Used:

**Olist Brazilian E-Commerce Public Dataset**

Contains

- Customers
- Orders
- Products
- Sellers
- Reviews
- Payments
- Geolocation

---

# 🚀 Installation

Clone repository

```bash
git clone https://github.com/srikar2107/Data_Engineering_poc.git
```

Go to project

```bash
cd Data_Engineering_poc
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Pipeline

Run each step

```bash
python pipeline/ingestion.py
```

```bash
python pipeline/validation.py
```

```bash
python pipeline/silver.py
```

```bash
python pipeline/transformation.py
```

```bash
python pipeline/scd_type1.py
```

```bash
python pipeline/scd_type2.py
```

```bash
python pipeline/gold.py
```

```bash
python pipeline/metadata.py
```

```bash
python pipeline/audit.py
```

---

# 📈 Future Improvements

- Incremental Loading
- Change Data Capture (CDC)
- Kafka Streaming
- AWS S3 Integration
- Apache Spark
- Snowflake
- Azure Data Factory
- Power BI Dashboard
- Great Expectations
- CI/CD Pipeline

---

# 📚 Learning Outcomes

This project demonstrates knowledge of:

- ETL & ELT
- Data Warehousing
- Medallion Architecture
- Data Validation
- Data Cleaning
- SCD Type 1 & Type 2
- PostgreSQL
- Airflow
- Docker
- Git & GitHub
- Python
- SQL
- Pandas

---

# 👨‍💻 Author

**Srikar E**

B.Tech Computer Science Engineering

SRM Institute of Science and Technology

GitHub: https://github.com/srikar2107

---

# ⭐ If you found this project useful

Please consider giving this repository a ⭐ on GitHub.
