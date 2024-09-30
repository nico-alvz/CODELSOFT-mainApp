from flask import request, jsonify
from flasgger import swag_from
from . import grades_bp
from ..utils import call_service_with_retries, token_required
from ..config import Config

@grades_bp.route('/grades', methods=['POST'])
@token_required
@swag_from({
    'tags': ['Grades'],
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
                    'subjectName': {'type': 'string'},
                    'gradeName': {'type': 'string'},
                    'grade': {'type': 'number'},
                    'comment': {'type': 'string'}
                },
                'required': ['studentId', 'subjectName', 'gradeName', 'grade']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Grade created successfully',
            'schema': {
                'type': 'object'
            }
        },
        400: {'description': 'Invalid or incomplete data'},
        500: {'description': 'Internal server error'}
    }
})
def create_grade():
    grade_data = request.get_json()
    token = request.headers.get("Authorization")

    grades_url = f"{Config.EXTERNAL_SERVICES['grades']}/api/grades"

    headers = {"Authorization": token}

    try:
        response = call_service_with_retries(grades_url, "POST", payload=grade_data, headers=headers)
        return jsonify(response), 201
    except Exception as e:
        return jsonify({"error": f"Failed to create grade: {str(e)}"}), 500

@grades_bp.route('/grades/<grade_id>', methods=['GET'])
@token_required
@swag_from({
    'tags': ['Grades'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'grade_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the grade'
        }
    ],
    'responses': {
        200: {
            'description': 'Grade retrieved successfully',
            'schema': {
                'type': 'object'
            }
        },
        404: {'description': 'Grade not found'},
        500: {'description': 'Internal server error'}
    }
})
def get_grade(grade_id):
    token = request.headers.get("Authorization")
    grades_url = f"{Config.EXTERNAL_SERVICES['grades']}/api/grades/{grade_id}"
    headers = {"Authorization": token}

    try:
        response = call_service_with_retries(grades_url, "GET", headers=headers)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve grade: {str(e)}"}), 500

@grades_bp.route('/grades/<grade_id>', methods=['PUT'])
@token_required
@swag_from({
    'tags': ['Grades'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'grade_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the grade to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'subjectName': {'type': 'string'},
                    'gradeName': {'type': 'string'},
                    'grade': {'type': 'number'},
                    'comment': {'type': 'string'}
                },
                'required': ['subjectName', 'gradeName', 'grade']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Grade updated successfully',
            'schema': {
                'type': 'object'
            }
        },
        400: {'description': 'Invalid or incomplete data'},
        404: {'description': 'Grade not found'},
        500: {'description': 'Internal server error'}
    }
})
def update_grade(grade_id):
    update_data = request.get_json()
    token = request.headers.get("Authorization")

    grades_url = f"{Config.EXTERNAL_SERVICES['grades']}/api/grades/{grade_id}"

    headers = {"Authorization": token}

    try:
        response = call_service_with_retries(grades_url, "PUT", payload=update_data, headers=headers)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": f"Failed to update grade: {str(e)}"}), 500
