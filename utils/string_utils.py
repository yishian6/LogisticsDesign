# -*- coding: utf-8 -*-
"""
@Author: ZBY
@date: 2022/8/6
@Description: 字符串相关工具类
"""


class StringUtils(object):

    @staticmethod
    def regex_replace(string):
        """
        对输入字符串格式化
        :return: 新的字符串
        """
        pass

    @staticmethod
    def trim_character(string: str):
        new_string = string.replace("\r\n", "").replace("\r", "").replace("\n", "").strip()
        return new_string
