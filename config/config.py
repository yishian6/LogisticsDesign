from utils.config_utils import ConfigUtils
import tzlocal

# 日志配置
LOG_PATH = ConfigUtils.get("Log", "logPath")
IS_AUTO_REMOVE = ConfigUtils.get("Log", "isAutoRemove")
ROTATION = ConfigUtils.get("Log", "rotation")
RETENTION = ConfigUtils.get("Log", "retention")

# Predict配置
PREDICT_PATH = ConfigUtils.get("Predict", "predict_model")

# 邮箱配置
MAIL_DEFAULT_RECEIVER = ConfigUtils.get("Mail", "mail_default_receiver")


# 数据库配置
class Config(object):
    DEBUG = False
    SCHEDULER_API_ENABLED = True
    SCHEDULER_TIMEZONE = str(tzlocal.get_localzone())
    JSON_AS_ASCII = False
    # secret_key
    SECRET_KEY = "secret_key"

    # 邮箱配置
    MAIL_SERVER = ConfigUtils.get("Mail", "mail_server")
    MAIL_PORT = ConfigUtils.get("Mail", "mail_port")
    MAIL_USE_TLS = ConfigUtils.get("Mail", "mail_use_tls")
    MAIL_USERNAME = ConfigUtils.get("Mail", "mail_username")
    MAIL_PASSWORD = ConfigUtils.get("Mail", "mail_password")
    MAIL_DEFAULT_SENDER = ConfigUtils.get("Mail", "mail_default_sender")


class DevelopmentConfig(Config):
    """开发环境"""
    DEBUG = True

    def __init__(self):
        self.DATABASE_HOST = ConfigUtils.get("DevelopmentMysql", "host")
        self.DATABASE_PORT = ConfigUtils.get("DevelopmentMysql", "port")
        self.DATABASE_NAME = ConfigUtils.get("DevelopmentMysql", "database")
        self.DATABASE_USER_NAME = ConfigUtils.get("DevelopmentMysql", "username")
        self.DATABASE_PASSWORD = ConfigUtils.get("DevelopmentMysql", "password")
        self.SQLALCHEMY_DATABASE_URI = ("mysql+pymysql://" + self.DATABASE_USER_NAME + ":" +
                                        self.DATABASE_PASSWORD + "@" + self.DATABASE_HOST +
                                        ":" + self.DATABASE_PORT + "/" + self.DATABASE_NAME)


class ProductionConfig(Config):
    """生产环境"""
    DEBUG = False

    def __init__(self):
        self.DATABASE_HOST = ConfigUtils.get("ProductionMysql", "host")
        self.DATABASE_PORT = ConfigUtils.get("ProductionMysql", "port")
        self.DATABASE_NAME = ConfigUtils.get("ProductionMysql", "database")
        self.DATABASE_USER_NAME = ConfigUtils.get("ProductionMysql", "username")
        self.DATABASE_PASSWORD = ConfigUtils.get("ProductionMysql", "password")
        self.SQLALCHEMY_DATABASE_URI = ("mysql+pymysql://" + self.DATABASE_USER_NAME + ":" +
                                        self.DATABASE_PASSWORD + "@" + self.DATABASE_HOST +
                                        ":" + self.DATABASE_PORT + "/" + self.DATABASE_NAME)


config = {
    "1": DevelopmentConfig,
    "0": ProductionConfig,
    'default': DevelopmentConfig
}
