from flask import request, jsonify
from flasgger import swag_from
from . import students_bp
from ..utils import call_service_with_retries, token_required
from ..config import Config

@students_bp.route('/students', methods=['POST'])
@token_required
@swag_from({
    'tags': ['Students'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'studentId': {'type': 'string'},
                    'name': {'type': 'string'},
                    'lastName': {'type': 'string'},
                    'email': {'type': 'string'}
                },
                'required': ['studentId', 'name', 'lastName', 'email']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Student created successfully',
            'schema': {
                'type': 'object'
            }
        },
        400: {'description': 'Invalid or incomplete data'},
        500: {'description': 'Internal server error'}
    }
})
def create_student():
    student_data = request.get_json()
    token = request.headers.get("Authorization")

    search_url = f"{Config.EXTERNAL_SERVICES['search']}/api/students"

    headers = {"Authorization": token}

    try:
        response = call_service_with_retries(search_url, "POST", payload=student_data, headers=headers)
        return jsonify(response), 201
    except Exception as e:
        return jsonify({"error": f"Failed to create student: {str(e)}"}), 500

@students_bp.route('/students/search', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Students'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'studentId',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'ID of the student to search'
        },
        {
            'name': 'name',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Name of the student to search'
        }
    ],
    'responses': {
        200: {
            'description': 'Students retrieved successfully',
            'schema': {
                'type': 'object'
            }
        },
        400: {'description': 'Missing query parameters'},
        500: {'description': 'Internal server error'}
    }
})
def search_students():
    student_id = request.args.get("studentId")
    name = request.args.get("name")
    token = request.headers.get("Authorization")

    if not student_id and not name:
        return jsonify({"error": "Either 'studentId' or 'name' must be provided"}), 400

    search_url = f"{Config.EXTERNAL_SERVICES['search']}/api/students/search"
    params = {}
    if student_id:
        params['studentId'] = student_id
    if name:
        params['name'] = name

    headers = {"Authorization": token}

    try:
        response = call_service_with_retries(search_url, "GET", params=params, headers=headers)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f"Failed to search students: {str(e)}"}), 500
