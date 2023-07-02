from fastapi import FastAPI

from app.routes import bot_router

app = FastAPI()

app.include_router(bot_router)