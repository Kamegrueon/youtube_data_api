from enum import StrEnum, auto
from typing import Any, Optional, TypedDict

from pydantic import BaseModel, model_validator


class VideoFilterParams(BaseModel):
    chart: Optional[str] = None
    ids: Optional[list[str]] = None

    @model_validator(mode="before")
    def validate_chart_or_id(cls, values: dict[str, Any]) -> dict[str, Any]:
        chart, ids = values.get("chart"), values.get("id")
        if not chart and not ids:
            raise ValueError('Either "chart" or "id" must be provided.')
        if chart and ids:
            raise ValueError('Only one of "chart" or "id" can be provided.')
        return values


class VideosParams(BaseModel):
    prefix: str
    part: list[str]
    filter: VideoFilterParams
    maxResults: int


class LoadParams(BaseModel):
    prefix: str
    path: str


class ActionUnit(StrEnum):
    store = auto()
    transfer = auto()
    load = auto()


class InvokeRequest(BaseModel):
    action: ActionUnit
    params: VideosParams | LoadParams


class PubsubData(TypedDict):
    action: ActionUnit
    params: LoadParams


class PubsubMessage(BaseModel):
    attributes: Optional[dict[str, str]] = None
    data: str
    messageId: str
    message_id: str
    orderingKey: Optional[str] = None
    publishTime: str
    publish_time: str


class PubsubRequest(BaseModel):
    message: PubsubMessage
    subscription: str
    deliveryAttempt: Optional[int] = None


class ResponseMessage(TypedDict):
    message: str
