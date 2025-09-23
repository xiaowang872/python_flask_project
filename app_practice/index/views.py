# 导入当前模块的蓝图实例
from app_practice.index import index_blu

# 使用蓝图注册路由
@index_blu.route('/')
def index():
    """
    首页视图函数
    """
    return "欢迎来到视频网站首页，现在，在app_practice/index/views.py"