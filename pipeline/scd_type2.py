import pandas as pd
from pathlib import Path
from datetime import datetime

print("SCD TYPE 2 Script Started")

# ======================================
# Paths
# ======================================

TRANSFORMED_PATH = Path("data/transformed")
GOLD_PATH = Path("data/gold")

GOLD_PATH.mkdir(parents=True, exist_ok=True)

INPUT_FILE = TRANSFORMED_PATH / "olist_transformed.parquet"
OUTPUT_FILE = GOLD_PATH / "dim_customer_scd2.parquet"


def scd_type2():

    print("\nLoading Transformed Data...")

    if not INPUT_FILE.exists():
        print("Transformed file not found.")
        return

    df = pd.read_parquet(INPUT_FILE)

    # Create Customer Dimension
    new_dim = df[
        [
            "customer_id",
            "customer_unique_id",
            "customer_city",
            "customer_state",
        ]
    ].drop_duplicates(subset=["customer_id"]).copy()

    # SCD Metadata
    new_dim["effective_date"] = datetime.now()
    new_dim["end_date"] = pd.NaT
    new_dim["is_current"] = True

    # ======================================
    # First Load
    # ======================================

    if not OUTPUT_FILE.exists():

        new_dim.to_parquet(OUTPUT_FILE, index=False)

        print("\nFirst Load Completed")
        print(f"Customers Loaded : {len(new_dim)}")

        return

    # ======================================
    # Incremental Load
    # ======================================

    existing = pd.read_parquet(OUTPUT_FILE)

    updated_rows = []

    current_time = datetime.now()

    for _, new_row in new_dim.iterrows():

        customer = new_row["customer_id"]

        current_record = existing[
            (existing["customer_id"] == customer) &
            (existing["is_current"] == True)
        ]

        # -----------------------
        # New Customer
        # -----------------------

        if current_record.empty:

            updated_rows.append(new_row)

            continue

        old_row = current_record.iloc[0]

        # -----------------------
        # Compare Attributes
        # -----------------------

        changed = (
            old_row["customer_city"] != new_row["customer_city"]
            or
            old_row["customer_state"] != new_row["customer_state"]
        )

        if changed:

            # Close old record

            existing.loc[
                current_record.index,
                "end_date"
            ] = current_time

            existing.loc[
                current_record.index,
                "is_current"
            ] = False

            # Insert new record

            new_row["effective_date"] = current_time
            new_row["end_date"] = pd.NaT
            new_row["is_current"] = True

            updated_rows.append(new_row)

    # Append new versions

    if len(updated_rows) > 0:

        updated_df = pd.DataFrame(updated_rows)

        existing = pd.concat(
            [existing, updated_df],
            ignore_index=True
        )

    existing.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print("\nSCD Type 2 Completed Successfully")
    print(f"Total Records : {len(existing)}")
    print(f"Current Active Records : {existing['is_current'].sum()}")


if __name__ == "__main__":
    scd_type2()