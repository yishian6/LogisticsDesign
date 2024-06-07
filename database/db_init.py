import traceback
import os
import pandas as pd
from sqlalchemy import inspect

from common.base_exception import ExcelToSqlException, DBInitDropException, \
    DBInitCreateException
from database.models import Vehicle, Part, RegressPredict, PartOptimize, Transport, TransportCost, EmptyCar
from utils.config_utils import BASE_DIR
from database.models import Base
from utils.log_utils import Logging
from database.db_connection import TransactionalSession

t = TransactionalSession()
engine = t.engine
log = Logging().get_logger()

part_path = os.path.join(BASE_DIR, 'data', 'sqlData', '零件数据统计.xlsx')
part_optimize_path = os.path.join(BASE_DIR, 'data', 'sqlData', '零件网络优化.xlsx')
vehicle_path = os.path.join(BASE_DIR, 'data', 'sqlData', '整车数据统计.xlsx')
regress_predict_path = os.path.join(BASE_DIR, 'data', 'sqlData', 'regress_predict.xlsx')
transport_path = os.path.join(BASE_DIR, 'data', 'sqlData', 'transport.xlsx')
transport_cost_path = os.path.join(BASE_DIR, 'data', 'sqlData', '运输成本.xlsx')
empty_car_path = os.path.join(BASE_DIR, 'data', 'sqlData', 'empty_car.xlsx')

# 定义新的列名
column_names_part = {
    "供应商名称": "supplier_name",
    '供应商地址': "supplier_addr",
    "省": "prov",
    "市": "city",
    '发往方向': "dest",
    "货车直运距离(m)": "distance",
    '货量（m³/年）': "quantity"
}
column_names_part_optimize = {
    "省": "prov",
    "城市": "city",
    "长春": "cc",
    "成都": "cd",
    "佛山": "fs",
    "青岛": "qd",
    "天津": "tj",
    "大连": "dl",
    "运货成本（元）": "cost",
    "方案": "programme",
    "方法": "method"
}

column_names_vehicle = {
    "省份": "prov",
    "城市": "city",
    "销售量（辆/年）": "sales",
    "经销店数量": "dealership_num"
}

column_names_regress = {
    "operate": "operate",
    "regress_data": "regress_data",
    "create_time": "create_time"
}

column_names_transport = {
    "route": "route",
    "site_type": "site_type",
    "highway": "highway",
    "railway": "railway",
    "waterway": "waterway"
}

column_names_transport_cost = {
    "分拨节点": "site", "历史销量(年)": "history_sales", "对应省/市销量(年)": "pro_sales",
    "吞吐量(年)": "throughput", "该省辐射的成本": "cost", "优化吞吐量": "o_throughput",
    "优化辐射成本": "o_cost", "类别": "type", "是否受限": "is_limit", "方法": "method"
}

column_names_empty_car = {
    "method": "method", "sales1": "sales1", "tt": "tt", "st": "st", "cost1": "cost1",
    "sales2": "sales2", "cost2": "cost2", "save_car": "save_car", "save_mileage": "save_mileage",
    "extra_cost": "extra_cost", "save_cost": "save_cost", "all_cost": "all_cost", "site": "site",
    "month": "month", "city": "city"
}


class DB:
    @staticmethod
    def drop_table():
        """
        判断 my_table 是否存在，如果存在则删除
        """
        insp = inspect(engine)
        try:
            if insp.has_table(Vehicle.__tablename__):
                Base.metadata.tables[Vehicle.__tablename__].drop(engine)
            if insp.has_table(Part.__tablename__):
                Base.metadata.tables[Part.__tablename__].drop(engine)
            if insp.has_table(PartOptimize.__tablename__):
                Base.metadata.tables[PartOptimize.__tablename__].drop(engine)
            if insp.has_table(RegressPredict.__tablename__):
                Base.metadata.tables[RegressPredict.__tablename__].drop(engine)
            if insp.has_table(Transport.__tablename__):
                Base.metadata.tables[Transport.__tablename__].drop(engine)
            if insp.has_table(TransportCost.__tablename__):
                Base.metadata.tables[TransportCost.__tablename__].drop(engine)
            if insp.has_table(EmptyCar.__tablename__):
                Base.metadata.tables[EmptyCar.__tablename__].drop(engine)
            log.info('drop my table successfully')
        except Exception:
            raise DBInitDropException

    @staticmethod
    def create_table():
        try:
            Base.metadata.create_all(engine)
            log.info('create my table successfully')
        except Exception:
            raise DBInitCreateException

    @staticmethod
    def data_init():
        DB.excel_to_sql(part_path, column_names_part, 'part')
        DB.excel_to_sql(part_optimize_path, column_names_part_optimize, 'part_optimize')
        DB.excel_to_sql(vehicle_path, column_names_vehicle, 'vehicle')
        DB.excel_to_sql(regress_predict_path, column_names_regress, 'regress_predict')
        DB.excel_to_sql(transport_path, column_names_transport, 'transport')
        DB.excel_to_sql(transport_cost_path, column_names_transport_cost, 'transport_cost')
        DB.excel_to_sql(empty_car_path, column_names_empty_car, 'empty_car')

    @staticmethod
    def excel_to_sql(excel_path, column_names, mysql_table_name, way='append'):
        """
        将excel文件中数据导入数据库
        :param excel_path: excel路径
        :param column_names: 中英标题名的字典
        :param mysql_table_name: 数据表表名
        :param if_exists: 默认覆盖表中数据
        :return: None
        """
        try:
            # log.info("excel to sql begin")
            data = pd.read_excel(excel_path, engine='openpyxl')
            # if_exists三个模式：fail，若表存在，则不输出；replace：若表存在，覆盖原来表里的数据；append：若表存在，将数据写到原表的后面。
            data.rename(columns=column_names).to_sql(name=mysql_table_name, con=engine, index=False, if_exists=way)
            log.info(f'Import excel data [{mysql_table_name}] successfully')
        except Exception:
            log.error(traceback.format_exc())
            raise ExcelToSqlException
