from fastapi import APIRouter, BackgroundTasks, HTTPException, Request, Response, status
from loguru import logger

from app.core import settings
from app.core.bot import BaseBot, main_bot
from app.core.constants import BotTypes

bot_router = APIRouter(prefix='/vk-bots')


@bot_router.post('/{bot_type}')
async def bots_handler(bot_type: str, request: Request, background_task: BackgroundTasks) -> Response:
    data = await try_get_data(request)
    bot, confrimation_code = get_bot_and_code(bot_type)
    if is_confirmation(data):
        return Response(confrimation_code)
    validate_secret_key(data)
    background_task.add_task(bot.process_event, data)
    return Response('ok')


async def try_get_data(request: Request) -> dict:
    try:
        return await request.json()
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Body is invalid')


def is_confirmation(data: dict) -> bool:
    if data.get('type') == 'confirmation':
        return True
    return False


def validate_secret_key(data: dict) -> None:
    if data.get('secret') != settings.SECRET_KEY:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Secret key is invalid')


def get_bot_and_code(bot_type: str) -> tuple[BaseBot, str]:
    match bot_type:
        case BotTypes.MAIN:
            return main_bot, settings.MAIN_CONFIRMATION_CODE
    raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Invalid bot type')
