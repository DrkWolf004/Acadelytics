from flask import Blueprint
from app.controllers.auth_controller import login, register, logout

bp = Blueprint('auth', __name__, url_prefix='/auth')

bp.route('/login', methods=['POST'])(login)
bp.route('/register', methods=['POST'])(register)
bp.route('/logout', methods=['POST'])(logout)
