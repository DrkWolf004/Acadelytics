from functools import wraps
from flask import jsonify
from app.models.user_model import user

def admin_required(f):
    @wraps(f)
    def decorated(current_user_id, *args, **kwargs):
        user_obj = user.query.get(current_user_id)
        if not user_obj:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        if user_obj.rol.lower() != 'administrador':
            return jsonify({
                'error': 'Acceso denegado',
                'message': 'Se requiere rol de administrador para esta acción.'
            }), 403
        
        return f(current_user_id, *args, **kwargs)
    return decorated
