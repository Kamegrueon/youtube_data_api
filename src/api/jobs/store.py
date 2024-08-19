from datetime import datetime

from api.schemas import InvokeRequest, PrefixUnit, ResponseMessage, VideosParams
from api.schemas.job_request import ActionUnit, VideoFilterParams
from env import (
    ENVIRONMENT,
    PROJECT_ID,
    SECRET_ID,
    SECRET_YOUTUBE_API_VERSION,
    TOPIC_NAME,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
)
from gcp import FirestoreInterface, PubSubInterface, SecretManagerInterface
from youtube.youtube_api import YoutubeApiRequest


def fetch_secret_value() -> str:
    sc = SecretManagerInterface()
    developer_key = sc.get_secret(
        project_id=PROJECT_ID,
        secret_id=SECRET_ID,
        version_id=SECRET_YOUTUBE_API_VERSION,
    )
    return developer_key


def fetch_most_popular_video_ids(developer_key: str, params: VideosParams) -> tuple[list[str], datetime]:
    part, chart, maxResults = (params.part, params.filter.chart, params.maxResults)
    youtube = YoutubeApiRequest(
        youtube_api_service_name=YOUTUBE_API_SERVICE_NAME,
        youtube_api_version=YOUTUBE_API_VERSION,
        developer_key=developer_key,
    )
    if not chart:
        raise ValueError("chart is empty")
    res = youtube.get_most_popular(part, chart, maxResults)
    video_ids = [item["id"] for item in res["items"]]
    processed_at = youtube.processed_at
    return video_ids, processed_at


def get_video_ids_by_time_window(prefix: PrefixUnit, processed_at: datetime, video_ids: list[str]) -> list[str]:
    database_name = "(default)"  # 無料枠利用のため
    client = FirestoreInterface(project_id=PROJECT_ID, database=database_name)
    collection_name = f"{ENVIRONMENT}_{prefix}"

    client.update_video_ids(collection_name=collection_name, processed_at=processed_at, video_ids=video_ids)
    video_ids = client.get_process_video_ids(collection_name=collection_name, processed_at=processed_at)
    return video_ids


def push_to_pubsub(prefix: PrefixUnit, process_video_ids: list[str]) -> None:
    ids = ",".join(process_video_ids)
    part = ",".join(["snippet", "contentDetails", "statistics"])

    pubsub = PubSubInterface(project_id=PROJECT_ID, topic_name=TOPIC_NAME)
    filter_params = VideoFilterParams(ids=ids)
    video_params = VideosParams(prefix=prefix, part=part, filter=filter_params, maxResults=50)
    request = InvokeRequest(action=ActionUnit.transfer, params=video_params)

    pubsub.publish(request.model_dump_json())


async def store(params: VideosParams) -> ResponseMessage:
    prefix = params.prefix
    developer_key = fetch_secret_value()
    get_video_ids, processed_at = fetch_most_popular_video_ids(developer_key, params)
    process_video_ids = get_video_ids_by_time_window(prefix, processed_at, get_video_ids)
    push_to_pubsub(prefix, process_video_ids)

    return {"message": "Store process completed successfully."}
