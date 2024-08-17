import base64
import json

from api.schemas import PubsubData, PubsubRequest


def decode_pubsub_message(request: PubsubRequest) -> PubsubData:
    data = json.loads(base64.b64decode(request.message.data).decode("utf-8").strip())

    return data
