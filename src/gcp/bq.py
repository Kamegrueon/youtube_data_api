"""bigqueryを操作するモジュール"""

from google.cloud import bigquery
from utils import gcp_error_handler

from gcp.config.bq_schema import MOST_POPULAR_TABLE_SCHEMA


class BqInterface:
    def __init__(self, project_id: str) -> None:
        self.client = bigquery.Client(project=project_id)

    @gcp_error_handler
    def insert_table_data(
        self, dataset_name: str, table_name: str, data: list[dict]
    ) -> None:
        job_config = bigquery.LoadJobConfig(
            schema=MOST_POPULAR_TABLE_SCHEMA,
        )

        table_id = f"{self.client.project}.{dataset_name}.{table_name}"
        table = self.client.get_table(table_id)
        job = self.client.load_table_from_json(
            json_rows=data,
            destination=table,
            job_config=job_config,
        )
        job.result()
