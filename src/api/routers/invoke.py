from api.jobs import load, transfer
from api.schemas.job_request import (
    InvokeRequest,
    LoadParams,
    PubsubRequest,
    TransferParams,
)
from fastapi import APIRouter, BackgroundTasks
from loguru import logger
from utils import decode_pubsub_message

router = APIRouter()


@router.post("/invoke")
async def invoke(
    background_tasks: BackgroundTasks, request: InvokeRequest | PubsubRequest
) -> dict[str, str]:
    data: InvokeRequest
    if isinstance(request, PubsubRequest):
        decode_value = decode_pubsub_message(request)
        try:
            data = InvokeRequest(
                action=decode_value["action"], params=decode_value["params"]
            )
        except ValueError as e:
            logger.error(f"Value Error{e}")
        except KeyError as e:
            logger.error(f"Key Error{e}")
    elif isinstance(request, InvokeRequest):
        data = request

    logger.info(data)

    action, params = data.action, data.params

    if action == "transfer" and isinstance(params, TransferParams):
        background_tasks.add_task(transfer, params)
    elif action == "load" and isinstance(params, LoadParams):
        background_tasks.add_task(load, params)
    else:
        raise ValueError(
            f"Invalid combination of action '{action}' and params type '{type(params).__name__}'"
        )

    return {"message": "Message received and processing '{action}'."}
