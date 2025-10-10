from sqlalchemy import text  # 添加这行导入
def test_mysql(app, db):
    """测试MySQL连接"""
    try:
        with app.app_context():
            db.session.execute(text('SELECT 1'))
        print("✅ MySQL连接成功")
        return True
    except Exception as e:
        print(f"❌ MySQL连接失败: {e}")
        return False
