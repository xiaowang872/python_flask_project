from flask import Flask, request
from flask_restful import Api, Resource,reqparse

app = Flask(__name__)
api = Api(app)

class HelloWord_Flask_one(Resource):
    def get(self):
        return {"message": "Hello World!"}
    def post(self):
        # 处理POST请求
        data = request.get_json()  # 获取JSON数据
        return {"received": data}, 201  # 返回接收到的数据和状态码
api.add_resource(HelloWord_Flask_one, '/hello')

class HelloWord_Flask_two(Resource):
    # 创建一个RequestParser对象,用于解析请求参数,设置规则
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='name参数不能为空')
    parser.add_argument('location', type=str, required=True, help='location参数不能为空')
    parser.add_argument('age', type=int, required=True, help='age参数不能为空')
   
    def get(self):
        return {"message": "Hello World!"}
    def post(self):
        # 处理post请求
        args = self.parser.parse_args()  # 解析请求参数
        # 验证参数
        name = args['name']
        location = args['location']
        age = args['age']
        return {"name": name, "location": location, "age": age}, 201
api.add_resource(HelloWord_Flask_two, '/')
        

     

if __name__ == '__main__':
    app.run(debug=True)