from flask import Blueprint
from app.routes.user_routes import bp as user_bp
from app.routes.auth_routes import bp as auth_bp

bp = Blueprint('main', __name__)

# Los blueprints ya definen su propio `url_prefix` (p. ej. '/auth', '/users').
# Registrarlos sin añadir otro prefijo evita rutas duplicadas como '/auth/auth/...'.
bp.register_blueprint(auth_bp)
bp.register_blueprint(user_bp)

@bp.route('/')
def home():
    return 'Backend Flask funcionando'
