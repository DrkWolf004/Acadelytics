from flask import jsonify

def handle_success(status_code, message, data=None):
    response = {
        'status': 'Success',
        'message': message,
        'data': data or {}
    }
    return jsonify(response), status_code

def handle_error_client(status_code, message, details=None):
    response = {
        'status': 'Client error',
        'message': message,
        'details': details or {}
    }
    return jsonify(response), status_code

def handle_error_server(message, status_code=500):
    response = {
        'status': 'Server error',
        'message': message
    }
    return jsonify(response), status_code
