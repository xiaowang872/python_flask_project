# 这只是一个测试蓝图的学习目录
# # 项目根目录（可自定义项目名称，如 "flask_project"）
# ├── app_practice/  # 核心应用目录，包含所有业务模块
# │   ├── __init__.py  # 应用初始化文件，用于注册蓝图
# │   │   # （文件内核心代码：导入 index_blu 并通过 app.register_blueprint 注册）
# │   └── index/  # 新建的 index 模块包（即步骤1中的 index package）
# │       ├── __init__.py  # index 模块的初始化文件
# │       │   # （文件内核心代码：导入 Blueprint、实例化 index_blu、导入 views.py）
# │       └── views.py  # index 模块的视图文件
# │           # （文件内核心代码：导入 index_blu、定义 @index_blu.route('/') 装饰的视图函数）
# └── manager.py  # 项目启动文件（步骤5中右键运行的文件，用于启动 Flask 服务）
# 导入app包中创建的Flask应用实例
from app_practice import app

# 程序入口
if __name__ == '__main__':
    app.run(debug=True)  # debug=True开启调试模式，开发环境使用