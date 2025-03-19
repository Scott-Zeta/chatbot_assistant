from functools import wraps
from flask import request, jsonify
from marshmallow import Schema, fields, ValidationError

class MessageSchema(Schema):
    query = fields.Str(required=True, validate=lambda x: len(x.strip()) > 0)

def validate_request(schema):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                schema.load(request.json)
            except ValidationError as err:
                return jsonify({"error": err.messages}), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator