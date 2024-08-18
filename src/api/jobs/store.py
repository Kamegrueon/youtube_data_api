import json

from api.schemas import ResponseMessage, VideosParams
from env import (
    PROJECT_ID,
    SECRET_ID,
    SECRET_YOUTUBE_API_VERSION,
    TOPIC_NAME,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
)
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


def fetch_youtube_data(developer_key: str, params: VideosParams) -> tuple[str, str]:
    part, chart, maxResults = (params.part, params.filter.chart, params.maxResults)
    youtube = YoutubeApiRequest(
        youtube_api_service_name=YOUTUBE_API_SERVICE_NAME,
        youtube_api_version=YOUTUBE_API_VERSION,
        developer_key=developer_key,
    )
    if not chart:
        raise ValueError("chart is empty")
    res = youtube.get_most_popular(part, chart, maxResults)
    data = json.dumps(res)
    return data, youtube.date_str


def create_firestore(file_path: str, data: str) -> int:
    return 200


def push_to_pubsub(prefix: str, file_path: str) -> None:
    pubsub = PubSubInterface(project_id=PROJECT_ID, topic_name=TOPIC_NAME)

    message = json.dumps({"action": "transfer", "params": {"prefix": prefix, "": file_path}})
    pubsub.publish(message)


async def store(params: VideosParams) -> ResponseMessage:
    prefix = params.prefix
    developer_key = fetch_secret_value()
    data, request_date = fetch_youtube_data(developer_key, params)

    file_path = f"{prefix}/{request_date}_{prefix}.json"
    status = create_firestore(file_path, data)
    # status = transfer_gcs(file_path, data)

    if status == 200:
        push_to_pubsub(prefix, file_path)
        return {"message": "Transfer process completed successfully."}
    else:
        return {"message": "Transfer process failed."}
