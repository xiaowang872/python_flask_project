# F:\vue_flask_project\vue_flask_project_one\flask\pythonProject1\api\modules\passport\__init__.py

from flask import Blueprint

passport_blu = Blueprint('passport', __name__, url_prefix='/passport')

from . import views