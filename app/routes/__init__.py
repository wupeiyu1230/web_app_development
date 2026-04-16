from flask import Blueprint

# 本專案將透過 Blueprint 來模組化各個功能的路由
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
recipes_bp = Blueprint('recipes', __name__, url_prefix='/recipes')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 匯入路由使其生效 (避免 Circular Import 故於下方匯入)
from app.routes import main, auth, recipes, admin
