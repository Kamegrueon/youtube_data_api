from typing import Optional, TypedDict

from pydantic import BaseModel


class TransferParams(BaseModel):
    prefix: str
    part: str
    chart: str
    maxResults: int


class LoadParams(BaseModel):
    prefix: str
    path: str


class InvokeRequest(BaseModel):
    action: str
    params: TransferParams | LoadParams


class PubsubData(TypedDict):
    action: str
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
