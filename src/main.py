import json
from pprint import pprint
from api.youtube_api import YoutubeApiRequest
from gcp.gcs import GCS
from gcp.bq import BQ
from gcp.config.gcp_config import PROJECT_ID, BUCKET_NAME
from utils.extract_most_popular import (
    extract_most_popular,
    extract_datetime_from_file_name
)


def main() -> None:
    youtube = YoutubeApiRequest()
    gcs = GCS(bucket_name=BUCKET_NAME)
    bq = BQ(project_id=PROJECT_ID)

    # ローカルにJSONファイルで保存
    youtube.get_youtube_data_to_json()

    local_file_path = f"{youtube.output_path}/{youtube.date_str}_popular.json"
    folder_path = f"{gcs.bucket_name}/most_popular/"
    gcs_file_path = f"{folder_path}{youtube.date_str}_popular.json"

    # ローカルのJSONファイルを取得してGCSにupload
    gcs.upload_file(
        gcs_path=gcs_file_path,
        local_path=local_file_path,
    )

    # GCSにuploadしたファイルを取得
    blob = gcs.get_file(gcs_file_path)

    dataset_name = "videos"
    table_name = "most_popular"

    # print("Deleting table if exists...")
    # bq.client.delete_table(f"{dataset_name}.{table_name}", not_found_ok=True)
    # bq.generate_table(dataset_name, table_name)

    if blob is not None:
        with blob.open(mode="r", encoding='utf-8') as f:
            data = json.load(f)

            created_at = extract_datetime_from_file_name(youtube.date_str)
            extract_data = extract_most_popular(data, created_at)

    pprint(extract_data[0])
    bq.insert_table_data(
        dataset_name=dataset_name,
        table_name=table_name,
        data=extract_data,
    )


if __name__ == "__main__":
    main()
