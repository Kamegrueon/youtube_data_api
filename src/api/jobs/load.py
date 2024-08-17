# Standard Library
import json
from typing import Any

# Third Party Library
from loguru import logger

# First Party Library
from api.schemas import LoadParams, ResponseMessage, YouTubeVideoResponse
from env import BUCKET_NAME, ENVIRONMENT, PROJECT_ID
from gcp import BqInterface, GcsInterface
from utils import (
    extract_datetime_from_file_path,
    extract_most_popular,
)


def load_to_bq(prefix: str, extract_data: list[dict[str, Any]]):
    bq = BqInterface(project_id=PROJECT_ID)
    dataset_name = f"{ENVIRONMENT}_videos"
    table_name = f"{ENVIRONMENT}_{prefix}"
    logger.info("Insert Table Data")
    bq.insert_table_data(dataset_name=dataset_name, table_name=table_name, data=extract_data)


def fetch_from_gcs(file_path: str) -> tuple[YouTubeVideoResponse, str]:
    gcs = GcsInterface(project_id=PROJECT_ID, bucket_name=BUCKET_NAME)
    blob = gcs.get_file(file_path)

    if blob is not None:
        with blob.open(mode="r", encoding="utf-8") as f:  # type: ignore
            data: YouTubeVideoResponse = json.load(f)
            created_at = extract_datetime_from_file_path(file_path)
        return data, created_at
    else:
        raise


async def load(params: LoadParams) -> ResponseMessage:
    prefix = params.prefix
    file_path = params.path

    if fetch_from_gcs(file_path):
        data, created_at = fetch_from_gcs(file_path)
    else:
        return {"message": "The file attempted to load was empty."}

    if prefix == "most_popular":
        extract_data = extract_most_popular(data, created_at)
        load_to_bq(prefix, extract_data)
    else:
        raise ValueError(f"Specified prefix({prefix}) does not exist")

    logger.info(f"'{prefix}' has been successfully loaded into BigQuery.")
    return {"message": f"'{prefix}' has been successfully loaded into BigQuery."}
