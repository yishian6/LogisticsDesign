# -*- coding: utf-8 -*-
"""
@Author: ZBY
@date: 2022/6/3
@Description: 程序中定义的一些异常类，如数据库连接异常等
"""
import traceback

from common import tag_name


class TopException(Exception):
    """
    项目中自定义的异常的顶层基类，包括异常堆栈的打印，error code和error msg的格式化输出
    """

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg
        super().__init__(self, code, msg)

    @property
    def trace_back(self):
        return traceback.format_exc()

    def __str__(self):
        return f"error code: [{self.code}]; err msg: [{self.msg}]"


class DBException(TopException):
    def __init__(self, code=tag_name.DB_CONNECT_ERROR, msg="db connect error."):
        self.code = code
        self.msg = msg
        super(DBException, self).__init__(self.code, self.msg)


class SessionException(TopException):
    def __init__(self, code=tag_name.SESSION_OPERATOR_ERROR, msg="db session operator failed."):
        self.code = code
        self.msg = msg
        super(SessionException, self).__init__(self.code, self.msg)


class InputParamException(TopException):
    def __init__(self, code=tag_name.INPUT_PARAM_ERROR, msg="input param is invalid."):
        self.code = code
        self.msg = msg
        super(InputParamException, self).__init__(self.code, self.msg)


class IOException(TopException):
    def __init__(self, code=tag_name.IO_STREAM_ERROR, msg="file operation failed."):
        self.code = code
        self.msg = msg
        super(IOException, self).__init__(self.code, self.msg)


class TrainModelException(TopException):
    def __init__(self, code=tag_name.TRAIN_MODEL_ERROR, msg="classify model train failed."):
        self.code = code
        self.msg = msg
        super(TrainModelException, self).__init__(self.code, self.msg)


class ModelPredictException(TopException):
    def __init__(self, code=tag_name.MODEL_PREDICT_ERROR, msg="classify model predict failed."):
        self.code = code
        self.msg = msg
        super(ModelPredictException, self).__init__(self.code, self.msg)


class ESException(TopException):
    def __init__(self, code=tag_name.ES_CONNECT_ERROR, msg="elasticsearch connect error."):
        self.code = code
        self.msg = msg
        super(ESException, self).__init__(self.code, self.msg)


class ClassNotFoundException(TopException):
    def __init__(self, code=tag_name.CLASS_NOT_FOUND_ERROR, msg="class not found."):
        self.code = code
        self.msg = msg
        super(ClassNotFoundException, self).__init__(self.code, self.msg)


class MethodNotFoundException(TopException):
    def __init__(self, code=tag_name.METHOD_NOT_FOUND_ERROR, msg="Method not found."):
        self.code = code
        self.msg = msg
        super(MethodNotFoundException, self).__init__(self.code, self.msg)


class JsonException(TopException):
    def __init__(self, code=tag_name.METHOD_NOT_FOUND_ERROR, msg="Json load error."):
        self.code = code
        self.msg = msg
        super(JsonException, self).__init__(self.code, self.msg)


class IndexOutOfRangeException(TopException):
    def __init__(self, code=tag_name.INDEX_OUT_OF_RANGE_ERROR, msg="index out of range."):
        self.code = code
        self.msg = msg
        super(IndexOutOfRangeException, self).__init__(self.code, self.msg)


class ExcelToSqlException(TopException):
    def __init__(self, code=tag_name.EXCEL_TO_SQL_ERROR, msg="excel to sql error."):
        self.code = code
        self.msg = msg
        super(ExcelToSqlException, self).__init__(self.code, self.msg)


class DBInitDropException(TopException):
    def __init__(self, code=tag_name.DB_INIT_DROP_ERROR, msg="database init drop table error."):
        self.code = code
        self.msg = msg
        super(DBInitDropException, self).__init__(self.code, self.msg)


class DBInitCreateException(TopException):
    def __init__(self, code=tag_name.DB_INIT_CREATE_ERROR, msg="database init create table error."):
        self.code = code
        self.msg = msg
        super(DBInitCreateException, self).__init__(self.code, self.msg)


class DBUpdateException(TopException):
    def __init__(self, code=tag_name.DB_UPDATE_ERROR, msg="excel data update to database error."):
        self.code = code
        self.msg = msg
        super(DBUpdateException, self).__init__(self.code, self.msg)


class RenameFileException(TopException):
    def __init__(self, code=tag_name.RENAME_FILE_ERROR, msg="rename file error."):
        self.code = code
        self.msg = msg
        super(RenameFileException, self).__init__(self.code, self.msg)


class MailSendError(TopException):
    def __init__(self, code=tag_name.MAIL_SEND_ERROR, msg="send mail error."):
        self.code = code
        self.msg = msg
        super(MailSendError, self).__init__(self.code, self.msg)


class MailSendSuccess(TopException):
    def __init__(self, code=tag_name.MAIL_SEND_SUCCESS, msg="send mail success."):
        self.code = code
        self.msg = msg
        super(MailSendSuccess, self).__init__(self.code, self.msg)
