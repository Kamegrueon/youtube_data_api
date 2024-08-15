"""bigqueryを操作するモジュール"""
from google.cloud import bigquery
from gcp.config.bq_schema import MOST_POPULAR_TABLE_SCHEMA


class BqInterface:
    def __init__(self, project_id: str) -> None:
        self.client = bigquery.Client(project=project_id)

    def generate_dataset(self, dataset_name: str) -> None:
        # [demo]という名称でDataSetを作成
        dataset_id = f"{self.client.project}.{dataset_name}"
        dataset = bigquery.Dataset(dataset_id)
        # locationはUSが一番安いのでいつもこれにしている. リージョンにこだわりがあれば変更してください
        dataset.location = "US"
        self.client.create_dataset(dataset)

    def generate_table(self, dataset_name: str, table_name: str) -> None:
        # テーブル名を決める
        table_id = f"{self.client.project}.{dataset_name}.{table_name}"
        table = bigquery.Table(table_id, schema=MOST_POPULAR_TABLE_SCHEMA)

        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="CREATED_AT"
        )

        table.clustering_fields = ["CHANNEL_ID", "CATEGORY_ID"]
        table.description = "Demo Data"

        self.client.create_table(table)

    def insert_table_data(
        self,
        dataset_name: str,
        table_name: str,
        data: list[dict]
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