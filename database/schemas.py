from marshmallow import Schema, fields


# 定义 Marshmallow schema
# Marshmallow是一个用于序列化和反序列化数据的库，它可以将复杂的数据结构转换为Python对象，反之亦然。
class VehicleSchema(Schema):
    id = fields.Int()
    prov = fields.Str()
    city = fields.Str()
    sales = fields.Int()
    dealership_num = fields.Int()


class PartSchema(Schema):
    id = fields.Int()
    supplier_name = fields.Str()
    supplier_addr = fields.Str()
    prov = fields.Str()
    city = fields.Str()
    dest = fields.Str()
    distance = fields.Int()
    quantity = fields.Float()


class PartOptimizeSchema(Schema):
    id = fields.Int()
    prov = fields.Str()
    city = fields.Str()
    cc = fields.Float()
    cd = fields.Float()
    fs = fields.Float()
    qd = fields.Float()
    tj = fields.Float()
    dl = fields.Float()
    cost = fields.Float()
    programme = fields.Str()
    method = fields.Str()


class RegressPredictSchema(Schema):
    id = fields.Int()
    operate = fields.Str()
    regress_data = fields.Str()
    create_time = fields.Date()


class TransportSchema(Schema):
    id = fields.Int()
    route = fields.Str()
    site_type = fields.Str()
    highway = fields.Str()
    railway = fields.Str()
    waterway = fields.Str()


class TransportCostSchema(Schema):
    id = fields.Int()
    site = fields.Str()
    history_sales = fields.Int()
    pro_sales = fields.Int()
    throughput = fields.Int()
    cost = fields.Float()
    o_throughput = fields.Int()
    o_cost = fields.Float()
    type = fields.Str()
    is_limit = fields.Str()
    method = fields.Str()


class EmptyCarSchema(Schema):
    __tablename__ = 'empty_car'
    __table_args__ = {'comment': '空车成本统计'}
    id = fields.Int()
    method = fields.Str()
    sales1 = fields.Float()
    tt = fields.Float()
    st = fields.Float()
    cost1 = fields.Float()
    sales2 = fields.Float()
    cost2 = fields.Float()
    save_car = fields.Float()
    save_mileage = fields.Float()
    extra_cost = fields.Float()
    save_cost = fields.Float()
    all_cost = fields.Float()
    site = fields.Str()
    month = fields.Str()
    city = fields.Str()

