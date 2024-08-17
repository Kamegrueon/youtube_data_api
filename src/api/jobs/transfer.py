import json

from api.schemas import ResponseMessage, TransferParams
from env import (
    BUCKET_NAME,
    PROJECT_ID,
    SECRET_ID,
    SECRET_YOUTUBE_API_VERSION,
    TOPIC_NAME,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
)
from gcp.gcs import GcsInterface
from gcp.pubsub import PubSubInterface
from gcp.secretmanager import SecretManagerInterface
from youtube.youtube_api import YoutubeApiRequest


def fetch_secret_value() -> str:
    sc = SecretManagerInterface()
    developer_key = sc.get_secret(
        project_id=PROJECT_ID,
        secret_id=SECRET_ID,
        version_id=SECRET_YOUTUBE_API_VERSION,
    )
    return developer_key


def fetch_youtube_data(developer_key: str, params: TransferParams):
    part, chart, maxResults = (params.part, params.chart, params.maxResults)
    youtube = YoutubeApiRequest(
        youtube_api_service_name=YOUTUBE_API_SERVICE_NAME,
        youtube_api_version=YOUTUBE_API_VERSION,
        developer_key=developer_key,
    )
    res = youtube.get_data(part, chart, maxResults)
    data = json.dumps(res)
    return data, youtube.date_str


def transfer_gcs(file_path: str, data: str) -> int:
    gcs = GcsInterface(
        project_id=PROJECT_ID,
        bucket_name=BUCKET_NAME,
    )

    try:
        gcs.upload_json(file_path, data)
        return 200
    except Exception as e:
        raise RuntimeError(f"Failed to upload JSON to GCS at {file_path}: {e}")


def push_to_pubsub(prefix: str, file_path: str):
    pubsub = PubSubInterface(project_id=PROJECT_ID, topic_name=TOPIC_NAME)

    message = json.dumps(
        {"action": "load", "params": {"prefix": prefix, "path": file_path}}
    )
    pubsub.publish(message)


async def transfer(params: TransferParams) -> ResponseMessage:
    prefix = params.prefix
    developer_key = fetch_secret_value()
    data, request_date = fetch_youtube_data(developer_key, params)

    file_path = f"{prefix}/{request_date}_{prefix}.json"
    status = transfer_gcs(file_path, data)

    if status == 200:
        push_to_pubsub(prefix, file_path)
        return {"message": "Transfer process completed successfully."}
    else:
        return {"message": "Transfer process failed."}
