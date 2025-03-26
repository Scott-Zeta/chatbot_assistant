from flask import Blueprint, jsonify, request
from app.services.contact_service import ContactService
from marshmallow import Schema, fields, ValidationError

contact_bp = Blueprint('contact', __name__)
contact_service = ContactService()

class ContactSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(allow_none=True)
    phone = fields.Str(required=True)
    online = fields.Str(allow_none=True)
    contact_preference = fields.Str(required=True)
    additional_text = fields.Str(allow_none=True)

@contact_bp.route('/contact', methods=['POST'])
def handle_contact_form():
    try:
        # Validate incoming data
        schema = ContactSchema()
        data = request.json.get('data')
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate the contact data
        validated_data = schema.load(data)
        
        # Save the contact information
        if contact_service.save_contact(validated_data):
            return jsonify({
                'response': {
                    'answer': f"Thank you {validated_data['name']}! We have received your contact information and will get in touch with you soon via your preferred contact method ({validated_data['contact_preference']})."
                }
            }), 200
        else:
            return jsonify({'error': 'Failed to save contact information'}), 500
            
    except ValidationError as err:
        return jsonify({'error': err.messages}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500