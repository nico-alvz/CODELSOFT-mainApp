from flask import request, jsonify
from flasgger import swag_from
from . import restrictions_bp
from ..utils import call_service_with_retries, token_required
from ..config import Config

@restrictions_bp.route('/students/restrictions', methods=['POST'])
@token_required
@swag_from({
    'tags': ['Restrictions'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'studentIds': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    },
                    'restriction': {
                        'type': 'object',
                        'properties': {
                            'restrictionId': {'type': 'string'},
                            'reason': {'type': 'string'},
                            'creationDate': {'type': 'string', 'format': 'date'}
                        },
                        'required': ['restrictionId', 'reason', 'creationDate']
                    }
                },
                'required': ['studentIds', 'restriction']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Restrictions created successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'details': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'studentId': {'type': 'string'},
                                'restriction': {'type': 'object'}
                            }
                        }
                    }
                }
            }
        },
        400: {'description': 'Invalid or incomplete data'},
        500: {'description': 'Internal server error'}
    }
})
def create_restrictions():
    data = request.get_json()
    student_ids = data.get("studentIds")
    restriction_data = data.get("restriction")
    token = request.headers.get("Authorization")

    if not student_ids or not restriction_data:
        return jsonify({"error": "studentIds and restriction are required"}), 400

    restrictions_url_base = f"{Config.EXTERNAL_SERVICES['restrictions']}/api/restrictions"

    headers = {"Authorization": token}

    created_restrictions = []

    for student_id in student_ids:
        payload = {
            "studentId": student_id,
            "restrictionId": restriction_data.get("restrictionId"),
            "reason": restriction_data.get("reason"),
            "creationDate": restriction_data.get("creationDate")
        }
        try:
            response = call_service_with_retries(f"{restrictions_url_base}", "POST", payload=payload, headers=headers)
            created_restrictions.append({"studentId": student_id, "restriction": response})
        except Exception as e:
            return jsonify({"error": f"Failed to create restriction for student {student_id}: {str(e)}"}), 500

    return jsonify({"message": "Restrictions created successfully", "details": created_restrictions}), 201

@restrictions_bp.route('/students/restrictions', methods=['DELETE'])
@token_required
@swag_from({
    'tags': ['Restrictions'],
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'restrictionId': {'type': 'string'}
                },
                'required': ['restrictionId']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Restrictions removed successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'updatedStudents': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'studentId': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        },
        400: {'description': 'Invalid or incomplete data'},
        404: {'description': 'No matching restrictions found'},
        500: {'description': 'Internal server error'}
    }
})
def remove_restrictions():
    data = request.get_json()
    restriction_id = data.get("restrictionId")
    token = request.headers.get("Authorization")

    if not restriction_id:
        return jsonify({"error": "restrictionId is required"}), 400

    search_url = f"{Config.EXTERNAL_SERVICES['restrictions']}/api/restrictions/{restriction_id}/students"
    headers = {"Authorization": token}

    try:
        students = call_service_with_retries(search_url, "GET", headers=headers)
    except Exception as e:
        return jsonify({"error": f"Failed to search students with restriction: {str(e)}"}), 500

    if not students:
        return jsonify({"error": "No matching restrictions found"}), 404

    restrictions_url_base = f"{Config.EXTERNAL_SERVICES['restrictions']}/api/restrictions"

    updated_students = []

    for student in students:
        student_id = student.get("studentId")
        if not student_id:
            continue
        delete_url = f"{restrictions_url_base}/{restriction_id}"
        params = {"studentId": student_id}
        try:
            call_service_with_retries(delete_url, "DELETE", params=params, headers=headers)
            updated_students.append({"studentId": student_id})
        except Exception as e:
            return jsonify({"error": f"Failed to remove restriction for student {student_id}: {str(e)}"}), 500

    return jsonify({"message": "Restrictions removed successfully", "updatedStudents": updated_students}), 200
