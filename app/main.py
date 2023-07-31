from fastapi import FastAPI
from app.core.delayed_tasks import run_delayed_tasks

from app.routes import bot_router

app = FastAPI()

app.include_router(bot_router)


@app.on_event('startup')
async def startup_event() -> None:
    run_delayed_tasks()