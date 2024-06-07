# -*- coding: utf-8 -*-
"""
@Author: ZBY
@date: 2022/6/3
@Description: 配置类读取，包含一些项目常用关键全局变量
"""
import configparser
import os

# 项目根路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 项目主体配置文件
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "config", "config.ini")
# 项目文件路径
FILE_SYSTEM_URL = os.path.join(BASE_DIR, "data", "FSStorage")


class ConfigUtils(object):
    """
    项目配置文件读取类
    """

    @staticmethod
    def _get_config_items():
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH)
        return config

    @staticmethod
    def get(section, item):
        """
        获取config.ini中某一个section中的item的值
        :param section: 如[Log]就是一个section
        :param item: 如[Log]中的logPath就是一个item
        :return: value, 获取到的值
        """
        config = ConfigUtils._get_config_items()
        value = config.get(section, item)
        return value
