# Standard Library
import base64
import json

# Third Party Library
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from api.routers import invoke
from loguru import logger

# First Party Library
from youtube.youtube_api import YoutubeApiRequest
from env import (
    BUCKET_NAME,
    TOPIC_NAME,
    PROJECT_ID,
    SECRET_ID,
    SECRET_YOUTUBE_API_VERSION,
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    ENVIRONMENT
)
from gcp.bq import BqInterface
from gcp.gcs import GcsInterface
from gcp.secretmanager import SecretManagerInterface
from gcp.pubsub import PubSubInterface
from utils.extract_most_popular import (
    extract_datetime_from_file_path,
    extract_most_popular,
)
from api.schemas.job_request import PubsubRequest

app = FastAPI()
app.include_router(invoke.router)

# flake8: noqa

def check_pubsub_message(request) -> str:
    envelope = json.loads(request.json())
    logger.info(f"envelope: {envelope} type: {type(envelope)}")
    if not envelope:
        msg = "no Pub/Sub message received"
        logger.info(f"error: {msg}")
        raise HTTPException(status_code=400, detail=f"Bad Request: {msg}")

    if not isinstance(envelope, dict) and "message" not in envelope:
        msg = "invalid Pub/Sub message format"
        logger.info(f"error: {msg}")
        raise HTTPException(status_code=400, detail=f"Bad Request: {msg}")

    pubsub_message = envelope["message"]
    logger.info(f"{pubsub_message}")
    text = ""
    if isinstance(pubsub_message, dict) and "data" in pubsub_message:
        text = base64.b64decode(
            pubsub_message["data"]).decode("utf-8").strip()
    logger.info(f"PubSubMsg Is {text}")
    return text


@app.post("/invoke/load")
async def invoke_load_to_bq(background_tasks: BackgroundTasks, request: PubsubRequest) -> dict[str, str]:
    file_path = check_pubsub_message(request)
    background_tasks.add_task(load_bq, file_path)
    return {"message": "Message received and processing started BQ Load."}


async def load_bq(file_path):
    gcs = GcsInterface(project_id=PROJECT_ID, bucket_name=BUCKET_NAME)
    bq = BqInterface(project_id=PROJECT_ID)
    blob = gcs.get_file(file_path)

    dataset_name = f"{ENVIRONMENT}_videos"
    table_name = f"{ENVIRONMENT}_most_popular"

    if blob is not None:
        with blob.open(mode="r", encoding='utf-8') as f:
            data = json.load(f)

            created_at = extract_datetime_from_file_path(file_path)
            extract_data = extract_most_popular(data, created_at)

        logger.info("Insert Table Data")
        bq.insert_table_data(
            dataset_name=dataset_name,
            table_name=table_name,
            data=extract_data
    )
