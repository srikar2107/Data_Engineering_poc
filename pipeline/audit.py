from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine

from config.config import DATABASE_URL

engine = create_engine(DATABASE_URL)


def log_audit(
    pipeline_name,
    layer_name,
    inserted_records,
    updated_records,
    rejected_records,
    status,
    remarks=""
):
    df = pd.DataFrame({
        "pipeline_name": [pipeline_name],
        "layer_name": [layer_name],
        "inserted_records": [inserted_records],
        "updated_records": [updated_records],
        "rejected_records": [rejected_records],
        "execution_time": [datetime.now()],
        "status": [status],
        "remarks": [remarks]
    })

    df.to_sql(
        "pipeline_audit",
        engine,
        schema="audit",
        if_exists="append",
        index=False
    )

    print("✅ Audit Logged Successfully")