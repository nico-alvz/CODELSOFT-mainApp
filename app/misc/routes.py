from flask import jsonify
from flasgger import swag_from
from . import misc_bp

@misc_bp.route('/onRender', methods=['GET'])
@swag_from({
    'tags': ['Miscellaneous'],
    'responses': {
        200: {
            'description': 'OnRender endpoint',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        }
    }
})
def on_render():
    return jsonify({"message": "OnRender endpoint is working"}), 200