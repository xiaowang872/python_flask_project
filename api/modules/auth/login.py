from flask import current_app
from flask_restful import Resource, reqparse,inputs
from api.models.user import UserLogin
from api.utils.auth_helper import Auth
from api.utils.response_utils import error,HttpCode

#Login 类继承自 Resource，表示这是一个RESTful资源
class Login(Resource):
    '''用户登录接口'''
    def post(self):
        # 创建解析对象
        parser = reqparse.RequestParser(bundle_errors=True)
        # 添加参数
        parser.add_argument('mobile',type = inputs.regex('1[3456789]\\d{9}'),nullable = False,location = ['form']  ,required = True,help = '请输入正确的手机号')
        parser.add_argument('password',type = str,required = True,nullable = False,location = ['form'],help = '密码参数不正确')
        # location=['form'] 表示从 HTTP请求的表单数据（Form Data） 中获取参数值。
        # 解析参数
        args = parser.parse_args()
        # 通过手机号取出用户对象
        try:
            user_login = UserLogin.query.filter(UserLogin.mobile == args.mobile).first()
        except Exception as e:
            current_app.logger.error(e)
            return error(code = HttpCode.db_error,msg = '数据库查询异常(查询手机号异常)')
        # 验证拿到这个手机号，是否在我们的登录信息中存在  异常捕获
        # 判断我们的用户信息不在时，返回错误信息的响应码
        if not user_login:
            return error(code=HttpCode.db_error,msg='用户不存在')
        return Auth().authenticate(args.mobile,args.password)
            




