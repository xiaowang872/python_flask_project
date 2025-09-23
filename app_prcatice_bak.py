from flask import Flask,render_template,request,url_for,abort
from datetime import datetime
from werkzeug.routing import BaseConverter
import re

app = Flask(__name__)

# 确保路由函数名与模板中使用的一致
@app.route('/')
def index():  # 函数名为index，对应url_for('index')
    return render_template('index_with_link.html')

@app.route('/tmp')
def tmp_page():  # 函数名为tmp_page，对应url_for('tmp_page')
    return render_template('tmp.html')

@app.route('/Custom_routing')
def Custom_routing_page():  
    return render_template('/Custom_routing/index.html')
# Custom_routing

# 表单参数实例
@app.route('/route_message_parameter/index.html')
def route_message_parameter():
    return render_template('/route_message_parameter/index.html')
@app.route('/route_message_parameter/message_form', methods=['POST'])
def route_message_parameter_message_form():
    # 处理POST请求
    try:
        name = request.form.get('name')
        location = request.form.get('location')
        age = request.form.get('age')
        if not name or not location or not age:
            return "请填写所有字段", 400
        return f'你好, {name}，你来自{location}，你今年{age}岁。'
    except Exception as e:
        return f'发生错误: {str(e)}', 400

################     自定义路由     ##########################
class DateConverter(BaseConverter):
    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d')
    def to_url(self, value):
        return value.strftime('%Y-%m-%d')
# 注册自定义转换器,现在转换器名字叫date
app.url_map.converters['date'] = DateConverter
@app.route('/Custom_route/date_event/<date:custom_date>')
def show_date_event(custom_date):
    # 现在custom_date是一个datetime对象
    print(custom_date)
    return f'今天是{custom_date.strftime("%Y-%m-%d")}，欢迎来到自定义路由！'

@app.route('/generate_url')
def generate_url():
    specific_date = datetime(2024, 6, 15)
    return url_for('show_date_event', custom_date=specific_date)
# regex正则表达式路由
class RegexConverter(BaseConverter):
    def __init__(self,url_map,regex):
        # 重写父类方法
        super(RegexConverter,self).__init__(url_map)
        # 原始的 BaseConverter 没有存储正则表达式的机制，我们需要自己保存：(说以有这一步)
        self.regex = regex  #保存正则表达式
    def to_python(self,value):
        print('你好，这里调用了to_python'+value)
        return value
app.url_map.converters['my_cv_regex'] = RegexConverter
@app.route("/user/<my_cv_regex(r'1[3456789]\d{9}'):user_id>")
def get_user(user_id):
    if not re.match(r'1[3456789]\d{9}', user_id):
        abort(404)  # 如果不匹配，返回404错误
        return None #其实这边return不会执行到
    # try-except捕获异常
    try:
        if re.match(r'1[3456789]\d{9}', user_id):
            print(f"格式正确，用户ID: {user_id}")
            return render_template('Custom_routing/user.html', user_id=user_id)
        # 我这边没有建立user.html模板，所以会报错让except捕获400，我没处理是为了和404对比
    except Exception as e:
        return f"发生错误: {str(e)}", 400
    # return f"格式正确，用户ID: {user_id}"
#如果输出错误控制台会抛出 127.0.0.1 - - [17/Sep/2025 10:18:18] "GET /user/187999999990 HTTP/1.1" 404 -


################     异常捕获     ##########################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)  # 启用自动重载，确保代码修改被加载 吟游提瓦特诗人 

