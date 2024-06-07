import os
import sys
import traceback
from flask import Flask, jsonify, render_template
# from flask_mail import Message, Mail
# from flask_apscheduler import APScheduler
from flask_cors import CORS
# from flask_login import LoginManager

# from database.models import User
from utils.config_utils import BASE_DIR
from config.config import config, MAIL_DEFAULT_RECEIVER
# from business.job.job_recommend import save_position_ids
# from business.news.news_recommend import save_news_ids
from common.base_exception import TopException, MailSendError, MailSendSuccess
from utils.log_utils import Logging

# from database.db_update import data_update, db_reconnection

log = Logging().get_logger()
# scheduler = APScheduler()
# login = LoginManager()
# mail = Mail()


def create_app(config_name):
    # 设置vue编译输出目录dist文件夹，为Flask模板文件目录
    app = Flask(__name__, static_folder=os.path.join(BASE_DIR, 'front', 'dist'),  # 设置静态文件夹目录
                template_folder=os.path.join(BASE_DIR, 'front', 'dist'),
                static_url_path="")
    # 获取相应的配置类
    app.config.from_object(config[config_name])
    register_blueprint(app)
    # scheduler_init(app)
    front(app)
    # mail.init_app(app)
    # login_manager_init(app)
    error_execute(app)
    CORS(app, supports_credentials=True)
    return app


# def login_manager_init(flask_app: Flask):
#     login.init_app(flask_app)
#     login.session_protection = 'basic'
#     login.login_view = 'personal_center_view.login'
#     login.login_message = '请登录后访问'


# @login.user_loader
# def load_user(user_id):
#     # since the user_id is just the primary key of our user table, use it in the query for the user
#     return User.get(user_id)
#
#
# def scheduler_init(flask_app: Flask):
#     # engine_options={'pool_recycle' = 3600,'pool_pre_ping' = True}
#     scheduler.add_job(id='database_reconnection', func=db_reconnection, trigger='interval', hours=1)
#     scheduler.add_job(id='data_update', func=data_update, trigger='cron', day_of_week='sun', hour=0, minute=0)
#     scheduler.add_job(id='save_news_ids_rural', func=save_news_ids, args=["Rural"], trigger='cron', day_of_week='sun',
#                       hour=0,
#                       minute=1)
#     scheduler.add_job(id='save_news_ids_last_mile', func=save_news_ids, args=["LastMile"], trigger='cron',
#                       day_of_week='sun',
#                       hour=0, minute=10)
#     scheduler.add_job(id='save_position_ids', func=save_position_ids, trigger='cron', day_of_week='sun', hour=0,
#                       minute=20)
#     scheduler.init_app(flask_app)
#     scheduler.start()  # 启动任务列表


# 注册蓝图
def register_blueprint(flask_app: Flask):
    from back_end.views.part_view import part_view
    from back_end.views.vehicle_view import vehicle_view
    from back_end.views.sales_view import sales_view
    flask_app.register_blueprint(part_view, catch_all_except=True)
    flask_app.register_blueprint(vehicle_view, catch_all_except=True)
    flask_app.register_blueprint(sales_view, catch_all_except=True)


# # 错误处理邮箱发送
# def send_error_email(method_name: str, error_info: str):
#     try:
#         msg = Message('Error occurred in zywj app',
#                       recipients=[MAIL_DEFAULT_RECEIVER])
#         msg.body = f"An error occurred in method {method_name}:\n\n{error_info}"
#         mail.send(msg)
#     except Exception:
#         raise MailSendError
#     else:
#         raise MailSendSuccess


# 错误请求页面处理
def error_execute(flask_app: Flask):
    @flask_app.errorhandler(Exception)
    def catch_all_except(e):
        _, _, exc_traceback = sys.exc_info()
        tb_list = traceback.extract_tb(exc_traceback)
        method_name = tb_list[-1][2]
        if isinstance(e, TopException):
            log.error(f"{method_name} error, info is{e.msg}")
            return jsonify({
                "code": e.code,
                "message": e.msg,
                "data": None
            })
        else:
            log.error(f"{method_name} error, info is {str(e)}")
            log.error(f"{traceback.format_exc()}")
            # 发送错误邮件
            # send_error_email(method_name, str(e))
            return jsonify({
                "code": 500,
                "message": None,
                "data": str(e)
            })


def front(flask_app: Flask):
    # 将"./web/front/dist/index.html"文件映射到根路径"/"
    @flask_app.route('/')
    def index():
        return render_template('index.html', name='index')
