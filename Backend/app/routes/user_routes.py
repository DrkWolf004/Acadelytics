from flask import Blueprint, request, jsonify
from app.services.user_service import create_user, get_all_users,get_user_by_id, update_user, delete_user

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('', methods=['POST'])
def create_user_route():
    data = request.json
    user = create_user(data)
    return jsonify({'id': user.id, 'correo': user.correo}), 201


@user_bp.route('', methods=['GET'])
def get_users_route():
    users = get_all_users()
    if not users:
        return jsonify({'error': 'No se encontraron usuarios'}), 404
    
    users_list = [{
        'id': u.id,
        'nombre': u.nombre,
        'apellidos': u.apellidos,
        'correo': u.correo,
        'rol': u.rol
    } for u in users]
    return jsonify(users_list)


@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user_route(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({
        'id': user.id,
        'nombre': user.nombre,
        'apellidos': user.apellidos,
        'correo': user.correo,
        'rol': user.rol
    })


@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    data = request.json
    user = update_user(user_id, data)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'message': 'Usuario actualizado'})


@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    user = delete_user(user_id)
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    return jsonify({'message': 'Usuario eliminado'})
