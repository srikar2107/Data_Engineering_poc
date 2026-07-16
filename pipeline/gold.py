import pandas as pd
from pathlib import Path

print("Gold Layer Script Started")

# =====================================
# Paths
# =====================================

TRANSFORMED_PATH = Path("data/transformed")
GOLD_PATH = Path("data/gold")

GOLD_PATH.mkdir(parents=True, exist_ok=True)

INPUT_FILE = TRANSFORMED_PATH / "olist_transformed.parquet"


def create_gold_layer():

    if not INPUT_FILE.exists():
        print("Transformed file not found.")
        return

    print("\nLoading transformed dataset...")

    df = pd.read_parquet(INPUT_FILE)

    # =====================================
    # FACT TABLE
    # =====================================

    fact_orders = df[
        [
            "order_id",
            "customer_id",
            "product_id",
            "seller_id",
            "payment_value",
            "price",
            "freight_value",
            "review_score",
            "delivery_days",
            "order_purchase_timestamp",
            "order_status"
        ]
    ].copy()

    fact_orders.to_parquet(
        GOLD_PATH / "fact_orders.parquet",
        index=False
    )

    print("✔ fact_orders created")

    # =====================================
    # PRODUCT DIMENSION
    # =====================================

    dim_product = df[
        [
            "product_id",
            "product_category_name",
            "product_category_name_english",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm"
        ]
    ].drop_duplicates()

    dim_product.to_parquet(
        GOLD_PATH / "dim_product.parquet",
        index=False
    )

    print("✔ dim_product created")

    # =====================================
    # SELLER DIMENSION
    # =====================================

    dim_seller = df[
        [
            "seller_id",
            "seller_city",
            "seller_state"
        ]
    ].drop_duplicates()

    dim_seller.to_parquet(
        GOLD_PATH / "dim_seller.parquet",
        index=False
    )

    print("✔ dim_seller created")

    # =====================================
    # SALES SUMMARY
    # =====================================

    sales_summary = (
        df.groupby("order_status")
        .agg(
            total_orders=("order_id", "count"),
            total_sales=("payment_value", "sum"),
            average_review=("review_score", "mean")
        )
        .reset_index()
    )

    sales_summary.to_parquet(
        GOLD_PATH / "sales_summary.parquet",
        index=False
    )

    print("✔ sales_summary created")

    # =====================================
    # MONTHLY SALES
    # =====================================

    monthly_sales = (
        df.groupby(["order_year", "order_month"])
        .agg(
            total_orders=("order_id", "count"),
            total_sales=("payment_value", "sum")
        )
        .reset_index()
        .sort_values(["order_year", "order_month"])
    )

    monthly_sales.to_parquet(
        GOLD_PATH / "monthly_sales.parquet",
        index=False
    )

    print("✔ monthly_sales created")

    print("\nGold Layer Created Successfully")


if __name__ == "__main__":
    create_gold_layer()