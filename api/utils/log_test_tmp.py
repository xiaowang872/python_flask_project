import logging
import os
import sys

# 导入同目录下的log_utils模块
from log_utils import setup_log, setup_logger

def get_absolute_log_path(relative_path):
    """将相对路径转换为绝对路径"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, relative_path)

def test_basic_functionality():
    """测试基本功能"""
    print("=== 基本功能测试 ===")
    
    # 使用绝对路径
    app_log_path = get_absolute_log_path('logs/app.log')
    dev_log_path = get_absolute_log_path('logs/dev.log')
    
    # 确保日志目录存在
    log_dir = os.path.dirname(app_log_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"创建日志目录: {log_dir}")
    
    # 测试setup_log函数
    print("1. 测试setup_log函数...")
    setup_log('app_logger', app_log_path, logging.DEBUG)
    app_logger = logging.getLogger('app_logger')
    
    app_logger.debug("调试信息 - 测试setup_log")
    app_logger.info("普通信息 - 用户登录成功")
    app_logger.warning("警告信息 - 内存使用率过高")
    app_logger.error("错误信息 - 数据库连接失败")
    print("setup_log测试完成")
    
    # 测试setup_logger函数
    print("2. 测试setup_logger函数...")
    setup_logger('dev_logger', dev_log_path, logging.DEBUG)
    dev_logger = logging.getLogger('dev_logger')
    
    dev_logger.debug("调试信息 - 测试setup_logger")
    dev_logger.info("普通信息 - API请求处理完成")
    dev_logger.warning("警告信息 - 响应时间过长")
    dev_logger.error("错误信息 - 文件不存在")
    print("setup_logger测试完成")

def test_different_log_levels():
    """测试不同的日志级别"""
    print("\n=== 不同日志级别测试 ===")
    
    # 测试INFO级别
    info_log_path = get_absolute_log_path('logs/info.log')
    setup_log('info_logger', info_log_path, logging.INFO)
    info_logger = logging.getLogger('info_logger')
    
    info_logger.debug("这条DEBUG信息不会被记录")  # 不会记录
    info_logger.info("这条INFO信息会被记录")
    info_logger.warning("这条WARNING信息会被记录")
    print("INFO级别测试完成")
    
    # 测试ERROR级别
    error_log_path = get_absolute_log_path('logs/error.log')
    setup_logger('error_logger', error_log_path, logging.ERROR)
    error_logger = logging.getLogger('error_logger')
    
    error_logger.debug("DEBUG - 不会记录")
    error_logger.info("INFO - 不会记录")
    error_logger.warning("WARNING - 不会记录")
    error_logger.error("ERROR - 会被记录")
    print("ERROR级别测试完成")

def test_log_format_differences():
    """测试两个函数的日志格式区别"""
    print("\n=== 日志格式区别测试 ===")
    
    # setup_log的详细格式
    detailed_path = get_absolute_log_path('logs/detailed.log')
    setup_log('detailed', detailed_path)
    detailed_logger = logging.getLogger('detailed')
    detailed_logger.info("这是setup_log的日志格式")
    
    # setup_logger的简化格式
    simple_path = get_absolute_log_path('logs/simple.log')
    setup_logger('simple', simple_path)
    simple_logger = logging.getLogger('simple')
    simple_logger.info("这是setup_logger的日志格式")
    
    print("日志格式测试完成")

def test_multiple_loggers():
    """测试多个日志记录器同时工作"""
    print("\n=== 多日志记录器测试 ===")
    
    # 创建不同用途的日志记录器
    db_path = get_absolute_log_path('logs/db.log')
    api_path = get_absolute_log_path('logs/api.log')
    security_path = get_absolute_log_path('logs/security.log')
    
    setup_log('database', db_path, logging.INFO)
    setup_logger('api', api_path, logging.DEBUG)
    setup_log('security', security_path, logging.WARNING)
    
    db_logger = logging.getLogger('database')
    api_logger = logging.getLogger('api')
    security_logger = logging.getLogger('security')
    
    # 模拟数据库操作
    db_logger.info("数据库连接池初始化")
    db_logger.info("执行SQL: SELECT * FROM users WHERE id = 1")
    
    # 模拟API请求
    api_logger.debug("收到GET请求: /api/users")
    api_logger.info("用户认证通过")
    api_logger.warning("查询参数验证警告")
    
    # 模拟安全事件
    security_logger.warning("检测到多次登录失败尝试")
    security_logger.error("IP地址被封禁")
    
    print("多日志记录器测试完成")

def test_error_with_traceback():
    """测试错误堆栈跟踪"""
    print("\n=== 错误堆栈跟踪测试 ===")
    
    exception_path = get_absolute_log_path('logs/exception.log')
    setup_log('exception_logger', exception_path)
    exception_logger = logging.getLogger('exception_logger')
    
    def simulate_error():
        # 模拟一个会出错的分支
        data = {"key": "value"}
        return data["nonexistent_key"]  # 这里会抛出KeyError
    
    try:
        simulate_error()
    except Exception as e:
        exception_logger.error("发生了一个异常", exc_info=True)
        exception_logger.error(f"错误详情: {str(e)}")
    
    print("错误堆栈跟踪测试完成")

def test_real_world_scenario():
    """模拟真实使用场景"""
    print("\n=== 真实场景模拟 ===")
    
    # 模拟用户服务
    user_service_path = get_absolute_log_path('logs/user_service.log')
    setup_log('user_service', user_service_path)
    user_logger = logging.getLogger('user_service')
    
    # 模拟用户注册流程
    def register_user(username, email):
        user_logger.info(f"开始用户注册流程 - 用户名: {username}, 邮箱: {email}")
        
        # 验证用户信息
        if not username or not email:
            user_logger.error("用户名或邮箱为空")
            return False
            
        user_logger.debug("用户信息验证通过")
        
        # 检查用户是否已存在
        user_logger.info("检查用户是否已存在")
        
        # 模拟创建用户
        try:
            # 这里模拟可能出错的数据库操作
            if username == "admin":
                raise Exception("管理员用户已存在")
                
            user_logger.info(f"用户 {username} 注册成功")
            return True
        except Exception as e:
            user_logger.error(f"用户注册失败: {str(e)}", exc_info=True)
            return False
    
    # 测试用户注册
    register_user("john_doe", "john@example.com")
    register_user("admin", "admin@example.com")  # 这个会失败
    register_user("", "test@example.com")  # 这个也会失败
    
    print("真实场景模拟完成")

def check_log_files():
    """检查生成的日志文件"""
    print("\n=== 日志文件检查 ===")
    
    log_dir = get_absolute_log_path('logs')
    if os.path.exists(log_dir):
        files = os.listdir(log_dir)
        print(f"生成的日志文件 ({len(files)} 个):")
        for file in sorted(files):
            file_path = os.path.join(log_dir, file)
            file_size = os.path.getsize(file_path)
            print(f"  - {file} ({file_size} 字节)")
            
            # 显示文件前几行内容
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:2]  # 只显示前2行
                    for line in lines:
                        print(f"    {line.strip()}")
            except Exception as e:
                print(f"    读取文件错误: {e}")
    else:
        print("日志目录不存在")

if __name__ == "__main__":
    print("开始测试 log_utils.py 中的日志函数")
    print("=" * 50)
    
    try:
        # 运行所有测试
        test_basic_functionality()
        test_different_log_levels()
        test_log_format_differences()
        test_multiple_loggers()
        test_error_with_traceback()
        test_real_world_scenario()
        
        # 检查生成的日志文件
        check_log_files()
        
        print("\n" + "=" * 50)
        print("所有测试完成！")
        print("\n总结：")
        print("1. setup_log - 使用RotatingFileHandler，支持日志轮转，格式详细")
        print("2. setup_logger - 使用FileHandler，每次覆盖，格式简化")
        print("3. 两个函数都支持控制台和文件输出")
        print("4. 日志文件保存在 api/utils/logs/ 目录下")
        
    except Exception as e:
        print(f"测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()