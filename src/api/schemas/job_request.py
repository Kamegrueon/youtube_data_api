from typing import Optional
from pydantic import BaseModel

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


class InvokeRequest(BaseModel):
    prefix: str
    part: str
    chart: str
    maxResults: int
