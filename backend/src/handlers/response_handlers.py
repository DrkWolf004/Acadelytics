from flask import jsonify, make_response


def handle_success(status_code, message, data=None):
    if data is None:
        data = {}

    payload = {
        "status": "Success",
        "message": message,
        "data": data,
    }
    return make_response(jsonify(payload), status_code)


def handle_error_client(status_code, message, details=None):
    if details is None:
        details = {}

    payload = {
        "status": "Client error",
        "message": message,
        "details": details,
    }
    return make_response(jsonify(payload), status_code)


def handle_error_server(status_code, message):
    payload = {
        "status": "Server error",
        "message": message,
    }
    return make_response(jsonify(payload), status_code)
