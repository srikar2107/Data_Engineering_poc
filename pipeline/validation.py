import pandas as pd
from pathlib import Path

print("Validation Script Started")

# ============================
# Paths
# ============================

BRONZE_PATH = Path("data/bronze")
SILVER_PATH = Path("data/silver")
REJECT_PATH = Path("data/reject")


def validate_data():

    # Create folders if they don't exist
    SILVER_PATH.mkdir(parents=True, exist_ok=True)
    REJECT_PATH.mkdir(parents=True, exist_ok=True)

    print(f"\nBronze Folder : {BRONZE_PATH.resolve()}")

    # Read all parquet files
    parquet_files = list(BRONZE_PATH.glob("*.parquet"))

    print(f"Found {len(parquet_files)} Bronze files\n")

    if len(parquet_files) == 0:
        print("No Parquet files found in data/bronze")
        return

    # Process each file
    for file in parquet_files:

        print("=" * 60)
        print(f"Validating : {file.name}")

        df = pd.read_parquet(file)

        total_rows = len(df)

        # Remove duplicate rows
        df = df.drop_duplicates()

        # Remove rows where every column is NULL
        df = df.dropna(how="all")

        valid_rows = len(df)
        rejected_rows = total_rows - valid_rows

        # Save valid records
        silver_file = SILVER_PATH / file.name
        df.to_parquet(silver_file, index=False)

        # Save rejected record count
        if rejected_rows > 0:

            reject_df = pd.DataFrame({
                "Rejected_Rows": [rejected_rows]
            })

            reject_file = REJECT_PATH / file.name
            reject_df.to_parquet(reject_file, index=False)

        print(f"Total Rows     : {total_rows}")
        print(f"Valid Rows     : {valid_rows}")
        print(f"Rejected Rows  : {rejected_rows}")
        print(f"Saved          : {silver_file.name}")

    print("\nValidation Completed Successfully")


if __name__ == "__main__":
    validate_data()