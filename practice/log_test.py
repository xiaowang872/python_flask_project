# # # import logging

# # # #使用普通的格式化器
# # # formatter = logging.Formatter('%(asctime)s -%(name)s - %(levelname)s - %(message)s')
# # # handler = logging.StreamHandler()
# # # handler.setFormatter(formatter)


# # # logger = logging.getLogger()
# # # logger.addHandler(handler)

# # # logger.warning('this is a log message 用户操作哦',extra= {'user_id':123,'action':'login'})

# # # logging.warning("这是一条警告消息")  # 这应该会输出
# # # logging.info("这是一条信息消息")    # 这可能不会输出

# # # # 问题： extra 参数中的自定义字段（user_id, action）完全丢失！


# # import logging
# # import json

# # # 方案1：简单修正
# # formatter = logging.Formatter(
# #     '%(asctime)s - %(name)s - %(levelname)s - %(message)s - user_id:%(user_id)s - action:%(action)s'
# # )

# # handler = logging.StreamHandler()
# # handler.setFormatter(formatter)

# # logger = logging.getLogger()
# # logger.addHandler(handler)
# # logger.setLevel(logging.INFO)

# # # 现在自定义字段会正确显示
# # logger.warning('this is a log message 用户操作哦', extra={'user_id':123,'action':'login'})
# # logger.info("这是一条信息消息", extra={'user_id':456,'action':'logout'})
# import logging

# formatter = logging.Formatter(
#     '%(asctime)s - %(name)s - %(levelname)s - %(message)s - user_id:%(user_id)s - action:%(action)s'
# )

# # 控制台处理器
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(formatter)

# # 文件处理器
# file_handler = logging.FileHandler('./practice/logs/app.logs', encoding='utf-8')
# file_handler.setFormatter(formatter)

# logger = logging.getLogger()
# logger.addHandler(console_handler)  # 输出到控制台
# logger.addHandler(file_handler)     # 输出到文件
# logger.setLevel(logging.INFO)

# logger.warning('this is a log message 用户操作哦', extra={'user_id':123,'action':'login'})
# logger.info("这是一条信息消息", extra={'user_id':456,'action':'logout'})
import logging
from pythonjsonlogger import jsonlogger
from datetime import datetime , timezone

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

# 使用示例
formatter = CustomJsonFormatter(
    '%(timestamp)s %(level)s %(name)s %(message)s %(user_id)s %(action)s'
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# 输出 JSON 格式的日志
logger.info('用户登录成功', extra={'user_id': 123, 'action': 'login'})