# practice/secret_key_practice.py
import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import create_app, db

def create_test_user():
    """创建测试用户"""
    app = create_app('dev')
    
    with app.app_context():
        # 动态导入，避免循环导入问题
        from api.modules.auth.login import UserLogin
        
        # 检查用户是否已存在
        existing_user = UserLogin.query.filter_by(mobile='13800138000').first()
        if existing_user:
            print("⚠️  测试用户已存在，跳过创建")
            return True
        
        # 创建新用户
        user = UserLogin()
        user.mobile = '13800138000'
        user.password = '123456'
        user.user_id = 1
        
        db.session.add(user)
        db.session.commit()
        print("✅ 测试用户创建成功")
        return True

def delete_test_user():
    """删除测试用户"""
    app = create_app('dev')
    
    with app.app_context():
        from api.modules.auth.login import UserLogin
        
        user = UserLogin.query.filter_by(mobile='13800138000').first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print("✅ 测试用户已删除")
            return True
        else:
            print("⚠️  测试用户不存在，无需删除")
            return False

def test_login():
    """测试登录功能"""
    app = create_app('dev')
    
    with app.app_context():
        from api.modules.auth.login import UserLogin
        
        def login(mobile, password):
            user = UserLogin.query.filter_by(mobile=mobile).first()
            if user and user.check_password(password):
                print(f"✅ 登录成功 - 用户ID: {user.id}")
                return True
            else:
                print("❌ 手机号或密码错误")
                return False
        
        print("\n🔐 开始登录测试...")
        login('13800138000', '123456')      # ✅ 返回 True
        login('13800138000', 'wrong_pass')  # ❌ 返回 False

if __name__ == '__main__':
    create_test_user()
    test_login()
    delete_test_user()