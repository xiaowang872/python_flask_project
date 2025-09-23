# api/models/__init__.py
from .base import BaseModels
from .user import UserInfo  # 导出 UserInfo

__all__ = ['BaseModels', 'UserInfo']