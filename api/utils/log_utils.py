import logging
from logging.handlers import RotatingFileHandler
def setup_log(logger_name=None,log_file='logs/log',level = logging.INFO):
    # 设置日志的几录等级
    logging.basicConfig(level=level)  # 控制台打印日志,调试debug等级
    # 穿件日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    file_log_handler =  RotatingFileHandler(log_file,maxBytes=1024*1024*100,backupCount=10,encoding='utf-8')
    # 创建日志记录的格式            日志等级  输入日志信息文件名 行数  日志信息
    formatter = logging.Formatter('%(asctime)s - %(levelname)s %(filename)s: %(lineno)d %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（ flask app 使用的）添加日志记录器
    logging.getLogger(logger_name).addHandler(file_log_handler)


def setup_logger(logger_name,log_file,level= logging.INFO):



    """
    %(asctime) 即日志记录时间，精确到毫秒
    %(levelname) 即日志级别
    %(filename) 即日志记录的python文件名
    %(functionname) 即触发日志记录的函数名
    %(lineno) 即触发日志代码记录的行号
    %(message) 这项及调用如app.logger.info('info log')时传入的参数，即message   
    :param logger_name:
    :param log_file:
    :param level:
    :return:
    """
    log = logging.getLogger(logger_name)
    # 创建日志对象
    formatter = logging.Formatter('%(asctime)s : %(message)s')
    # 创建日志记录格式,即日志记录时间和日志内容
    file_handler  = logging.FileHandler(log_file,mode='w',encoding='utf-8')
    # 创建日志记录器，将日志保存名为log_file的文件中，mode='w'表示每次运行程序时覆盖之前的日志
    file_handler.setFormatter(formatter)
    # 将日志格式设置为文件处理器的格式
    stream_handler = logging.StreamHandler()
    # 创建一个文件处理器，将日志输出到控制台
    stream_handler.setFormatter(formatter)
    # 将文件处理器设置为流处理器的格式
    log.setLevel(level)
    # 将你的日志级别设置为传入的参数level
    log.addHandler(file_handler)
    log.addHandler(stream_handler)
    # 将文件处理器和流处理器添加到日志对象中

#############################################################
# 这边的json_log()函数用于将日志以JSON格式记录到文件中（支持日志滚动）。
# 自己写的，不确定是否兼容
import json
from pythonjsonlogger import jsonlogger
from datetime import datetime, timezone
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            # now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            # log_record['timestamp'] = now    这里utcnown()函数已经被弃用了
            log_record['timestamp'] = datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname




import os

def json_log(logger_name, log_file, level=logging.INFO):

# ###############添加了日志路径guixiang###############

    if log_file is None:
        log_file = 'logs/user_action.log'
    
    # 确保使用绝对路径
    if not os.path.isabs(log_file):
        # 获取项目根目录（根据您的项目结构调整）
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        log_file = os.path.join(project_root, log_file)
    
    abs_log_path = os.path.abspath(log_file)
    log_dir = os.path.dirname(abs_log_path)
    
    print(f"🔍 日志文件路径: {abs_log_path}")
    
    # 确保日志目录存在
    try:
        if not os.path.exists(log_dir):
            print(f"🛠️ 创建日志目录: {log_dir}")
            os.makedirs(log_dir, exist_ok=True)
    except Exception as e:
        print(f"❌ 创建日志目录失败: {e}")
        # 使用当前目录作为备选
        log_file = 'user_action.log'
        abs_log_path = os.path.abspath(log_file)






    logging.basicConfig(level=level)  # 调试debug级
    logger = logging.getLogger(logger_name)
    # log_handler = logging.StreamHandler()
    log_handler = logging.FileHandler(log_file)
    # formatter = jsonlogger.JsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
    formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s %(message)s')
    # formatter = jsonlogger.JsonFormatter(json_encoder=json.JSONEncoder)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
