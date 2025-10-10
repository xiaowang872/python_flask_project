# # F:\vue_flask_project\vue_flask_project_one\flask\pythonProject1\api\modules\video\views.py

# import logging
# from api.utils.log_utils import json_log
# json_log('user_action','/logs/user_action.log')
# user_action_log = logging.getLogger('user_action')

import logging
import os

# 确保目录存在
if not os.path.exists('logs'):
    os.makedirs('logs', exist_ok=True)

# 直接配置基础日志（不依赖复杂的json_log）
logger = logging.getLogger('user_action')
logger.setLevel(logging.INFO)

# 如果还没有handler，就添加一个
if not logger.handlers:
    handler = logging.FileHandler('logs/user_action.log', encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

user_action_log = logger