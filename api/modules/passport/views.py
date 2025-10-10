# F:\vue_flask_project\vue_flask_project_one\flask\pythonProject1\api\modules\passport\views.py

import re
from datetime import datetime
from flask import request, current_app, make_response

from api import redis_store
from api.models.user import UserLogin, UserInfo
from api.modules.passport import passport_blu
from api.modules.video.views import user_action_log  # 导入日志记录器
# from api.thirdparty.captcha import captcha
from api.utils.auth_helper import Auth
# from api.utils.common import auth_identify
from api.utils.constants import IMAGE_CODE_REDIS_EXPIRES
from api.utils.response_utils import error, HttpCode, success


@passport_blu.route('/logout', methods=['POST'])
def logout():
    """
    # 退出登陆(restful)
    # 请求路径: /passport/logout
    # 请求方式: POST
    # 请求参数: 无
    """
    response = Auth().identify(request)
    if response.get('code') == 200:
        user_id = response.get('data')['user_id']
        # 查询用户对象
        # 查询redis中的值  删除token相关信息
        try:
            redis_store.delete("jwt_token:%s" % user_id)
        except Exception as e:
            current_app.logger.error(e)
            return error(code=HttpCode.db_error, msg='redis删除token错误')

        # 记录退出日志
        try:
            user_action_log.warning(f"用户退出 - 用户ID: {user_id}, 时间: {datetime.now()}")
            print("✅ 退出日志记录成功")
        except Exception as e:
            print(f"记录退出日志失败: {e}")
        
        # 返回响应
        return success(msg="退出登陆成功")

    else:
        return success(msg=response.get('msg'))


@passport_blu.route('/login', methods=['POST'])
def login():
    """
    登陆接口
    :return:
    """
    data_dict = request.form
    mobile = data_dict.get('mobile')
    password = data_dict.get('password')
    img_code_id = data_dict.get("img_code_id")
    img_code = data_dict.get("img_code")
    # 判断参数对不对 需要有些验证
    # 2.校验参数
    if not all([mobile, password, img_code_id, img_code]):
        return error(code=HttpCode.parmas_error, msg='参数不完整')

    # 3.通过手机号取出用户对象
    try:
        user_login = UserLogin.query.filter(UserLogin.mobile == mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return error(code=HttpCode.db_error, msg='查询手机号异常')
    # 验证拿到的这个手机号  是否在我们的登陆信息中存在  异常捕获
    # user_login = UserLogin.query.filter(UserLogin.mobile == mobile).first()
    # 判断我们的用户信息不在返回错误的响应码
    if not user_login:
        return error(code=HttpCode.db_error, msg='用户不存在')
    try:
        redis_img_code = redis_store.get(f'img_code: {img_code_id}')
        # print(redis_img_code)
    except Exception as e:
        current_app.logger.error(e)
        return error(code=HttpCode.db_error, msg='验证码数据库查询异常')
    if not redis_img_code:
        return error(code=HttpCode.parmas_error, msg='验证码不存在')
    if img_code.lower() != redis_img_code.lower():
        return error(code=HttpCode.parmas_error, msg='验证码匹配不成功')
    
    # 调用Auth认证
    auth_result = Auth().authenticate(mobile, password)
    
    # 记录登录日志
    if auth_result.get('code') == 200:
        try:
            user_id = auth_result.get('data', {}).get('user_id')
            user_action_log.warning(f"用户登录 - 用户ID: {user_id}, 手机号: {mobile}, 时间: {datetime.now()}")
            print("✅ 登录日志记录成功")
        except Exception as e:
            print(f"记录登录日志失败: {e}")
    
    return auth_result


@passport_blu.route('/register', methods=['POST'])
def register():
    """
    注册接口
    :return: code msg
    """
    data_dict = request.form
    mobile = data_dict.get('mobile')
    password = data_dict.get('password')
    img_code_id = data_dict.get('img_code_id')  # cur_id
    img_code = data_dict.get('img_code')  # 填写的code

    if not all([mobile, password, img_code_id, img_code]):
        return error(code=HttpCode.parmas_error, msg='注册所需参数不能为空')

    # 2.1验证手机号格式
    if not re.match('1[3456789]\\d{9}', mobile):
        return error(code=HttpCode.parmas_error, msg='手机号格式不正确')

    # 3.通过手机号取出redis中的验证码
    redis_img_code = None
    # 从redis取出img_code_id对应的验证码
    try:
        redis_img_code = redis_store.get(f'img_code: {img_code_id}')
    except Exception as e:
        current_app.logger.errer(e)

    if not redis_img_code:
        return error(HttpCode.parmas_error, 'redis图片验证码获取失败')

    if img_code.lower() != redis_img_code.lower():
        return error(HttpCode.parmas_error, '图片验证码不正确')

    user_info = UserInfo()
    user_info.mobile = mobile
    user_info.nickname = mobile
    user_info.add(user_info)

    user_login = UserLogin()
    user_login.mobile = mobile
    user_login.password = password
    user_login.user_id = user_info.id
    user_login.add(user_login)

    # 记录注册日志
    try:
        user_action_log.warning(f"用户注册 - 手机号: {mobile}, 用户ID: {user_info.id}, 时间: {datetime.now()}")
        print("✅ 注册日志记录成功")
    except Exception as e:
        print(f"记录注册日志失败: {e}")

    return success('注册成功')


@passport_blu.route('/image_code')
def img_code():
    """
    生成图像验证码
    :return: 图片的响应
    """
    # 1.获取请求参数,args是获取?后面的参数
    cur_id = request.args.get('cur_id')
    pre_id = request.args.get('pre_id')
    # 2.生成图片验证码
    name, text, img_data = captcha.captcha.generate_captcha()
    # 3.保存到redis
    try:
        redis_store.set(f'img_code: {cur_id}', text, IMAGE_CODE_REDIS_EXPIRES)
        # 判断是否有上一个uuid,如果存在则删除
        if pre_id:
            redis_store.delete(f'img_code: {pre_id}')
    except Exception as e:
        current_app.logger.error(e)
        return error(HttpCode.db_error, 'redis存储失败')
    # 4. 返回图片验证码
    response = make_response(img_data)
    response.headers["Content-Type"] = "image/jpg"

    return response


@passport_blu.route('/check_mobile', methods=['POST'])
def check_mobile():
    """
    验证手机号
    # 请求路径: /passport/check_mobile
    # 请求方式: POST
    # 请求参数: mobile
    :return:code,msg
    """
    data_dict = request.form
    mobile = data_dict.get('mobile')

    try:
        users = UserLogin.query.all()
    except Exception as e:
        current_app.logger.error(e)
        return error(code=HttpCode.db_error, msg='查询用户信息异常')

    if mobile in [i.mobile for i in users]:
        return error(code=HttpCode.parmas_error, msg='手机号已存在，请重新输入')

    return success(msg=f'{mobile}，此手机号可以使用')