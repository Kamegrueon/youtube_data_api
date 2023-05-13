"""bigqueryを操作するモジュール"""
import json

from google.cloud import bigquery
from google.oauth2.service_account import Credentials

from gcp.config.schema import MOST_POPULAR_TABLE_SCHEMA
from gcp.config.gcp_config import GOOGLE_KEY_PATH, PROJECT_ID
from utils.extract_most_popular import (
    extract_most_popular,
    extract_datetime_from_file_name
)

# client_options = ClientOptions(
# api_endpoint="http://host.docker.internal:9050"
# )

# ローカルからbigqueryのshellを起動する
# bq --api http://0.0.0.0:9050 --project_id=youtube_data_api shell


class BQ:
    def __init__(self, project_id: str) -> None:
        credentials = Credentials.from_service_account_file(GOOGLE_KEY_PATH)
        self.client = bigquery.Client(
            # credentials=AnonymousCredentials(),
            credentials=credentials,
            project=project_id,
            # client_options=client_options
        )

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
        table.description = "DEmo Data"

        self.client.create_table(table)

    def insert_table_data(
        self,
        dataset_name: str,
        table_name: str,
        data: list[dict],
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


if __name__ == "__main__":

    # from api.youtube_api import YoutubeApiRequest
    from gcp.gcs import GCS
    BUCKET_NAME = PROJECT_ID

    # youtube = YoutubeApiRequest()
    gcs = GCS(bucket_name=BUCKET_NAME)
    bq = BQ(project_id=PROJECT_ID)
    # youtube.get_youtube_data_to_json()
    # LOCAL_FILE_PATH =
    # f"{youtube.output_path}/{youtube.date_str}_popular.json"
    # GCS_FILE_PATH = f"{gcs.bucket_name}/{youtube.date_str}_popular.json"
    GCS_FILE_PATH = "202305020957_popular.json"

    # gcs.upload_file(
    #     gcs_path=GCS_FILE_PATH,
    #     local_path=LOCAL_FILE_PATH
    # )

    blob = gcs.get_file(GCS_FILE_PATH)

    dataset_name = "videos"
    table_name = "most_popular"

    # print("Deleting Dataset if exists...")
    # bq.client.delete_dataset(dataset_name, not_found_ok=True)
    # bq.generate_dataset(dataset_name)

    print("Deleting table if exists...")
    bq.client.delete_table(f"{dataset_name}.{table_name}", not_found_ok=True)
    bq.generate_table(dataset_name, table_name)

    if blob is not None:
        with blob.open(mode="r", encoding='utf-8') as f:
            data = json.load(f)
            created_at = extract_datetime_from_file_name(blob.name)
            extract_data = extract_most_popular(data, created_at)

    from pprint import pprint
    pprint(extract_data[0])
    bq.insert_table_data(
        dataset_name=dataset_name,
        table_name=table_name,
        data=extract_data,
    )
