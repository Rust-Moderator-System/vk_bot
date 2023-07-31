from __future__ import annotations

from loguru import logger


def add_debug_file_log() -> None:
    logger.add('logs/debug.log', rotation='1 week', level='DEBUG')


def add_info_file_log() -> None:
    logger.add('logs/info.log', rotation='500mb', level='INFO')


def setup_logs():
    add_debug_file_log()
    add_info_file_log()