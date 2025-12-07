from flask import Blueprint
from app.controllers.classFolder_controller import (
    get_classfolder,
    get_classfolders,
    create_classfolder,
    update_classfolder,
    delete_classfolder,
)
from app.middlewares.authentication_middleware import token_required

bp = Blueprint('classfolders', __name__, url_prefix='/classfolders')

@bp.before_request
@token_required
def before_request_func(Token_user_id):
    pass

bp.route('/', methods=['GET'])(get_classfolders)
bp.route('/', methods=['POST'])(create_classfolder)
bp.route('/detail/', methods=['GET'])(get_classfolder)
bp.route('/detail/', methods=['PATCH'])(update_classfolder)
bp.route('/detail/', methods=['DELETE'])(delete_classfolder)