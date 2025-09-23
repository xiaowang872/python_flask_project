from flask import jsonify
class HttpCode(object):
    ok = 200               # 成功
    params_error = 400     # 参数错误
    server_error = 500     # 服务器错误
    auth_error = 401       # 认证错误
    method_error = 405     # 方法不允许
    db_error = 1001        # 自定义数据库错误
def rep_result(code,msg,data):
    #{"code"= 200,"msg" = 'baababaab',"data"={}}
    return jsonify({
        'code': code,
        'msg': msg,
        'data': data or {}  # data为空时，返回{},就是确保data不为空
    })
def success(msg,data = None):
    return rep_result(code = HttpCode.ok,msg = msg,data = data)
def error(code,msg,data = None):
    return rep_result(code = code,msg = msg,data = data)

