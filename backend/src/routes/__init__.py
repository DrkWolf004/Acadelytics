from flask import Flask

from .auth_routes import auth_blueprint
from .user_routes import user_blueprint


def register_routes(app: Flask) -> None:
    app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
    app.register_blueprint(user_blueprint, url_prefix="/api/users")
