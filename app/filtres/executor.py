from copy import deepcopy

from loguru import logger

from app.filtres.abc import ABCFilter


def execute_filters(data, filters: list[ABCFilter]) -> bool:
    copied_data = deepcopy(data)
    for filter in filters:
        if not filter(copied_data):
            logger.debug(f'{filter}: {copied_data} is false')
            return False
    return True
