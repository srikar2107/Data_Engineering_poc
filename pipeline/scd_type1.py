import pandas as pd
from pathlib import Path

print("SCD TYPE 1 Script Started")

# =====================================
# Paths
# =====================================

TRANSFORMED_PATH = Path("data/transformed")
GOLD_PATH = Path("data/gold")

GOLD_PATH.mkdir(parents=True, exist_ok=True)

INPUT_FILE = TRANSFORMED_PATH / "olist_transformed.parquet"
OUTPUT_FILE = GOLD_PATH / "dim_customer.parquet"


def scd_type1():

    print("\nLoading Transformed Data...")

    if not INPUT_FILE.exists():
        print("Transformed file not found.")
        return

    df = pd.read_parquet(INPUT_FILE)

    print("Rows Loaded :", len(df))

    # =====================================
    # Customer Dimension
    # =====================================

    dim_customer = df[
        [
            "customer_id",
            "customer_unique_id",
            "customer_city",
            "customer_state",
        ]
    ].copy()

    # Remove duplicates
    dim_customer = dim_customer.drop_duplicates(
        subset=["customer_id"],
        keep="last"
    )

    print("Unique Customers :", len(dim_customer))

    # =====================================
    # SCD Type 1 Logic
    # =====================================

    if OUTPUT_FILE.exists():

        print("Existing Dimension Found")

        existing = pd.read_parquet(OUTPUT_FILE)

        merged = pd.concat(
            [existing, dim_customer],
            ignore_index=True
        )

        # Keep latest record
        merged = merged.drop_duplicates(
            subset=["customer_id"],
            keep="last"
        )

        merged.to_parquet(
            OUTPUT_FILE,
            index=False
        )

        print("Dimension Updated Successfully")

    else:

        dim_customer.to_parquet(
            OUTPUT_FILE,
            index=False
        )

        print("Dimension Created Successfully")

    print("\nOutput File")
    print(OUTPUT_FILE.resolve())

    print("\nSCD TYPE 1 Completed Successfully")


if __name__ == "__main__":
    scd_type1()