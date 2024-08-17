from api.routers import invoke
from fastapi import FastAPI

app = FastAPI()
app.include_router(invoke.router)
