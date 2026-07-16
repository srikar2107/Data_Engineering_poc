from datetime import datetime

import pandas as pd

from sqlalchemy import create_engine

from config.config import DATABASE_URL

engine = create_engine(DATABASE_URL)


def log_pipeline_execution(
        pipeline_name,
        layer_name,
        start_time,
        end_time,
        records_processed,
        status,
        error_message=""
):

    duration = (end_time - start_time).total_seconds()

    df = pd.DataFrame({

        "pipeline_name": [pipeline_name],

        "layer_name": [layer_name],

        "start_time": [start_time],

        "end_time": [end_time],

        "duration_seconds": [duration],

        "records_processed": [records_processed],

        "status": [status],

        "error_message": [error_message]

    })

    df.to_sql(
        "pipeline_execution",
        engine,
        schema="metadata",
        if_exists="append",
        index=False
    )

    print("✅ Metadata Logged Successfully")