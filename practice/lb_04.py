# 它的作用就是连接mysql数据库服务器
import pymysql
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
    connection = pymysql.connect(
        host='192.168.117.200',
        port = 3306,
        user = 'root',
        password = '123456',
        database='flask_databases',
    )
    return "数据库连接成功！"
if __name__ == '__main__':
    app.run()