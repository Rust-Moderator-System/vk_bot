from copy import deepcopy

from loguru import logger

from app.filtres.abc import ABCFilter


def execute_filters(data, filters: list[ABCFilter]) -> bool:
    for filter in filters:
        if not filter(deepcopy(data)):
            logger.debug(f'{filter}: {data} is false')
            return False
    return True
