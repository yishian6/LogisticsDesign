import functools
import os
import traceback
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from common import base_exception
from common.base_exception import TopException
from config.config import config

from utils.log_utils import Logging
from utils.singleton_utils import singleton

log = Logging().get_logger()
result = None
config = config[os.getenv('FLASK_DEBUG') or 'default']()


@singleton
class TransactionalSession:
    def __init__(self, pool_size=20):
        # 连接池
        SQLALCHEMY_DATABASE_URI = config.SQLALCHEMY_DATABASE_URI
        self.engine = create_engine(
            SQLALCHEMY_DATABASE_URI,
            connect_args={'charset': 'utf8mb4'}, pool_size=pool_size, max_overflow=5, pool_recycle=60,
            pool_pre_ping=True)
        # session工厂
        self.session_factory = sessionmaker(
            bind=self.engine,
            expire_on_commit=False)
        # 线程安全对象
        self.trans_session = scoped_session(self.session_factory)

    def transaction(self, func):
        """
        装饰器实现事务管理
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            session = self.get_session()
            try:
                # with session.begin():
                res = func(*args, **kwargs)
                session.commit()
                return res
            # 异常还是需要打印一下的
            except TopException as e:
                log.error(f"[Project Except]transaction function error, info is{e.msg}")
                session.rollback()
                raise e
            except Exception as e:
                log.error(f"[Except]transaction function error, info is {str(e)}")
                log.error(f"{traceback.format_exc()}")
                session.rollback()
                raise e
            finally:
                self.trans_session.remove()

        return wrapper

    @staticmethod
    def execute_sql(session, str_sql):
        global result
        try:
            result = 0
            sql_execute_res = session.execute(str_sql)
            if "select" in str_sql.lower():
                result = sql_execute_res.fetchall()
            elif "insert" in str_sql.lower():
                log.info(f"{sql_execute_res.rowcount} rows have been inserted.")
                result = sql_execute_res.rowcount
            elif "update" in str_sql.lower():
                log.info(f"{sql_execute_res.rowcount} rows have been updated.")
                result = sql_execute_res.rowcount
            elif "delete" in str_sql.lower():
                log.info(f"{sql_execute_res.rowcount} rows have been deleted.")
                result = sql_execute_res.rowcount
            session.commit()
            return result
            # 异常还是需要打印一下的
        except Exception:
            log.error(f"errmsg is : {traceback.format_exc()}")
            session.rollback()
            raise base_exception.SessionException
        finally:
            session.close()

    def get_session(self):
        return self.trans_session()
