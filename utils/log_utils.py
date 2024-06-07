# -*- coding: utf-8 -*-
"""
@Author: ZBY
@date: 2022/6/3
@Description: 日志类
"""
import os
import time
from loguru import logger

from utils.config_utils import BASE_DIR
from config.config import LOG_PATH, ROTATION, RETENTION
from utils.singleton_utils import singleton


def logger_config():
    """
    日志配置
    :return: logger
    """
    _log_path = LOG_PATH
    _rotation = ROTATION
    _retention = RETENTION
    _log_dir = os.path.join(BASE_DIR, _log_path)
    _time = time.strftime('%Y-%m-%d')
    logger.add(
        f"{_log_dir}/{_time}.log",
        rotation=_rotation,
        encoding="utf8",
        enqueue=True,
        retention=_retention,
        format="[{time:YYYY-MM-DD HH:mm:ss}|{thread}|{level}|{file}:{line}]  {message}"
    )
    return logger


@singleton
class Logging(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Logging, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.__logger = logger_config()

    def get_logger(self):
        return self.__logger
