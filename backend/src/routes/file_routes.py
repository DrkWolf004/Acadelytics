import mimetypes
import os

from flask import Blueprint, request, send_file

from controllers.file_controller import (
    create_file_controller,
    delete_file_controller,
    edit_file_controller,
    get_file_by_id_controller,
    get_files_controller,
    upload_file_controller,
)
from services.file_service import get_file_by_id
from middlewares.authentication import authenticate_jwt

file_blueprint = Blueprint("file_blueprint", __name__)


@file_blueprint.route("/upload/<int:class_folder_id>", methods=["POST"], strict_slashes=False)
@authenticate_jwt
def upload_file_route(class_folder_id: int):
    """Upload a file to a specific class folder."""
    if "file" not in request.files:
        return {"status": "error", "message": "No file part provided", "code": 400}, 400
    
    file = request.files["file"]
    return upload_file_controller(class_folder_id, file)


@file_blueprint.route("", methods=["POST"], strict_slashes=False)
@authenticate_jwt
def create_file_route():
    return create_file_controller(request.get_json() or {})


@file_blueprint.route("", methods=["GET"], strict_slashes=False)
@authenticate_jwt
def get_files_route():
    class_folder_id = request.args.get("class_folder_id", type=int)
    return get_files_controller(class_folder_id)


@file_blueprint.route("/<int:file_id>", methods=["GET"])
@authenticate_jwt
def get_file_by_id_route(file_id: int):
    return get_file_by_id_controller(file_id)


@file_blueprint.route("/<int:file_id>/raw", methods=["GET"])
@authenticate_jwt
def get_file_raw_route(file_id: int):
    file_record = get_file_by_id(file_id)
    if file_record is None:
        return {"status": "error", "message": "File no encontrado.", "code": 404}, 404
    if not os.path.exists(file_record.filepath):
        return {"status": "error", "message": "Archivo no encontrado.", "code": 404}, 404

    mimetype, _ = mimetypes.guess_type(file_record.filename)
    return send_file(file_record.filepath, mimetype=mimetype or "application/octet-stream", as_attachment=False)


@file_blueprint.route("/<int:file_id>", methods=["PUT"])
@authenticate_jwt
def update_file_route(file_id: int):
    return edit_file_controller(file_id, request.get_json() or {})


@file_blueprint.route("/<int:file_id>", methods=["DELETE"])
@authenticate_jwt
def delete_file_route(file_id: int):
    return delete_file_controller(file_id)
