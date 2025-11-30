from app.models.user_model import user
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
from datetime import datetime

def get_user_service(query):
    try:
        user_id = query.get('id')
        correo = query.get('correo')
        
        filters = []
        if user_id:
            filters.append(user.id == int(user_id))
        if correo:
            filters.append(user.correo == correo)
        
        if not filters:
            return None, "Debe proporcionar al menos id o correo"
        
        user_obj = user.query.filter(or_(*filters)).first()

        if not user_obj:
            return None, "Usuario no encontrado"

        user_data = {
            'id': user_obj.id,
            'nombre': user_obj.nombre,
            'apellidos': user_obj.apellidos,
            'correo': user_obj.correo,
            'rol': user_obj.rol,
            'created_at': user_obj.created_at,
            'updated_at': user_obj.updated_at
        }

        return user_data, None
    except Exception as error:
        print("Error obtener el usuario:", error)
        return None, "Error interno del servidor"

def get_users_service():
    try:
        users_list = user.query.all()
        if not users_list:
            return [], None

        users_data = []
        for user_obj in users_list:
            data = {
                'id': user_obj.id,
                'nombre': user_obj.nombre,
                'apellidos': user_obj.apellidos,
                'correo': user_obj.correo,
                'rol': user_obj.rol,
                'created_at': user_obj.created_at,
                'updated_at': user_obj.updated_at
            }
            users_data.append(data)

        return users_data, None
    except Exception as error:
        print("Error al obtener a los usuarios:", error)
        return None, "Error interno del servidor"

def update_user_service(query, body):
    try:
        user_id = query.get('id')
        correo = query.get('correo')

        filters = []
        if user_id:
            filters.append(user.id == int(user_id))
        if correo:
            filters.append(user.correo == correo)
        
        if not filters:
            return None, "Debe proporcionar al menos id o correo"

        user_obj = user.query.filter(or_(*filters)).first()

        if not user_obj:
            return None, "Usuario no encontrado"

        if body.get('correo') and body.get('correo') != user_obj.correo:
            existing_user = user.query.filter_by(correo=body.get('correo')).first()
            if existing_user:
                return None, "Ya existe un usuario con el mismo correo"

        if 'password' in body and body['password']:
            if not user_obj.check_password(body['password']):
                return None, "La contraseña no coincide"

        user_obj.nombre = body.get('nombre', user_obj.nombre)
        user_obj.apellidos = body.get('apellidos', user_obj.apellidos)
        user_obj.correo = body.get('correo', user_obj.correo)
        user_obj.rol = body.get('rol', user_obj.rol)

        new_password = body.get('newPassword')
        if new_password and new_password.strip() != '':
            user_obj.set_password(new_password)

        db.session.commit()

        user_updated = {
            'id': user_obj.id,
            'nombre': user_obj.nombre,
            'apellidos': user_obj.apellidos,
            'correo': user_obj.correo,
            'rol': user_obj.rol,
            'created_at': user_obj.created_at,
            'updated_at': user_obj.updated_at
        }

        return user_updated, None

    except Exception as error:
        print("Error al modificar un usuario:", error)
        return None, "Error interno del servidor"

def delete_user_service(query):
    try:
        user_id = query.get('id')
        correo = query.get('correo')

        filters = []
        if user_id:
            filters.append(user.id == int(user_id))
        if correo:
            filters.append(user.correo == correo)
        
        if not filters:
            return None, "Debe proporcionar al menos id o correo"

        user_obj = user.query.filter(or_(*filters)).first()

        if not user_obj:
            return None, "Usuario no encontrado"

        if user_obj.rol == 'Administrador':
            return None, "No se puede eliminar un usuario con rol de administrador"

        db.session.delete(user_obj)
        db.session.commit()

        data_user = {
            'id': user_obj.id,
            'nombre': user_obj.nombre,
            'apellidos': user_obj.apellidos,
            'correo': user_obj.correo,
            'rol': user_obj.rol,
            'created_at': user_obj.created_at,
            'updated_at': user_obj.updated_at
        }

        return data_user, None

    except Exception as error:
        print("Error al eliminar un usuario:", error)
        return None, "Error interno del servidor"
