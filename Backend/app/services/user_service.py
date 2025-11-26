from app.models.User import User
from app import db

def create_user(data):
    user = User(
        nombre=data['nombre'],
        apellidos=data['apellidos'],
        correo=data['correo'],
        rol=data['rol']
    )
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_id(user_id):
    return User.query.get(user_id)

def update_user(user_id, data):
    user = User.query.get(user_id)
    if user:
        user.nombre = data.get('nombre', user.nombre)
        user.apellidos = data.get('apellidos', user.apellidos)
        user.correo = data.get('correo', user.correo)
        user.rol = data.get('rol', user.rol)
        if 'password' in data:
            user.set_password(data['password'])
        db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
    return user

def get_all_users():
    return User.query.all()