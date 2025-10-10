from api import db, create_app
# from flask_script import Manager    #命令行管理的Manager类,可惜flask-script不再维护了,不能用了，我这边改为原生的写法
from flask_migrate import Migrate
import click
from flask.cli import with_appcontext
from api.models import UserInfo # 导入你的用户模型
from datetime import datetime
import time  
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
from flask import send_from_directory, request
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

# 临时检查mysql与redis页面
from flask import send_from_directory, render_template
@app.route('/login_page_abc')
def login_page():
    return render_template('mysql_redis_connect_tmp.html')

# 数据库重置表结构
@app.route('/reset_db')
def reset_db():
    """重置数据库表结构（开发环境使用）"""
    try:
        db.drop_all()
        db.create_all()
        return "数据库重置成功，所有表已重新创建"
    except Exception as e:
        return f"数据库重置失败: {str(e)}", 500


@app.route('/login_tmp')
def login_page_tmp():
    """用户登录页面"""
    return render_template('login_tmp.html')

# 可选：添加一个需要认证的测试路由
from api.utils.response_utils import error, success  # 添加这一行以导入 error 和 success
from api.utils.response_utils import HttpCode      # 如果 HttpCode 未导入，也一并导入

@app.route('/profile')
def user_profile():
    """需要认证的用户资料页面"""
    from api.utils.auth_helper import Auth
    auth = Auth()
    result = auth.identify(request)
    
    if result['code'] != 200:
        return error(code=HttpCode.auth_error, msg='请先登录')
    
    user_id = result['data']['user_id']
    user_info = UserInfo.query.get(user_id)
    
    if user_info:
        return success(msg='获取用户信息成功', data=user_info.to_dict())
    else:
        return error(code=HttpCode.params_error, msg='用户不存在')
# 添加认证认证页面加用户认证
@app.route('/user_add')
def user_add_page():
    """用户添加页面"""
    return render_template('user_add.html')
####################################################################################

@app.route('/add_user')
def add_user():
    """一键创建测试用户"""
    try:
        from api.models.user import UserInfo, UserLogin
        
        # 测试用户数据
        test_users = [
            {
                'nickname': '测试用户1', 
                'mobile': '13888888888', 
                'signature': '追求理想', 
                'role_id': 1,
                'sex': '1',
                'password': '123456'
            },
            {
                'nickname': '测试用户2', 
                'mobile': '13999999999', 
                'signature': '坚持信念', 
                'role_id': 2,
                'sex': '2',
                'password': '123456'
            },
            {
                'nickname': '测试用户3', 
                'mobile': '13777777777', 
                'signature': '持之以恒', 
                'role_id': 1,
                'sex': '1',
                'password': '123456'
            },
            {
                'nickname': '测试用户4', 
                'mobile': '13666666666', 
                'signature': '努力奋斗', 
                'role_id': 2,
                'sex': '0',
                'password': '123456'
            }
        ]
        
        success_count = 0
        results = []
        
        for user_data in test_users:
            try:
                # 检查手机号是否已存在
                existing_login = UserLogin.query.filter_by(mobile=user_data['mobile']).first()
                if existing_login:
                    results.append(f"❌ 手机号 {user_data['mobile']} 已存在，跳过")
                    continue
                
                # 1. 创建UserInfo用户信息（移除create_time）
                user_info = UserInfo(
                    nickname=user_data['nickname'],
                    mobile=user_data['mobile'],
                    signature=user_data['signature'],
                    role_id=user_data['role_id'],
                    sex=user_data['sex']
                    # create_time 字段在 BaseModels 中已经存在
                )
                user_info.add(user_info)
                
                # 2. 创建UserLogin登录信息
                user_login = UserLogin(
                    mobile=user_data['mobile'],
                    user_id=user_info.id,
                    last_login=datetime.now(),
                    last_login_stamp=int(time.time())
                )
                user_login.password = user_data['password']
                user_login.add(user_login)
                
                success_count += 1
                results.append(f"✅ 成功创建: {user_data['nickname']}({user_data['mobile']})")
                
            except Exception as e:
                results.append(f"❌ 创建失败 {user_data['nickname']}: {str(e)}")
        
        if success_count > 0:
            return f"成功创建 {success_count} 个测试用户！账号：13888888888/13999999999/13777777777/13666666666，密码：123456"
        else:
            return "创建失败，可能用户已存在或出现错误"
        
    except Exception as e:
        return f"添加用户数据失败: {str(e)}"

@app.route('/add_user_manual', methods=['POST'])
def add_user_manual():
    """手动添加单个用户"""
    try:
        from api.models.user import UserInfo, UserLogin
        
        # 获取表单数据
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        nickname = request.form.get('nickname')
        signature = request.form.get('signature', '')
        role_id = int(request.form.get('role_id', 1))
        sex = request.form.get('sex', '0')
        
        # 检查手机号是否已存在
        if UserLogin.query.filter_by(mobile=mobile).first():
            return "手机号已存在"
        
        # 创建UserInfo（移除create_time）
        user_info = UserInfo(
            nickname=nickname,
            mobile=mobile,
            signature=signature,
            role_id=role_id,
            sex=sex
            # create_time 字段在 BaseModels 中已经存在
        )
        user_info.add(user_info)
        
        # 创建UserLogin
        user_login = UserLogin(
            mobile=mobile,
            user_id=user_info.id,
            last_login=datetime.now(),
            last_login_stamp=int(time.time())
        )
        user_login.password = password
        user_login.add(user_login)
        
        return f"✅ 用户添加成功！手机号: {mobile}, 密码: {password}, 用户ID: {user_info.id}"
        
    except Exception as e:
        return f"添加用户失败: {str(e)}"

@app.route('/check_tables')
def check_tables():
    """检查两个表的数据"""
    try:
        from api.models.user import UserInfo, UserLogin
        
        user_info_count = UserInfo.query.count()
        user_login_count = UserLogin.query.count()
        
        user_info_data = UserInfo.query.all()
        user_login_data = UserLogin.query.all()
        
        result = f"""
        <h3>数据库表数据检查</h3>
        <p>UserInfo 表记录数: {user_info_count}</p>
        <p>UserLogin 表记录数: {user_login_count}</p>
        
        <h4>UserInfo 表数据:</h4>
        <pre>{[{'id': u.id, 'nickname': u.nickname, 'mobile': u.mobile} for u in user_info_data]}</pre>
        
        <h4>UserLogin 表数据:</h4>
        <pre>{[{'id': u.id, 'mobile': u.mobile, 'user_id': u.user_id} for u in user_login_data]}</pre>
        """
        
        return result
    except Exception as e:
        return f"检查失败: {str(e)}"

@app.route('/add_user_debug')
def add_user_debug():
    """调试版本的添加用户"""
    try:
        from api.models.user import UserInfo, UserLogin
        
        test_users = [
            {'nickname': '调试用户1', 'mobile': '13555555555', 'signature': '调试1', 'role_id': 1, 'sex': '1', 'password': '123456'},
        ]
        
        results = []
        
        for user_data in test_users:
            try:
                print(f"开始创建用户: {user_data['mobile']}")
                
                # 检查手机号是否已存在
                existing_login = UserLogin.query.filter_by(mobile=user_data['mobile']).first()
                if existing_login:
                    results.append(f"❌ UserLogin中手机号 {user_data['mobile']} 已存在")
                    continue
                    
                existing_info = UserInfo.query.filter_by(mobile=user_data['mobile']).first()
                if existing_info:
                    results.append(f"❌ UserInfo中手机号 {user_data['mobile']} 已存在")
                    continue
                
                # 1. 创建UserInfo
                print("创建UserInfo...")
                user_info = UserInfo(
                    nickname=user_data['nickname'],
                    mobile=user_data['mobile'],
                    signature=user_data['signature'],
                    role_id=user_data['role_id'],
                    sex=user_data['sex']
                )
                db.session.add(user_info)
                db.session.flush()  # 获取ID但不提交
                print(f"UserInfo创建成功，ID: {user_info.id}")
                
                # 2. 创建UserLogin
                print("创建UserLogin...")
                user_login = UserLogin(
                    mobile=user_data['mobile'],
                    user_id=user_info.id,
                    last_login=datetime.now(),
                    last_login_stamp=int(time.time())
                )
                print("设置密码...")
                user_login.password = user_data['password']  # 这会触发密码加密
                print("添加到session...")
                db.session.add(user_login)
                
                # 提交事务
                print("提交事务...")
                db.session.commit()
                print("事务提交成功!")
                
                results.append(f"✅ 成功创建: {user_data['nickname']}({user_data['mobile']})")
                
            except Exception as e:
                db.session.rollback()
                error_msg = f"❌ 创建失败 {user_data['nickname']}: {str(e)}"
                print(error_msg)
                results.append(error_msg)
                import traceback
                print(traceback.format_exc())  # 打印完整堆栈跟踪
        
        return "<br>".join(results)
        
    except Exception as e:
        return f"整体失败: {str(e)}"

@app.route('/check_redis')
def check_redis():
    """检查Redis连接状态"""
    try:
        from api import redis_store
        
        # 测试Redis连接
        redis_store.ping()
        
        # 测试Redis读写
        test_key = 'test_connection'
        redis_store.set(test_key, 'test_value', 10)
        value = redis_store.get(test_key)
        
        return f"""
        <div class="alert alert-success">
            <h4>✅ Redis连接正常</h4>
            <p>连接信息: {redis_store.connection_pool.connection_kwargs}</p>
            <p>测试读写: {value}</p>
        </div>
        """
    except Exception as e:
        return f"""
        <div class="alert alert-danger">
            <h4>❌ Redis连接失败</h4>
            <p>错误信息: {str(e)}</p>
        </div>
        """
    
# 在您的Flask应用中添加测试路由
@app.route('/test_log')
def test_log():
    """测试日志系统"""
    try:
        from api.modules.video.views import user_action_log
        user_action_log.info("这是一条测试日志消息")
        user_action_log.warning("这是一条警告日志")
        
        # 获取日志文件路径
        import os
        log_path = os.path.abspath('logs/user_action.log')
        
        return f"""
        ✅ 日志写入成功！<br>
        📁 日志文件位置: {log_path}<br>
        🔍 请检查该文件是否生成并包含日志内容
        """
    except Exception as e:
        return f"❌ 日志测试失败: {str(e)}"

@app.route('/log_status')
def log_status():
    """查看日志系统状态"""
    import os
    from api.modules.video.views import user_action_log
    
    status = []
    
    # 检查日志器配置
    status.append("📊 日志器配置:")
    status.append(f"   名称: {user_action_log.name}")
    status.append(f"   级别: {user_action_log.level}")
    status.append(f"   Handler数量: {len(user_action_log.handlers)}")
    
    for i, handler in enumerate(user_action_log.handlers):
        status.append(f"   Handler {i}: {type(handler).__name__}")
        if hasattr(handler, 'baseFilename'):
            status.append(f"       文件: {handler.baseFilename}")
            status.append(f"       文件存在: {os.path.exists(handler.baseFilename)}")
    
    # 检查预期日志文件
    expected_paths = [
        'logs/user_action.log',
        'F:/logs/user_action.log',
        './logs/user_action.log'
    ]
    
    status.append("🔍 检查预期日志文件:")
    for path in expected_paths:
        abs_path = os.path.abspath(path)
        exists = os.path.exists(abs_path)
        status.append(f"   {abs_path}: {'✅ 存在' if exists else '❌ 不存在'}")
        if exists:
            try:
                size = os.path.getsize(abs_path)
                status.append(f"       大小: {size} 字节")
                with open(abs_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                status.append(f"       内容预览: {content[:200]}...")
            except Exception as e:
                status.append(f"       读取失败: {e}")
    
    return "<br>".join(status)

from api.modules.passport import passport_blu
app.register_blueprint(passport_blu)
if __name__ == '__main__':
    app.run(debug=True)