# -*- coding: utf-8 -*-
"""
@Author: ZBY
@date: 2022/6/3
@Description: flask api 异常类定义
"""
from common import tag_name
from common.tag_name import Index_View_Error


class ApiException(Exception):
    """
    自定义异常类
    """

    def __init__(self, code: int, message: str, data=None):
        """
        初始化
        :param code: 状态码
        :param message: 异常信息
        :param data: 返回数据
        """
        self.code = code
        self.message = message
        self.data = data

    def __str__(self):
        """
        重写异常类的 __str__ 方法
        :return: 异常信息
        """
        return f"code: {self.code}, message: {self.message}, data: {self.data}"


class IndexViewException(ApiException):
    """
    index_view页面中的异常类
    """

    def __init__(self, code=tag_name.Index_View_Error, msg="index view error."):
        self.code = code
        self.msg = msg
        super(IndexViewException, self).__init__(self.code, self.msg)
