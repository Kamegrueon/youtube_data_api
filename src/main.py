from fastapi import FastAPI

from api.routers import invoke

app = FastAPI()
app.include_router(invoke.router)
