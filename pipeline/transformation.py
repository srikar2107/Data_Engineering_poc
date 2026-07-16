import pandas as pd
from pathlib import Path

print("Transformation Script Started")

# ==========================================
# Paths
# ==========================================

SILVER_PATH = Path("data/silver")
TRANSFORMED_PATH = Path("data/transformed")

TRANSFORMED_PATH.mkdir(parents=True, exist_ok=True)


def load_table(name):
    df = pd.read_parquet(SILVER_PATH / f"{name}.parquet")

    # Remove metadata columns
    df.drop(
        columns=["load_timestamp", "source_file"],
        errors="ignore",
        inplace=True,
    )

    return df


def transform_data():

    print("\nLoading Silver Files...\n")

    orders = load_table("olist_orders_dataset")
    customers = load_table("olist_customers_dataset")
    order_items = load_table("olist_order_items_dataset")
    payments = load_table("olist_order_payments_dataset")
    reviews = load_table("olist_order_reviews_dataset")
    products = load_table("olist_products_dataset")
    sellers = load_table("olist_sellers_dataset")
    category = load_table("product_category_name_translation")

    print("Joining Orders + Customers...")

    df = orders.merge(
        customers,
        on="customer_id",
        how="left"
    )

    print("Joining Order Items...")

    df = df.merge(
        order_items,
        on="order_id",
        how="left"
    )

    print("Joining Products...")

    df = df.merge(
        products,
        on="product_id",
        how="left"
    )

    print("Joining Sellers...")

    df = df.merge(
        sellers,
        on="seller_id",
        how="left"
    )

    print("Joining Payments...")

    df = df.merge(
        payments,
        on="order_id",
        how="left"
    )

    print("Joining Reviews...")

    df = df.merge(
        reviews,
        on="order_id",
        how="left"
    )

    print("Joining Product Category Translation...")

    df = df.merge(
        category,
        on="product_category_name",
        how="left"
    )

    # ==========================================
    # Business Transformations
    # ==========================================

    print("\nApplying Business Transformations...")

    # Delivery Days

    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"]
    )

    df["order_delivered_customer_date"] = pd.to_datetime(
        df["order_delivered_customer_date"]
    )

    df["delivery_days"] = (
        df["order_delivered_customer_date"]
        - df["order_purchase_timestamp"]
    ).dt.days

    # Order Value

    df["total_amount"] = (
        df["price"] +
        df["freight_value"]
    )

    # High Value Order

    df["high_value_order"] = df["total_amount"] > 500

    # Order Year

    df["order_year"] = df["order_purchase_timestamp"].dt.year

    # Order Month

    df["order_month"] = df["order_purchase_timestamp"].dt.month

    # Order Day

    df["order_day"] = df["order_purchase_timestamp"].dt.day

    # Order Weekday

    df["weekday"] = df["order_purchase_timestamp"].dt.day_name()

    # Weekend Order

    df["weekend_order"] = df["weekday"].isin(
        ["Saturday", "Sunday"]
    )

    # ==========================================
    # Save
    # ==========================================

    output = TRANSFORMED_PATH / "olist_transformed.parquet"

    df.to_parquet(output, index=False)

    print("\nRows :", len(df))
    print("Columns :", len(df.columns))

    print("\nSaved :", output)

    print("\nTransformation Completed Successfully")


if __name__ == "__main__":
    transform_data()