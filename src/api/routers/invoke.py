import json

from fastapi import APIRouter, BackgroundTasks, Request
from api.jobs.transfer import transfer
from api.schemas.job_request import InvokeRequest

router = APIRouter()

@router.post("/invoke/transfer")
async def invoke_transfer(background_tasks: BackgroundTasks, request: InvokeRequest) -> dict[str, str]:

    background_tasks.add_task(transfer, request)
    return {"message": "Message received and processing started API Fetch to Save."}