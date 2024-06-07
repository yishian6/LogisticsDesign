# import json
#
# import flask
# import flask_login
# from flask import Blueprint, request
# from flask_login import login_user, login_required, current_user
# from werkzeug.security import generate_password_hash
# from database.base_model import t
# from database.models import User, Resume
# from utils.file_utils import AvatarStorage
# from utils.log_utils import Logging
#
# log = Logging().get_logger()
# personal_center = Blueprint("personal_center_view", __name__)
#
#
# @personal_center.route('/user/register', methods=['POST'])
# @t.transaction
# def register():
#     upload_data = json.loads(request.get_data().decode('utf-8'))
#     username = upload_data.get("username")
#     password = upload_data.get("password")
#     # 验证用户名和密码是否为空
#     if not username or not password:
#         return flask.jsonify({'code': 400, 'message': 'username or password is empty'})
#
#     log.info(User.query(User.username, filter=[User.username == username], limit=1))
#     # 验证用户名是否已经被注册
#     if User.query(User.username, filter=[User.username == username], limit=1):
#         return flask.jsonify({'code': 400, 'message': 'username has been registered'})
#     user = User(username=username, password_hash=generate_password_hash(password), role=0)
#     user.add()
#     # 添加简历的信息
#     Resume(username=username).add()
#     return flask.jsonify({'code': 200, 'message': 'Register success.'})
#
#
# @personal_center.route('/user/login', methods=['POST'])
# def login():
#     upload_data = json.loads(request.get_data().decode('utf-8'))
#     username = upload_data.get("username")
#     password = upload_data.get("password")
#     if not username or not password:
#         return flask.jsonify({'code': 400, 'message': 'username or password is empty'})
#     # 验证用户名和密码是否一致
#     # 数据库中查询用户
#     password_hash_list = User.query([User.password_hash], filter=[User.username == username])
#     if not password_hash_list:
#         return flask.jsonify({'code': 400, 'message': 'username not exist'})
#     user = User(username=username, password_hash=password_hash_list[0][0], role=0)
#     if user.validate_password(user.password_hash, password):
#         login_user(user)  # 登入用户
#         return flask.jsonify({'code': 200, 'message': 'Login success.'})
#     return flask.jsonify({'code': 400, 'message': 'username or password is wrong'})
#
#
# @personal_center.route('/user/logout', methods=['GET', 'POST'])
# @login_required
# def logout():
#     flask_login.logout_user()
#     return flask.jsonify({'code': 200, 'message': 'Logout success.'})
#
#
# @personal_center.route('/protected', methods=['GET', 'POST'])
# @login_required
# # 添加保护路由
# def protected():
#     return flask.jsonify({'code': 200, 'message': 'Protected.'})
#
#
# @personal_center.route('/user/avatar/upload', methods=['POST'])
# @login_required
# @t.transaction
# def avatar_upload():
#     username = current_user.username
#     avatar_file = request.files['avatar']
#     # 上传文件
#     avatar_filename = AvatarStorage.generate_filename(username=username)
#     avatar_local_path = AvatarStorage.get_local_path(avatar_filename)
#     AvatarStorage.upload(avatar_file, avatar_local_path)
#
#     if AvatarStorage.is_file_exist(avatar_local_path):
#         # 将avatar_local_path传入数据库
#         User.update({'avatar': avatar_local_path}, [User.username == username])
#         return flask.jsonify({'code': 200, 'message': 'Successfully modified the avatar.'})
#     else:
#         return flask.jsonify({'code': 400, 'message': 'Failed modified the avatar.'})
#
#
# @personal_center.route('/user/display', methods=['GET'])
# @login_required
# def avatar_display():
#     username = current_user.username
#     User.query([User.username, User.role, User.avatar], filter=[User.username == username])
#
#     return {'code': 200, 'message': 'Successfully display person center.'}
