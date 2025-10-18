from marshmallow import Schema, fields, validate, EXCLUDE

class UserRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    role = fields.String(required=True)
    clinic_name = fields.String(required=False)
    
    # Allow camelCase input but convert to snake_case
    firstName = fields.String(required=True, data_key='first_name', load_only=True)
    lastName = fields.String(required=True, data_key='last_name', load_only=True)
    clinicName = fields.String(required=False, data_key='clinic_name', load_only=True)
    
    # This tells Marshmallow to expect camelCase but output snake_case
    class Meta:
        unknown = EXCLUDE

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class UserOutSchema(Schema):
    id = fields.String()
    email = fields.Email()
    role = fields.String()
    clinic_name = fields.String()
    stripe_customer_id = fields.String()
