import json

from youtube.youtube_api import YoutubeApiRequest
from env import (
    BUCKET_NAME,
    TOPIC_NAME,
    PROJECT_ID,
    SECRET_ID,
    SECRET_YOUTUBE_API_VERSION,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
)

from gcp.gcs import GcsInterface
from gcp.secretmanager import SecretManagerInterface
from gcp.pubsub import PubSubInterface

from api.schemas.job_request import InvokeRequest

async def transfer(params: InvokeRequest):
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
    res = youtube.get_data(params)
    data = json.dumps(res)

    gcs = GcsInterface(
        project_id=PROJECT_ID,
        bucket_name=BUCKET_NAME,
    )
    file_path = f"{params.prefix}/{youtube.date_str}_{params.prefix}.json"
    gcs.upload_json(file_path, data)

    pubsub = PubSubInterface(
        project_id=PROJECT_ID,
        topic_name=TOPIC_NAME
    )
    pubsub.publish(file_path)