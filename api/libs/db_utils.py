from sqlalchemy.exc import SQLAlchemyError
from api import db

def session_commit():
    """提交数据库会话，并处理可能的异常"""
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()  # 回滚会话以防止数据不一致
        reason = str(e)
        print(f"数据库操作失败: {reason}")
        return reason