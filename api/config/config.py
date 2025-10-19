# F:\vue_flask_project\vue_flask_project_one\flask\pythonProject1\api\config\config.py
# 原始一点的写法，后面我们将他封装成类
# connection = pymysql.connect(
#     'host': '192.168.117.200',
#     'port': 3306,
#     'user': 'root',
#     'password': '123456',
#     'database': 'flask_databases',
# )
# 
import logging
from redis import StrictRedis
class Config:
    DEBUG = True
    # 设置日志的级别
    LEVEL_LOG = logging.INFO
    # 数据库配置
    SQL_HOST = '192.168.117.200'
    SECRET_KEY = 'slajfasfjkajfj'
    SQL_USERNAME = 'root'
    SQL_PASSWORD = '123456'
    SQL_PORT = 3306
    SQL_DB = 'flask_databases'
    JSON_AS_ASCII = False  # 解决 jsonify 中文显示问题
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{SQL_USERNAME}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DB}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = '192.168.117.200'
    REDIS_PORT = 6379
    REDIS_PASSWORD = '1234567890'
    # 指定session存储方式
    SESSION_TYPE = 'redis'
    # 指定session的保存的redis的位置
    SESSION_REDIS = StrictRedis(host=REDIS_HOST,port=REDIS_PORT)
    # 使用session_key签名
    SESSION_USE_SIGNER = True
    # 设置session的过期时间
    PERMANENT_SESSION_LIFETIME = 31*60*60*24  # 31天



# 开发环境的config
class DevConfig(Config):
    pass


# 生产环境的config
class ProConfig(Config):
    LEVEL_LOG = logging.ERROR
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:123456@192.168.117.200:3306/abc_test?charset=utf8mb4"


# 测试环境的config
class TestConfig(Config):
    pass
Config_dict = {
    'dev':DevConfig,
    'pro':ProConfig,
    'test':TestConfig
}



