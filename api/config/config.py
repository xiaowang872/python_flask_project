# 原始一点的写法，后面我们将他封装成类
# connection = pymysql.connect(
#     'host': '192.168.117.200',
#     'port': 3306,
#     'user': 'root',
#     'password': '123456',
#     'database': 'flask_databases',
# )
class Config:
    SQL_HOST = '192.168.117.200'
    SQL_USERNAME = 'root'
    SQL_PASSWORD = '123456'
    SQL_PORT = 3306
    SQL_DB = 'flask_databases'
    JSON_AS_ASCII = False  # 解决 jsonify 中文显示问题
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{SQL_USERNAME}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DB}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# 开发环境的config
class DevConfig(Config):
    pass
# 生产环境的config
class ProConfig(Config):
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