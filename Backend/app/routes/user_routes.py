from flask import Blueprint
from app.controllers.user_controller import get_user, get_users, update_user, delete_user
from app.middlewares.authentication_middleware import token_required
from app.middlewares.authorization_middleware import admin_required

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.before_request
@token_required
@admin_required
def before_request_func(Token_user_id):
    pass
    

bp.route('/', methods=['GET'])(get_users)
bp.route('/detail/', methods=['GET'])(get_user)
bp.route('/detail/', methods=['PATCH'])(update_user)
bp.route('/detail/', methods=['DELETE'])(delete_user)
