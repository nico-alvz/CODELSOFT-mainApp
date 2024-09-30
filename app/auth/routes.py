from flask import request, jsonify
from flasgger import swag_from
from . import auth_bp
from ..utils import call_service_with_retries
from ..config import Config

@auth_bp.route('/auth/login', methods=['POST'])
@swag_from({
    'tags': ['Authentication'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Successful login',
            'schema': {
                'type': 'object',
                'properties': {
                    'jwtToken': {'type': 'string'}
                }
            }
        },
        400: {'description': 'Missing email or password'},
        500: {'description': 'Internal server error'}
    }
})
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    auth_url = f"{Config.EXTERNAL_SERVICES['auth']}/auth/login"

    try:
        response = call_service_with_retries(auth_url, "POST", payload={"email": email, "password": password})
        jwt_token = response.get("jwtToken")
        if not jwt_token:
            raise Exception("JWT token not provided by auth service")
        return jsonify({"jwtToken": jwt_token}), 200
    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500
