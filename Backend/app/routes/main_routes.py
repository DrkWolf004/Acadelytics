from flask import Blueprint
from app.routes.user_routes import user_bp


bp = Blueprint('main', __name__)
bp.register_blueprint(user_bp)

@bp.route('/')
def home():
    return 'Backend Flask funcionando'