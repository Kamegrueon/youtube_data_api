# Standard Library
import base64
import json

# Third Party Library
from fastapi import FastAPI, HTTPException, Request

# First Party Library
from api.youtube_api import YoutubeApiRequest
from env import (
    BUCKET_NAME,
    PROJECT_ID,
    SECRET_ID,
    SECRET_YOUTUBE_API_VERSION,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
)
from gcp.bq import BqInterface
from gcp.gcs import GcsInterface
from gcp.secretmanager import SecretManagerInterface
from utils.extract_most_popular import (
    extract_datetime_from_file_path,
    extract_most_popular,
)

app = FastAPI()


@app.get("/invoke/transfer")
def invoke_transfer_to_gcs() -> str:
    sc = SecretManagerInterface()
    developer_key = sc.get_secret(
        project_id=PROJECT_ID,
        secret_id=SECRET_ID,
        version_id=SECRET_YOUTUBE_API_VERSION
    )

    youtube = YoutubeApiRequest(
        youtube_api_service_name=YOUTUBE_API_SERVICE_NAME,
        youtube_api_version=YOUTUBE_API_VERSION,
        developer_key=developer_key
    )

    res = youtube.get_youtube_data()
    data = json.dumps(res)

    gcs = GcsInterface(
        project_id=PROJECT_ID,
        bucket_name=BUCKET_NAME,
    )
    file_path = f"most_popular/{youtube.date_str}_popular.json"
    gcs.upload_json(file_path, data)
    return file_path


@app.get("/invoke/load")
def invoke_load_to_bq(request: Request) -> None:

    envelope = request.json()
    if not envelope:
        msg = "no Pub/Sub message received"
        print(f"error: {msg}")
        raise HTTPException(status_code=400, detail=f"Bad Request: {msg}")

    if not isinstance(envelope, dict) or "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        print(f"error: {msg}")
        raise HTTPException(status_code=400, detail=f"Bad Request: {msg}")

    pubsub_message = envelope["message"]
    file_path = ""
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        file_path = base64.b64decode(
            pubsub_message["data"]).decode("utf-8").strip()

    gcs = GcsInterface(project_id=PROJECT_ID, bucket_name=BUCKET_NAME)
    bq = BqInterface(project_id=PROJECT_ID)
    blob = gcs.get_file(file_path)

    dataset_name = "videos"
    table_name = "most_popular"

    print("Deleting table if exists...")
    bq.client.delete_table(f"{dataset_name}.{table_name}", not_found_ok=True)
    bq.generate_table(dataset_name, table_name)

    if blob is not None:
        with blob.open(mode="r", encoding='utf-8') as f:
            data = json.load(f)

            created_at = extract_datetime_from_file_path(file_path)
            extract_data = extract_most_popular(data, created_at)

    bq.insert_table_data(
        dataset_name=dataset_name,
        table_name=table_name,
        data=extract_data,
    )

# def main() -> None:
#     youtube = YoutubeApiRequest()
#     gcs = GCS(bucket_name=BUCKET_NAME)
#     bq = BQ(project_id=PROJECT_ID)

#     # ローカルにJSONファイルで保存
#     youtube.get_youtube_data_to_json()

#     local_file_path = f"{youtube.local_path}/{youtube.date_str}_popular.json"
#     gcs_file_path = f"most_popular/{youtube.date_str}_popular.json"

#     # ローカルのJSONファイルを取得してGCSにupload
#     gcs.upload_file(
#         gcs_path=gcs_file_path,
#         local_path=local_file_path,
#     )

#     # GCSにuploadしたファイルを取得
#     blob = gcs.get_file(gcs_file_path)

#     dataset_name = "videos"
#     table_name = "most_popular"

#     # print("Deleting table if exists...")
#     # bq.client.delete_table(f"{dataset_name}.{table_name}",
#                               not_found_ok=True)
#     # bq.generate_table(dataset_name, table_name)

#     if blob is not None:
#         with blob.open(mode="r", encoding='utf-8') as f:
#             data = json.load(f)

#             created_at = extract_datetime_from_file_name(youtube.date_str)
#             extract_data = extract_most_popular(data, created_at)

#     pprint(extract_data[0])
#     bq.insert_table_data(
#         dataset_name=dataset_name,
#         table_name=table_name,
#         data=extract_data,
#     )


# if __name__ == "__main__":
#     main()
