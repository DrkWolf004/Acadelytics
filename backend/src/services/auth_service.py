from datetime import datetime, timedelta

import jwt
from config.configEnv import ACCESS_TOKEN_SECRET


def create_access_token(user_data: dict, expires_in_minutes: int = 60) -> str:
    if not ACCESS_TOKEN_SECRET:
        raise RuntimeError("ACCESS_TOKEN_SECRET no está configurado en el entorno")

    payload = {
        "sub": str(user_data.get("id")) if user_data.get("id") is not None else None,
        "id": user_data.get("id"),
        "correo": user_data.get("correo"),
        "rol": user_data.get("rol"),
        "exp": datetime.utcnow() + timedelta(minutes=expires_in_minutes),
        "iat": datetime.utcnow(),
    }

    return jwt.encode(payload, ACCESS_TOKEN_SECRET, algorithm="HS256")
