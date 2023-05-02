"""bigqueryを操作するモジュール"""
from google.auth.credentials import AnonymousCredentials
from google.cloud import bigquery

from gcp.config.bq_config import MOST_POPULAR_TABLE_SCHEMA
from gcp.config.gcp_config import PROJECT_ID

# client_options = ClientOptions(
# api_endpoint="http://host.docker.internal:9050"
# )

# ローカルからbigqueryのshellを起動する
# bq --api http://0.0.0.0:9050 --project_id=youtube_data_api shell

client = bigquery.Client(
    credentials=AnonymousCredentials(),
    project=PROJECT_ID,
    # client_options=client_options
)

dataset_name = "videos"
table_name = "most_popular"


def generate_dataset(dataset_name: str) -> None:
    # [demo]という名称でDataSetを作成
    dataset_id = "{}.{}".format(client.project, dataset_name)
    dataset = bigquery.Dataset(dataset_id)
    # locationはUSが一番安いのでいつもこれにしている. リージョンにこだわりがあれば変更してください
    dataset.location = "US"

    client.create_dataset(dataset)


def generate_table(table_name: str) -> None:
    # テーブル名を決める
    table_id = "{}.{}.{}".format(PROJECT_ID, dataset_name, table_name)
    table = bigquery.Table(table_id, schema=MOST_POPULAR_TABLE_SCHEMA)

    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="CREATED_AT"
    )

    table.clustering_fields = ["CHANNEL_ID", "CATEGORY_ID"]
    table.description = "DEmo Data"

    client.create_table(table)


if __name__ == "__main__":
    generate_dataset(dataset_name)
    generate_table(table_name)
