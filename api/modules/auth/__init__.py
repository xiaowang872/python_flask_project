# F:\vue_flask_project\vue_flask_project_one\flask\pythonProject1\api\modules\auth\__init__.py
from flask import Blueprint
from flask_restful import Api

# 创建蓝图
auth_blu = Blueprint('auth', __name__, url_prefix='/auth')

# 创建api对象
api = Api(auth_blu)

from api.modules.auth.login import LoginView

# 添加资源到api中（注册路由）
api.add_resource(LoginView, '/login')