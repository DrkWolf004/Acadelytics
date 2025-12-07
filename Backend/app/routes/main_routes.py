from flask import Blueprint
from app.routes.user_routes import bp as user_bp
from app.routes.auth_routes import bp as auth_bp
from app.routes.classroom_routes import bp as classroom_bp
from app.routes.classFolder_routes import bp as classfolder_bp
from app.routes.file_routes import bp as file_bp

bp = Blueprint('main', __name__)

bp.register_blueprint(auth_bp)
bp.register_blueprint(user_bp)
bp.register_blueprint(classroom_bp)
bp.register_blueprint(classfolder_bp)
bp.register_blueprint(file_bp)

@bp.route('/')
def home():
    return 'Backend Flask funcionando'
