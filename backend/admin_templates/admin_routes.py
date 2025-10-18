
# Admin Interface Routes
from flask import Blueprint, render_template, jsonify, request
from app import db
from sqlalchemy import text

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_dashboard():
    """Main admin dashboard"""
    return render_template('admin.html')

@admin_bp.route('/api/data/<table_name>')
def get_table_data(table_name):
    """API endpoint to get sample data from any table"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Basic security check - only allow existing tables
        inspector = db.inspect(db.engine)
        if table_name not in inspector.get_table_names():
            return jsonify({'error': 'Table not found'}), 404
        
        # Get sample data
        result = db.session.execute(
            text(f"SELECT * FROM {table_name} LIMIT :limit"),
            {'limit': limit}
        )
        
        columns = result.keys()
        data = [dict(zip(columns, row)) for row in result]
        
        return jsonify(data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/api/schema')
def get_schema():
    """API endpoint to get complete database schema"""
    try:
        inspector = db.inspect(db.engine)
        schema_info = {}
        
        for table_name in inspector.get_table_names():
            # Get table info
            columns = inspector.get_columns(table_name)
            primary_keys = inspector.get_pk_constraint(table_name)
            foreign_keys = inspector.get_foreign_keys(table_name)
            indexes = inspector.get_indexes(table_name)
            
            # Get row count
            count = db.session.execute(
                text(f"SELECT COUNT(*) FROM {table_name}")
            ).scalar()
            
            schema_info[table_name] = {
                'columns': [
                    {
                        'name': col['name'],
                        'type': str(col['type']),
                        'nullable': col['nullable'],
                        'default': str(col.get('default', '')),
                        'primary_key': col.get('primary_key', False),
                        'autoincrement': col.get('autoincrement', False)
                    } for col in columns
                ],
                'primary_keys': primary_keys.get('constrained_columns', []),
                'foreign_keys': [
                    {
                        'columns': fk['constrained_columns'],
                        'references': f"{fk['referred_table']}.{fk['referred_columns']}"
                    } for fk in foreign_keys
                ],
                'indexes': [
                    {
                        'name': idx['name'],
                        'columns': idx['column_names'],
                        'unique': idx['unique']
                    } for idx in indexes
                ],
                'row_count': count
            }
        
        return jsonify(schema_info)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Register this blueprint in your main app
# from admin_routes import admin_bp
# app.register_blueprint(admin_bp)
