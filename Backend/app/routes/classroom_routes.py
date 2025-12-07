from flask import Blueprint
from app.controllers.classroom_controller import (
    get_classroom,
    get_classrooms,
    create_classroom,
    update_classroom,
    delete_classroom,
)
from app.middlewares.authentication_middleware import token_required

bp = Blueprint('classrooms', __name__, url_prefix='/classrooms')

@bp.before_request
@token_required
def before_request_func(Token_user_id):
    pass


bp.route('/', methods=['GET'])(get_classrooms)
bp.route('/', methods=['POST'])(create_classroom)
bp.route('/detail/', methods=['GET'])(get_classroom)
bp.route('/detail/', methods=['PATCH'])(update_classroom)
bp.route('/detail/', methods=['DELETE'])(delete_classroom)
