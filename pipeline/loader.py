from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine, text

from config.config import DATABASE_URL
from pipeline.metadata import log_pipeline_execution
from pipeline.audit import log_audit

# ---------------------------------------------------
# Start Time
# ---------------------------------------------------
start_time = datetime.now()

print("=" * 60)
print("Loading Gold Layer into PostgreSQL...")
print("=" * 60)

engine = create_engine(DATABASE_URL)

# ---------------------------------------------------
# Create Gold Schema if it doesn't exist
# ---------------------------------------------------
with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold;"))

try:
    # ---------------------------------------------------
    # Read Gold Parquet Files
    # ---------------------------------------------------
    dim_customer = pd.read_parquet("data/gold/dim_customer.parquet")
    dim_customer_scd2 = pd.read_parquet("data/gold/dim_customer_scd2.parquet")
    dim_product = pd.read_parquet("data/gold/dim_product.parquet")
    dim_seller = pd.read_parquet("data/gold/dim_seller.parquet")
    fact_orders = pd.read_parquet("data/gold/fact_orders.parquet")
    monthly_sales = pd.read_parquet("data/gold/monthly_sales.parquet")
    sales_summary = pd.read_parquet("data/gold/sales_summary.parquet")

    # ---------------------------------------------------
    # Load into PostgreSQL
    # ---------------------------------------------------
    dim_customer.to_sql(
        "dim_customer",
        engine,
        schema="gold",
        if_exists="replace",
        index=False
    )

    dim_customer_scd2.to_sql(
        "dim_customer_scd2",
        engine,
        schema="gold",
        if_exists="replace",
        index=False
    )

    dim_product.to_sql(
        "dim_product",
        engine,
        schema="gold",
        if_exists="replace",
        index=False
    )

    dim_seller.to_sql(
        "dim_seller",
        engine,
        schema="gold",
        if_exists="replace",
        index=False
    )

    fact_orders.to_sql(
        "fact_orders",
        engine,
        schema="gold",
        if_exists="replace",
        index=False
    )

    monthly_sales.to_sql(
        "monthly_sales",
        engine,
        schema="gold",
        if_exists="replace",
        index=False
    )

    sales_summary.to_sql(
        "sales_summary",
        engine,
        schema="gold",
        if_exists="replace",
        index=False
    )

    print("\n✅ Gold Layer Successfully Loaded into PostgreSQL")

    # ---------------------------------------------------
    # Calculate Total Records
    # ---------------------------------------------------
    end_time = datetime.now()

    total_records = (
        len(dim_customer)
        + len(dim_customer_scd2)
        + len(dim_product)
        + len(dim_seller)
        + len(fact_orders)
        + len(monthly_sales)
        + len(sales_summary)
    )

    # ---------------------------------------------------
    # Metadata Logging
    # ---------------------------------------------------
    log_pipeline_execution(
        pipeline_name="PostgreSQL Loader",
        layer_name="Gold",
        start_time=start_time,
        end_time=end_time,
        records_processed=total_records,
        status="SUCCESS"
    )

    # ---------------------------------------------------
    # Audit Logging
    # ---------------------------------------------------
    log_audit(
        pipeline_name="PostgreSQL Loader",
        layer_name="Gold",
        inserted_records=total_records,
        updated_records=0,
        rejected_records=0,
        status="SUCCESS",
        remarks="Gold layer loaded into PostgreSQL successfully"
    )

    

except Exception as e:

    end_time = datetime.now()

    # ---------------------------------------------------
    # Metadata Logging (Failure)
    # ---------------------------------------------------
    log_pipeline_execution(
        pipeline_name="PostgreSQL Loader",
        layer_name="Gold",
        start_time=start_time,
        end_time=end_time,
        records_processed=0,
        status="FAILED",
        error_message=str(e)
    )

    # ---------------------------------------------------
    # Audit Logging (Failure)
    # ---------------------------------------------------
    log_audit(
        pipeline_name="PostgreSQL Loader",
        layer_name="Gold",
        inserted_records=0,
        updated_records=0,
        rejected_records=0,
        status="FAILED",
        remarks=str(e)
    )

    print("\n❌ Pipeline Failed")
    print(e)