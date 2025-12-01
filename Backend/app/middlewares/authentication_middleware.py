from functools import wraps
from flask import request, jsonify, current_app
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        if not token:
            return jsonify({'error': 'Token es obligatorio'}), 401
        try:
            data = jwt.decode(token, current_app.config['ACCESS_TOKEN_SECRET'], algorithms=['HS256'])
            current_user_id = data['id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token ha expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401

        return f(current_user_id, *args, **kwargs)
    return decorated
