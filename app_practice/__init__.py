from flask import Flask
from app_practice.index import index_blu



app = Flask(__name__)
app.register_blueprint(index_blu, url_prefix='/example')#加了前缀，访问路径变为 /example/
# app.register_blueprint(index_blu)  # 不加前缀，直接访问