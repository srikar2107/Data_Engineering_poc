import pandas as pd
from pathlib import Path

print("Silver Layer Processing Started")

# ====================================
# Paths
# ====================================

SILVER_PATH = Path("data/silver")

# ====================================
# Process all Silver files
# ====================================

def process_silver():

    parquet_files = list(SILVER_PATH.glob("*.parquet"))

    print(f"\nFound {len(parquet_files)} Silver files\n")

    if len(parquet_files) == 0:
        print("No Silver files found.")
        return

    for file in parquet_files:

        print("=" * 60)
        print(f"Processing : {file.name}")

        df = pd.read_parquet(file)

        # --------------------------------
        # Standardize Column Names
        # --------------------------------

        df.columns = (
            df.columns
              .str.strip()
              .str.lower()
              .str.replace(" ", "_")
        )

        # --------------------------------
        # Clean String Columns
        # --------------------------------

        string_columns = df.select_dtypes(include="object").columns

        for col in string_columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
            )

        # --------------------------------
        # Convert Date Columns
        # --------------------------------

        for col in df.columns:

            if "date" in col or "timestamp" in col:

                df[col] = pd.to_datetime(
                    df[col],
                    errors="coerce"
                )

        # --------------------------------
        # Fill Missing Values
        # --------------------------------

        for col in df.columns:

            if df[col].dtype == "object":

                df[col] = df[col].fillna("unknown")

            elif str(df[col].dtype).startswith(("int", "float")):

                df[col] = df[col].fillna(0)

        # --------------------------------
        # Remove Duplicate Rows
        # --------------------------------

        df = df.drop_duplicates()

        # --------------------------------
        # Save File
        # --------------------------------

        df.to_parquet(file, index=False)

        print(f"Saved : {file.name}")

    print("\nSilver Layer Processing Completed Successfully")


# ====================================
# Execute
# ====================================

if __name__ == "__main__":
    process_silver()