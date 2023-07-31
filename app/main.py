from fastapi import FastAPI
from app.core.delayed_tasks import run_delayed_tasks
from app.core.logs import setup_logs

from app.routes import bot_router

app = FastAPI()

app.include_router(bot_router)


@app.on_event('startup')
async def startup_event() -> None:
    setup_logs()
    run_delayed_tasks()