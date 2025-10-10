# F:\vue_flask_project\vue_flask_project_one\flask\pythonProject1\api\models\user.py
# 用于存放用户信息表示
from api import db
from api.models.base import BaseModels
from datetime import datetime
from api.models.message import Message
from werkzeug.security import generate_password_hash, check_password_hash
class UserLogin(BaseModels,db.Model):
# 其中 BaseModels 是一个基础模型类，db.Model 是一个数据库模型类。模型里面包含的字段就是登录功能相关的字段信息。
    """用户登录模型"""
    __tablename__ = 'user_login'  # 指定表名为 user_login
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键，自增
    mobile = db.Column(db.String(16),unique=True,nullable=False)  # 手机号，唯一且不能为空
    password_hash = db.Column(db.String(255),nullable=False)  # 密码哈希值，不能为空
    user_id = db.Column(db.Integer,nullable=False)  # 用户ID，不能为空
    last_login = db.Column(db.DateTime, default= datetime.now)  # 最后登录时间
    last_login_stamp = db.Column(db.Integer) #最后登录时间戳
    @property
    # 将一个属性方法封装成属性
    def password(self):
        raise AttributeError('密码不可读(密码属性不可直接获取)')
    @password.setter
    # 定义password的setter方法
    def password(self, value):
        self.password_hash = generate_password_hash(value)
    # 传入的是明文，效验明文和数据库里的hash之后密码，正确为true
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UserInfo(BaseModels,db.Model):
    """用户信息模型表"""
    __tablename__ = 'user_info'
    id = db.Column(db.Integer,primary_key = True , autoincrement = True) #用户id
    nickname = db.Column(db.String(64),nullable = False) #用户昵称
    mobile = db.Column(db.String(16))  #手机号
    avatar_url = db.Column(db.String(256)) #用户头像路径
    signature = db.Column(db.String(256)) #签名
    sex = db.Column(db.Enum('0','1','2'),default = '0')  #性别 0-暂时不写 1-男 2-女
    birth_date = db.Column(db.DateTime) #出生日期
    role_id = db.Column(db.Integer) #角色id
    is_admin = db.Column(db.SmallInteger,default = 0)
    last_message_read_time = db.Column(db.DateTime)
    def new_messages_counts(self):
        last_read_time = self.last_message_read_time or datetime(1900,1,1)
        return Message.query.filter_by(recipient_id = self.id).filter(Message.timestamp > last_read_time).count()
    
    def to_dict(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'mobile': self.mobile,
            'avatar_url': self.avatar_url,
            'sex': self.sex,
        }
    # to_dict 函数可以将 UserInfo 对象序列化为 JSON 数据，这样就能在查询时将查询到的数据放在 Flask 的响应中。这里的学习重点就是掌握创建方法

