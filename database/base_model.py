# -*- coding: utf-8 -*-
"""
@Author: ZBY
@date: 2023/6/4
@Description: 所有orm类继承的基类，orm类的操作需要配合事务管理使用
"""
from typing import Dict, Iterable

from common.base_exception import InputParamException
from database.db_connection import TransactionalSession
from utils.log_utils import Logging

log = Logging().get_logger()
t = TransactionalSession()


class BaseOrmModel(object):
    """
    orm类的基类
    """
    _db_name = None

    def add(self) -> None:
        """ orm, sql插入
        eg: a = MerchantBillDetail(id=1)
            a.add()
        :return: None
        """
        add_session = t.get_session()
        if add_session is None:
            raise InputParamException(msg="g_session must initialize!")
        log.info(f"session [{id(add_session)}] and [{self.__class__.__name__}] has an operator: ADD.")
        add_session.add(self)

    @classmethod
    def batch_add(cls, objs) -> None:
        """批量增加.
        eg: a = [MerchantBillDetail(id=1), MerchantBillDetail(id=2)]
            MerchantBillDetail.batch_add(a)
        :param objs: 增加的orm对象
        :return: None
        """
        batch_add_session = t.get_session()
        if batch_add_session is None:
            raise InputParamException(msg="g_session must initialize!")
        log.info(f"session [{id(batch_add_session)}] and [{cls.__name__}] has an operator: ADD BATCH.")
        batch_add_session.add_all(objs)

    @classmethod
    def delete(cls, where_conditions) -> None:
        """条件下的删除
        eg: BaseModel.delete([BaseModel.a>1, BaseModel.b==2])
        :param where_conditions: 条件语句, list
        :return: None
        """
        delete_session = t.get_session()
        if delete_session is None:
            raise InputParamException(msg="g_session must initialize!")
        log.info(f"session [{id(delete_session)}] and [{cls.__name__}] has an operator: DELETE.")
        delete_session.query(cls).filter(*where_conditions).delete(synchronize_session='fetch')

    @classmethod
    def update(cls, update_dict: Dict, where_conditions):
        """
        更新.
        eg: BaseModel.update({'name': 'jack'}, [BaseModel.id>=1])
        :param update_dict: 需要更新的orm键值对
        :param where_conditions: where条件
        :return: None
        """
        update_session = t.get_session()
        if update_session is None:
            raise InputParamException(msg="g_session must initialize!")
        log.info(f"session [{id(update_session)}] and [{cls.__name__}] has an operator: UPDATE.")
        update_session.query(cls).filter(*where_conditions).update(
            update_dict,
            synchronize_session='fetch')

    @classmethod
    def query(cls, params, **where_conditions):
        """高级查询，按照指定的条件进行查询，返回一个或者多个结果，子类可以重写该方法
        eg: BaseModel.query([BaseModel.id, BaseModel.name],
                filter=[BaseModel.id>=1],
                group_by=[BaseModel.id, BaseModel.name]
                order_by=BaseModel.id.desc(), limit=10, offset=0)
        :param params: 查询参数
        :param where_conditions: 根据参数的where语句
        :return: 结果对象
        """
        query_session = t.get_session()
        log.info(f"session [{id(query_session)}] and [{cls.__name__}] has an operator: QUERY.")
        if not where_conditions:
            if not set(where_conditions.keys()).issubset(
                    {'filter', 'group_by', 'having', 'order_by', 'limit', 'offset'}):
                raise InputParamException
        c_filter = where_conditions.pop('filter', None)
        group_para = where_conditions.pop('group_by', None)
        having = where_conditions.pop('having', None)
        order_para = where_conditions.pop('order_by', None)
        limit = where_conditions.pop('limit', None)
        offset = where_conditions.pop('offset', None)
        query_first = where_conditions.get('query_first', False)

        if not isinstance(params, Iterable):
            params = [params]
        s_query = query_session.query(*params)
        if c_filter is not None:
            s_query = s_query.filter(*c_filter)
        if group_para is not None:
            s_query = s_query.group_by(*group_para)
        if having is not None:
            s_query = s_query.having(having)
        if order_para is not None:
            s_query = s_query.order_by(order_para)
        if limit is not None:
            s_query = s_query.limit(limit)
        if offset is not None:
            s_query = s_query.offset(offset)
        if query_first:
            return s_query.first()
        return s_query.all()

    @classmethod
    def execute(cls, sql_str):
        """
        执行原生sql
        :param sql_str: sql
        :return: 执行后结果
        """
        execute_session = t.get_session()
        if execute_session is None:
            raise InputParamException(msg="g_session must initialize!")
        log.info(f"session [{id(execute_session)}] and [{cls.__name__}] has an operator: EXEC SQL.")
        return execute_session.execute(sql_str)
