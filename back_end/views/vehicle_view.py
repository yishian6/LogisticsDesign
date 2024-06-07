# """
#    @Description: 实现多式联运的部分
# """
import json
import os
from flask import Blueprint, request, jsonify, send_file

from utils.config_utils import BASE_DIR
# from sqlalchemy import func
from utils.log_utils import Logging
from database.models import Vehicle, Transport, TransportCost as Tc, EmptyCar as Ec
from database.schemas import VehicleSchema, TransportSchema, TransportCostSchema, EmptyCarSchema

# 生成蓝图
vehicle_view = Blueprint("vehicle_view", __name__)
log = Logging().get_logger()

vehicle_list = [Vehicle.id, Vehicle.prov, Vehicle.city, Vehicle.sales, Vehicle.dealership_num]
ec_list = [Ec.id, Ec.method, Ec.sales1, Ec.tt, Ec.st, Ec.cost1, Ec.sales2, Ec.cost2, Ec.save_car, Ec.save_mileage,
           Ec.extra_cost, Ec.save_cost, Ec.all_cost, Ec.city]


@vehicle_view.route('/vehicle/index', methods=['GET'])
def vehicle_init():
    query_result = Vehicle.query(vehicle_list)
    vehicle_schema = VehicleSchema()
    json_data = vehicle_schema.dump(query_result, many=True)  # 转换后的 JSON 数据
    log.info("Vehicle init successfully")
    return jsonify({
        "code": 200,
        "message": "Vehicle init successfully",
        "data": json_data
    })


# 进行多式联运末端节点高级查询的操作
@vehicle_view.route('/vehicle/search', methods=['POST'], endpoint="explore")
def explore():
    upload_data = json.loads(request.get_data().decode('utf-8'))
    prov = upload_data.get("prov")
    city = upload_data.get("city")
    query_filter = []
    if prov != "":
        query_filter.append(Vehicle.prov == prov)
    if city != "":
        query_filter.append(Vehicle.city == city)
    query_result = Vehicle.query(vehicle_list, filter=query_filter)
    vehicle_schema = VehicleSchema()
    json_data = vehicle_schema.dump(query_result, many=True)  # 转换后的 JSON 数据
    log.info("Vehicle explore successfully")
    return jsonify({
        "code": 200,
        "message": "explore successfully",
        "data": json_data
    })


# 查询整车网络优化的路线
@vehicle_view.route('/transport/index', methods=['GET'])
def transport_init():
    query_result = Transport.query(
        [Transport.id, Transport.route, Transport.site_type, Transport.highway, Transport.railway, Transport.waterway])
    transport_schema = TransportSchema()
    json_data = transport_schema.dump(query_result, many=True)  # 转换后的 JSON 数据
    log.info("transport init successfully")
    return jsonify({
        "code": 200,
        "message": "transport init successfully",
        "data": json_data
    })


# 进行多式联运末端节点高级查询的操作
@vehicle_view.route('/transport/search', methods=['POST'])
def transport_search():
    upload_data = json.loads(request.get_data().decode('utf-8'))
    way = upload_data.get("way")
    site_type = upload_data.get("site_type")
    site = upload_data.get("site")
    field_filter = []
    if site_type != "":
        field_filter.append(Transport.site_type == site_type)
    if site != "":
        field_filter.append(Transport.route.like(f"%{site}%"))
    if way == "铁路":
        field_filter.append(Transport.highway != "该路线暂未开通")
    elif way == "水路":
        field_filter.append(Transport.waterway != "该路线暂未开通")
    query_result = Transport.query(
        [Transport.id, Transport.route, Transport.site_type, Transport.highway, Transport.railway, Transport.waterway],
        filter=field_filter)
    transport_schema = TransportSchema()
    json_data = transport_schema.dump(query_result, many=True)  # 转换后的 JSON 数据
    log.info("transport search successfully")
    return jsonify({
        "code": 200,
        "message": "transport search successfully",
        "data": json_data
    })


# 多式联运运输成本优化（品牌车）
@vehicle_view.route('/transport/cost', methods=['POST'])
def transport_cost():
    site_list = []
    throughput_list = []
    cost_list = []
    o_throughput_list = []
    o_cost_list = []
    upload_data = json.loads(request.get_data().decode('utf-8'))
    req_type = upload_data.get("type")
    req_limit = upload_data.get("is_limit")
    req_method = upload_data.get("method")
    query_result = Tc.query(
        [Tc.id, Tc.site, Tc.history_sales, Tc.pro_sales, Tc.throughput, Tc.cost, Tc.o_throughput, Tc.o_cost],
        filter=[Tc.type == req_type, Tc.is_limit == req_limit, Tc.method == req_method])
    for i in range(len(query_result) - 1):
        site_list.append(query_result[i][1])
        throughput_list.append(query_result[i][4])
        cost_list.append(query_result[i][5] / 10000.0)
        o_throughput_list.append(query_result[i][6])
        o_cost_list.append(query_result[i][7] / 10000.0)
    transport_cost_schema = TransportCostSchema()
    json_data = transport_cost_schema.dump(query_result, many=True)  # 转换后的 JSON 数据
    log.info("transport cost successfully")
    return jsonify({
        "code": 200,
        "message": "transport cost successfully",
        "data": {
            "all_data": json_data,
            "site": site_list,
            "throughput": throughput_list,
            "cost": cost_list,
            "o_throughput": o_throughput_list,
            "o_cost": o_cost_list
        }
    })


# 实现品牌车运输成本优化的下载（需要进一步完善）
@vehicle_view.route('/transport/cost/download', methods=['POST'])
def cost_download_excel():
    # 获取前端传来的数据
    upload_data = json.loads(request.get_data().decode('utf-8'))
    req_type = upload_data.get("type")
    req_limit = upload_data.get("is_limit")
    req_method = upload_data.get("method")
    month = "12月"
    site = "广州"
    # 生成Excel文件的路径
    filename = f"{month}{site}空车优化结果.xlsx"
    excel_file = os.path.join(BASE_DIR, 'data/emptyCar', filename)
    if not os.path.exists(excel_file):
        return jsonify({'code': 500, 'message': 'file not exist'})
    # 发送Excel文件给前端
    return send_file(excel_file, as_attachment=True)


# 进行空车数据的查询
@vehicle_view.route('/empty/search', methods=['POST'])
def select_empty_car():
    req_data = json.loads(request.get_data().decode("utf-8"))
    site = req_data.get('site')
    month = req_data.get('month')
    query_res = Ec.query(ec_list, filter=[Ec.site == site, Ec.month == month])
    empty_car_schema = EmptyCarSchema()
    json_data = empty_car_schema.dump(query_res, many=True)  # 转换后的 JSON 数据
    log.info("Empty car search successfully")
    return jsonify({
        "code": 200,
        "message": "empty car search successfully",
        "data": json_data
    })
    pass


# 实现空车优化部分的下载
@vehicle_view.route('/empty/download', methods=['POST'])
def download_excel():
    # 获取前端传来的数据
    upload_data = json.loads(request.get_data().decode('utf-8'))
    site = upload_data.get("site")
    month = upload_data.get("month")
    # 生成Excel文件的路径
    filename = f"{month}{site}空车优化结果.xlsx"
    excel_file = os.path.join(BASE_DIR, 'data/emptyCar', filename)
    if not os.path.exists(excel_file):
        return jsonify({'code': 500, 'message': 'file not exist'})
    # 发送Excel文件给前端
    return send_file(excel_file, as_attachment=True)

