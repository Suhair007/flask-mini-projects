from flask import jsonify

def success_response(data=None, message="Success", status_code=200):
    """Standardized success response"""
    response = {
        'status': 'success',
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def error_response(message, status_code=400, errors=None):
    """Standardized error response"""
    response = {
        'status': 'error',
        'message': message
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), status_code 