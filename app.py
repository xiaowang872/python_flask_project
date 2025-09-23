from api import db, create_app
# from flask_script import Manager    #命令行管理的Manager类,可惜flask-script不再维护了,不能用了，我这边改为原生的写法
from flask_migrate import Migrate
import click
from flask.cli import with_appcontext
from api.models import UserInfo # 导入你的用户模型
from datetime import datetime
from video_practice import video_bp
import secrets  # 用于生成安全的密钥

app = create_app('dev')
Migrate(app, db)

@app.route('/')
def index():
    return "欢迎来到视频网站首页"

@app.route('/add')
def add_data():
    u = UserInfo()
    new_user1 = UserInfo(nickname='flask_test1', mobile='13888888888', signature='理想', create_time=datetime.now(), role_id=1)
    new_user2 = UserInfo(nickname='flask_test2', mobile='13999999999', signature='信念', create_time=datetime.now(), role_id=2)
    new_user3 = UserInfo(nickname='flask_test3', mobile='13777777777', signature='坚持', create_time=datetime.now(), role_id=1)
    new_user4 = UserInfo(nickname='flask_test4', mobile='13666666666', signature='奋斗', create_time=datetime.now(), role_id=2)
    u.add(new_user1)
    u.add(new_user2)
    u.add(new_user3)
    u.add(new_user4)
    return "添加数据成功"

@app.route('/query1')
def query_data1():
    user_list = UserInfo.query.all()
    result = []
    for user in user_list:
        result.append(user.to_dict())
    return {'users': result}

@app.route('/query2')
def query_data2():
    user=UserInfo.query.get(3)  #主键查询
    return {'users': user.to_dict()}

@app.route('/query3')
def query_data3():
    first_user = UserInfo.query.first()  #查询第一条数据
    return {'users': first_user.to_dict()}

@app.route('/query4')
def query_data4():
    user_list = UserInfo.query.filter(UserInfo.signature == '理想').all()  #条件查询
    result = []
    for user in user_list:
        result.append(user.to_dict())
    return {'users': result}

@app.route('/query5')
def query_data5():
    userlist = UserInfo.query.filter_by(signature='信念').all()  #根据字段
    result = []
    for user in userlist:
        result.append(user.to_dict())
    return {'users': result}

# 删除id为4的信息
@app.route('/delete1')
def delete_data():
    try:
        user = UserInfo.query.get(4)
        db.session.delete(user)
        db.session.commit()
        return "删除id为4的数据成功,使用db.session.delete()方法且已db.session.commit()提交（容易误删）"
    except Exception as e:
        return "删除失败，错误信息：(数据不存在或已经被（彻底）删除过一次)" + str(e)
        
@app.route('/delete2')
def delete_data2():
    delete_user = UserInfo.query.get(3)
    delete_user.delete()
    return "删除id为3的数据成功,使用模型类的delete()方法（推荐）,修改status状态为0，已提交"

@app.route('/update1')
def update_data():
    u = UserInfo()
    update_user = u.query.get(3)
    update_user.status = 1
    u.update()
    return "更新id为3的数据成功,使用模型类的update()方法（推荐）,将status状态改为1，已提交"


# 注册自定义命令：创建数据库表
@app.cli.command("create-db")
@with_appcontext
def create_db():
    """创建所有数据库表"""
    # from api.models.user import UserInfo  # 导入你的用户模型
    db.create_all()
    click.echo("数据库表创建成功！")

# 如果你有其他自定义命令，也可以在这里注册
# @app.cli.command("其他命令名")
# def 函数名():
#     命令逻辑

# 注册视频蓝图，并指定url前缀
# 为蓝图中的所有路由统一添加前缀 /video
app.register_blueprint(video_bp, url_prefix='/video')

import os
# 视频提前做声明
# app.config['UPLOAD_FOLDER'] = 'video_practice/uploads/videos'  # 设置上传文件的保存路径
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 设置最大上传文件大小为500MB
app.secret_key = secrets.token_hex(32)  # 生成64字符的十六进制密钥，设置Flask应用的密钥，用于加密会话数据

# # 1. 配置你的视频目录（绝对路径，避免相对路径问题）
# # 这里直接指向你的目录：video_practice/uploads/videos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # app.py 所在目录
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'video_practice', 'uploads', 'videos')
# # 确保目录存在（防止误删）
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
# # 打印目录路径，方便调试
print(f"自定义视频目录（绝对路径）: {app.config['UPLOAD_FOLDER']}")

# 添加静态路由用于访问上传的视频文件
from flask import send_from_directory
@app.route('/uploads/videos/<filename>')
def serve_uploaded_video(filename):
    """用于访问上传的视频文件"""
    try:
        return send_from_directory(
            app.config['UPLOAD_FOLDER'], 
            filename,
            as_attachment=False  # 设置为True会提示下载，False则直接在浏览器中播放
            )
    except FileNotFoundError:
        return "视频文件不存在",404
    
if __name__ == '__main__':
    app.run(debug=True)