from app.models.user_model import user
from app import db
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
from flask import current_app

def login_service(data):
    email = data.get('correo')
    password = data.get('password')

    user_obj = user.query.filter_by(correo=email).first()
    if not user_obj:
        return None, {'dataInfo': 'correo', 'message': 'El correo electrónico es incorrecto'}

    if not user_obj.check_password(password):
        return None, {'dataInfo': 'password', 'message': 'La contraseña es incorrecta'}

    payload = {
        'id': user_obj.id,
        'correo': user_obj.correo,
        'rol': user_obj.rol,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }

    token = jwt.encode(payload, current_app.config['ACCESS_TOKEN_SECRET'], algorithm='HS256')
    return token, None

def register_service(data):
    nombre_completo = data.get('nombreCompleto', '').split()
    apellidos = ' '.join(nombre_completo[1:]) if len(nombre_completo) > 1 else nombre_completo[0] if nombre_completo else ''
    nombre = nombre_completo[0] if nombre_completo else ''
    correo = data.get('correo')
    password = data.get('password')
    rol = data.get('rol', 'Alumno')

    if user.query.filter_by(correo=correo).first():
        return None, {'dataInfo': 'correo', 'message': 'Correo electrónico en uso'}

    new_user = user(nombre=nombre, apellidos=apellidos, correo=correo, rol=rol)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    user_data = {
        'id': new_user.id,
        'nombre': new_user.nombre,
        'apellidos': new_user.apellidos,
        'correo': new_user.correo,
        'rol': new_user.rol,
    }
    return user_data, None


