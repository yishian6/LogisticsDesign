import json
from flask import Blueprint, request

from utils.log_utils import Logging

log = Logging().get_logger()
personal_center = Blueprint("personal_center_view", __name__)


@personal_center.route('/user/login', methods=['POST'])
def login():
    upload_data = json.loads(request.get_data().decode('utf-8'))
    username = upload_data.get("username")
    password = upload_data.get("password")
