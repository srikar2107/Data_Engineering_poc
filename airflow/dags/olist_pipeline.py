from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "srikar",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="olist_data_pipeline",
    default_args=default_args,
    description="Olist End-to-End Data Engineering Pipeline",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["Data Engineering", "Olist"],
) as dag:

    bronze = BashOperator(
        task_id="bronze_ingestion",
        bash_command="cd /opt/airflow/project && python -m pipeline.ingestion"
    )

    validation = BashOperator(
        task_id="validation",
        bash_command="cd /opt/airflow/project && python -m pipeline.validation"
    )

    silver = BashOperator(
        task_id="silver_layer",
        bash_command="cd /opt/airflow/project && python -m pipeline.silver"
    )

    transformation = BashOperator(
        task_id="transformation",
        bash_command="cd /opt/airflow/project && python -m pipeline.transformation"
    )

    scd_type1 = BashOperator(
        task_id="scd_type1",
        bash_command="cd /opt/airflow/project && python -m pipeline.scd_type1"
    )

    scd_type2 = BashOperator(
        task_id="scd_type2",
        bash_command="cd /opt/airflow/project && python -m pipeline.scd_type2"
    )

    gold = BashOperator(
        task_id="gold_layer",
        bash_command="cd /opt/airflow/project && python -m pipeline.gold"
    )

    postgres_loader = BashOperator(
        task_id="postgres_loader",
        bash_command="cd /opt/airflow/project && python -m pipeline.loader"
    )

    audit = BashOperator(
        task_id="audit_logging",
        bash_command="cd /opt/airflow/project && python -m pipeline.audit"
    )

    metadata = BashOperator(
        task_id="metadata_generation",
        bash_command="cd /opt/airflow/project && python -m pipeline.metadata"
    )

    (
        bronze
        >> validation
        >> silver
        >> transformation
        >> scd_type1
        >> scd_type2
        >> gold
        >> postgres_loader
        >> audit
        >> metadata
    )