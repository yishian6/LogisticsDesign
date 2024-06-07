import os
# from dotenv import load_dotenv

from database.db_init import DB
from utils.log_utils import Logging
from database.base_model import t
from back_end import create_app

# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
# if os.path.exists(dotenv_path):
#     load_dotenv(dotenv_path)

log = Logging().get_logger()
app = create_app(os.getenv('FLASK_DEBUG') or 'default')


@app.teardown_appcontext
def shutdown_session(exception=None):
    t.trans_session.remove()


@app.cli.command()
def create():
    try:
        DB.drop_table()
        DB.create_table()
        DB.data_init()
    except Exception as e:
        log.warning(str(e))


@app.cli.command()
def training():
    try:
        # save_news_ids("Rural")
        # save_news_ids("LastMile")
        # save_position_ids()
        pass
    except Exception as e:
        log.warning(str(e))


if __name__ == '__main__':
    # create()  # 创建数据库
    app.run(host='0.0.0.0', debug=True, port=5000)
