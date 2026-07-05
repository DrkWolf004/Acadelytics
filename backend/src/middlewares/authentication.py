from functools import wraps

import jwt
from flask import g, request

from config.configEnv import ACCESS_TOKEN_SECRET
from handlers.response_handlers import handle_error_client, handle_error_server


def authenticate_jwt(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        authorization = request.headers.get("Authorization", "")
        token = None

        if authorization.startswith("Bearer "):
            token = authorization.split(" ", 1)[1].strip()
        elif request.is_json and isinstance(request.json, dict):
            token = request.json.get("token") or request.json.get("access_token")
        elif request.args.get("token"):
            token = request.args.get("token")

        if not token:
            return handle_error_client(
                401,
                "No tienes permiso para acceder a este recurso",
                {"info": "Token de autorización no proporcionado."},
            )

        if not ACCESS_TOKEN_SECRET:
            return handle_error_server(500, "No se ha configurado el secreto de token.")

        try:
            payload = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=["HS256"])
            g.current_user = payload
            return func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return handle_error_client(
                401,
                "Token expirado",
                {"info": "El token ha caducado."},
            )
        except jwt.InvalidTokenError:
            return handle_error_client(
                401,
                "Token inválido",
                {"info": "No se pudo verificar el token."},
            )
        except Exception as error:
            return handle_error_server(500, f"Error de autenticación en el servidor: {error}")

    return wrapper
