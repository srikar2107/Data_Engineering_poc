import pandas as pd
from pathlib import Path
from datetime import datetime

RAW_DATA_PATH = Path("data/raw")
BRONZE_DATA_PATH = Path("data/bronze")


def ingest_data():

    BRONZE_DATA_PATH.mkdir(parents=True, exist_ok=True)

    csv_files = list(RAW_DATA_PATH.glob("*.csv"))

    print(f"\nFound {len(csv_files)} CSV files\n")

    for file in csv_files:

        print(f"Reading {file.name}")

        df = pd.read_csv(file)

        df["load_timestamp"] = datetime.now()
        df["source_file"] = file.name

        output_file = BRONZE_DATA_PATH / file.with_suffix(".parquet").name

        df.to_parquet(output_file, index=False)

        print(f"Saved {output_file.name}")

    print("\nBronze Layer Created Successfully!")


if __name__ == "__main__":
    ingest_data()