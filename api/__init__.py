from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.config.config import Config_dict
from redis import StrictRedis
from api.config import config
from api.test_connections.test_mysql import test_mysql

# guixiang留言：在项目中，一般把内个db和app的实例化，放在api文件下的__init__.py文件中
# 在create_app函数中，可以传输一个config_name参数，方便我切换开发，测试的数据库配置
# app.config.from_object(Config)它的作用是，将Config类中的属性，全部导入到app.config中
# app.config.from_object(config) 的作用是将一个 Python 类或模块中的所有大写属性导入到 Flask 应用的配置系统中。
# db.init_app(app)，就是将Flask应用实例app，绑定到SQLAlchemy实例db中，这样就可以通过SQLAlchemy的db对象来操作数据库了

db = SQLAlchemy()
def create_app(config_name):
    app = Flask(__name__)
    config = Config_dict.get(config_name)
    app.config.from_object(config)
    db.init_app(app)
    test_mysql(app,db)
    global redis_store
    # redis_store = None
    # 创建redis的连接对象
    redis_store = StrictRedis(
        host=config.REDIS_HOST, 
        port=config.REDIS_PORT,
        decode_responses=True,
        password=config.REDIS_PASSWORD # 密码，标记一下这是我自己添加的，后续有排查错误时，可以查看redis的连接信息
        )
    print(f"Redis连接信息: host={config.REDIS_HOST}, port={config.REDIS_PORT}")
    try:
        redis_store.ping()
        print("✅ Redis连接成功")
    except Exception as e:
        print(f"❌ Redis连接失败: {e}")
        redis_store = None
        raise e

    # 延迟导入模块，避免循环导入
    from api.modules.auth import auth_blu
    app.register_blueprint(auth_blu)





    return app


# redis存储




