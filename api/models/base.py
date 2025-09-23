from datetime import datetime
from api import db
from api.libs.db_utils import session_commit

class BaseModels:
    '''这边guixiang创建了一个模型的基类'''
    create_time = db.Column(db.DateTime, default=datetime.now)  # 创建一个名为 create_time 的字段，类型是 DateTime
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 创建一个名为 update_time 的字段，类型是 DateTime
    status = db.Column(db.Integer, default=1)  # 创建一个名为 status 的字段，类型是 Integer
    def add(self,obj):
        db.session.add(obj)           # 第一步：将对象添加到会话
        return session_commit()       # 第二步：提交事务并返回结果
    def update(self):
        return session_commit()
    def delete(self):
        self.status = 0               # 将状态标记为删除
        return session_commit()
# 添加验证：打印基类，确认导入成功
print("成功导入 BaseModels：", BaseModels)
print("BaseModels 的属性：", dir(BaseModels))  # 查看是否包含 create_time 等字段
