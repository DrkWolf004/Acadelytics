from flask import Blueprint
from app.controllers.file_controller import (
    get_file,
    get_files,
    create_file,
    update_file,
    delete_file,
)
from app.middlewares.authentication_middleware import token_required

bp = Blueprint('files', __name__, url_prefix='/files')

@bp.before_request
@token_required
def before_request_func(Token_user_id):
    pass


bp.route('/', methods=['GET'])(get_files)
bp.route('/', methods=['POST'])(create_file)
bp.route('/detail/', methods=['GET'])(get_file)
bp.route('/detail/', methods=['PATCH'])(update_file)
bp.route('/detail/', methods=['DELETE'])(delete_file)