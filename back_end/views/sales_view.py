import json
import os
import time

# import pandas as pd
# from sqlalchemy import desc
from flask import Blueprint, jsonify, request, send_file
from sqlalchemy import desc

from business.sales.sales_predict import predict
from database.models import RegressPredict as rp
from database.schemas import RegressPredictSchema
from utils.config_utils import BASE_DIR
from utils.log_utils import Logging
from database.base_model import t

log = Logging().get_logger()
sales_view = Blueprint("sales_view", __name__)


@sales_view.route('/sales/index', methods=['GET'], endpoint="init")
def init():
    query_result = rp.query([rp.id, rp.operate, rp.regress_data, rp.create_time], order_by=desc(rp.id))
    regress_predict_schema = RegressPredictSchema()
    print(query_result)
    json_data = regress_predict_schema.dump(query_result, many=True)  # 转换后的 JSON 数据
    # 将存在数据库的数据转换成字典格式
    for data in json_data:
        data["regress_data"] = eval(data["regress_data"])
    log.info("Regress Predict init successfully")
    print(json_data)
    return jsonify({
        "code": 200,
        "message": "Regress Predict init successfully",
        "data": json_data
    })


# 进行销量的回归预测，返回预测的数据，并且将数据保存在excel文件，供前端下载，
@sales_view.route('/sales/regress', methods=['POST'])
@t.transaction
def sales_regress():
    upload_data = json.loads(request.get_data().decode('utf-8'))
    method = upload_data.get("method")
    start = upload_data.get("start")
    end = upload_data.get("end")
    operates = f"使用{method}预测{start}~{end}的汽车销量情况"
    log.info(operates)
    # 获取预测结果
    res_dict = predict(method, start, end)
    rp_add = rp(operate=operates, regress_data=str(res_dict),
                create_time=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    rp_add.add()
    query_result = rp.query([rp.id, rp.operate, rp.regress_data, rp.create_time], order_by=desc(rp.id))
    regress_predict_schema = RegressPredictSchema()
    json_data = regress_predict_schema.dump(query_result, many=True)  # 转换后的 JSON 数据
    # 将存在数据库的数据转换成字典格式
    for data in json_data:
        data["regress_data"] = eval(data["regress_data"])
    log.info("Regress Predict successfully")
    return jsonify({
        "code": 200,
        "message": "Regress Predict successfully",
        "data": {
            "regress_record": json_data,
            "regress_result": res_dict
        }
    })


@sales_view.route("/sales/delete", methods=['POST'])
@t.transaction
def delete():
    # 获取前端传来的数据
    upload_data = json.loads(request.get_data().decode('utf-8'))
    record_id = upload_data.get("delId")
    filename: str = upload_data.get("filename")
    # 删除该元素
    rp.delete([rp.id == record_id])
    log.info("Regress Predict delete successfully")

    # 删除文件
    filename = filename.replace("/", '-').removeprefix("使用").removesuffix("的汽车销量情况") + ".xlsx"
    delete_file = os.path.join(BASE_DIR, 'data/prediction', filename)
    if os.path.exists(delete_file):
        # 如果文件存在，使用 os 模块中的 remove 方法来删除文件
        os.remove(delete_file)
        log.info(f"{delete_file} 已被删除")
    else:
        log.info(f"文件 {delete_file} 不存在")
    return jsonify({
        "code": 200,
        "message": "Regress Predict delete successfully",
    })


@sales_view.route('/sales/download', methods=['POST'])
def download_excel():
    # 获取前端传来的数据
    upload_data = json.loads(request.get_data().decode('utf-8'))
    method = upload_data.get("method")
    start = upload_data.get("start")
    end = upload_data.get("end")
    start = start.replace("/", "-")
    end = end.replace("/", "-")
    # 生成Excel文件的路径
    filename = f"{method}预测{start}~{end}.xlsx"
    excel_file = os.path.join(BASE_DIR, 'data/prediction', filename)
    if not os.path.exists(excel_file):
        return jsonify({'code': 500, 'message': 'file not exist'})
    # 发送Excel文件给前端
    return send_file(excel_file, as_attachment=True)

# @sales_view.route('/upload', methods=['POST'])
# def upload():
#     file = request.files['file']
#     file_name = file.filename
#     log.debug(file_name)
#     file_path = os.path.join(FILE_SYSTEM_URL, 'upload_file', file_name)
#     file.save(file_path)
#     if not os.path.exists(file_path):
#         return jsonify({'code': 500, 'message': 'file not exist'})
#     return jsonify({'code': 200, 'message': 'upload success'})

