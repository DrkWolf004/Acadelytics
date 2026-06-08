from flask import Flask

from .auth_routes import auth_blueprint
from .user_routes import user_blueprint
from .classroom_routes import classroom_blueprint
from .class_folder_routes import class_folder_blueprint
from .file_routes import file_blueprint
from .classroom_invitation_routes import invitation_blueprint


def register_routes(app: Flask) -> None:
    app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
    app.register_blueprint(user_blueprint, url_prefix="/api/users")
    app.register_blueprint(classroom_blueprint, url_prefix="/api/classrooms")
    app.register_blueprint(class_folder_blueprint, url_prefix="/api/classfolders")
    app.register_blueprint(file_blueprint, url_prefix="/api/files")
    app.register_blueprint(invitation_blueprint, url_prefix="/api/invitations")
