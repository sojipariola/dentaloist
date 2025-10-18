from marshmallow import Schema, fields

class PatientSchema(Schema):
    id = fields.String(dump_only=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    date_of_birth = fields.Date(load_default=None)
    notes = fields.String(load_default=None)
