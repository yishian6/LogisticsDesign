# from flask_login import UserMixin
from sqlalchemy import Column, Float, Integer, String, Date, TEXT
from sqlalchemy.ext.declarative import declarative_base
# from werkzeug.security import generate_password_hash, check_password_hash
from database.base_model import BaseOrmModel

Base = declarative_base()


# metadata = Base.metadata


class Vehicle(Base, BaseOrmModel):
    __tablename__ = 'vehicle'
    __table_args__ = {'comment': '整车数量统计'}
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    prov = Column(String(32), nullable=False)
    city = Column(String(32), nullable=False)
    sales = Column(Integer, nullable=False)
    dealership_num = Column(Integer, nullable=False)


class Part(Base, BaseOrmModel):
    __tablename__ = 'part'
    __table_args__ = {'comment': '零件信息统计'}
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    supplier_name = Column(String(32), nullable=False)
    supplier_addr = Column(String(256), nullable=False)
    prov = Column(String(16), nullable=False)
    city = Column(String(16), nullable=False)
    dest = Column(String(16), nullable=False)
    distance = Column(Integer, nullable=False)
    quantity = Column(Float, nullable=False)


class PartOptimize(Base, BaseOrmModel):
    __tablename__ = 'part_optimize'
    __table_args__ = {'comment': '零件网络优化'}
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    prov = Column(String(16), nullable=False)
    city = Column(String(16), nullable=False)
    cc = Column(Float, nullable=False)
    cd = Column(Float, nullable=False)
    fs = Column(Float, nullable=False)
    qd = Column(Float, nullable=False)
    tj = Column(Float, nullable=False)
    dl = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    programme = Column(String(32), nullable=False)
    method = Column(String(32), nullable=False)


class RegressPredict(Base, BaseOrmModel):
    __tablename__ = 'regress_predict'
    __table_args__ = {'comment': '销量回归预测'}
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    operate = Column(String(256), nullable=False)
    regress_data = Column(TEXT, nullable=False)
    create_time = Column(Date, nullable=False)


class Transport(Base, BaseOrmModel):
    __tablename__ = 'transport'
    __table_args__ = {'comment': '多式联运'}
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    route = Column(String(128), nullable=False)
    site_type = Column(String(16), nullable=False)
    highway = Column(String(32), nullable=False)
    railway = Column(String(32), nullable=False)
    waterway = Column(String(32), nullable=False)


class TransportCost(Base, BaseOrmModel):
    __tablename__ = 'transport_cost'
    __table_args__ = {'comment': '多式联运运输成本'}
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    site = Column(String(8), nullable=False)
    history_sales = Column(Integer, nullable=False)
    pro_sales = Column(Integer, nullable=False)
    throughput = Column(Integer, nullable=False)
    cost = Column(Float, nullable=False)
    o_throughput = Column(Integer, nullable=False)
    o_cost = Column(Float, nullable=False)
    type = Column(String(8), nullable=False)  # 查询的类型
    is_limit = Column(String(32), nullable=False)  # 是否受限
    method = Column(String(32), nullable=False)  # 使用的方法


class EmptyCar(Base, BaseOrmModel):
    __tablename__ = 'empty_car'
    __table_args__ = {'comment': '空车成本统计'}
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
    method = Column(String(64), nullable=False)
    sales1 = Column(Float, nullable=False)
    tt = Column(Float, nullable=False)
    st = Column(Float, nullable=False)
    cost1 = Column(Float, nullable=False)
    sales2 = Column(Float, nullable=False)
    cost2 = Column(Float, nullable=False)
    save_car = Column(Float, nullable=False)
    save_mileage = Column(Float, nullable=False)
    extra_cost = Column(Float, nullable=False)
    save_cost = Column(Float, nullable=False)
    all_cost = Column(Float, nullable=False)
    site = Column(String(16), nullable=False)
    month = Column(String(16), nullable=False)
    city = Column(String(16), nullable=False)


# class User(Base, BaseOrmModel, UserMixin):
#     __tablename__ = 'user'
#     __table_args__ = {'comment': '用户'}
#     id = Column(Integer, primary_key=True, unique=True, autoincrement=True, nullable=False)
#     username = Column(String(32), nullable=False)
#     password_hash = Column(String(128), nullable=False)
#     # 0: 普通用户 1: 管理员
#     role = Column(Integer, nullable=False)
#     # 头像
#     avatar = Column(String(256), nullable=False)
#
#     def __init__(self, username, password_hash, role):
#         super(User, self).__init__()
#         self.username = username
#         self.password_hash = password_hash
#         self.role = role
#         self.avatar = 'https://exmaple.com/avatar.png'
#
#     def get_id(self):
#         id_list = User.query([User.id],
#                              filter=[User.username == self.username])
#         if id_list:
#             self.id = id_list[0][0]
#         else:
#             self.id = 0
#         return self.id
#
#     @staticmethod
#     def get(user_id):
#         """try to return user_id corresponding User object.
#         This method is used by load_user callback function
#         """
#         if not user_id:
#             return None
#         user_information = User.query([User.username, User.password_hash, User.role, User.avatar],
#                                       filter=[User.id == user_id])
#         user = User(username=user_information[0][0], password_hash=user_information[0][1], role=user_information[0][2])
#         if user_information:
#             return user
#         return None
#
#     def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
#         self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段
#
#     @staticmethod
#     def validate_password(password_hash, password):  # 用于验证密码的方法，接受密码作为参数
#         return check_password_hash(password_hash, password)  # 返回布尔值

