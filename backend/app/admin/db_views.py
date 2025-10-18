# backend/app/admin/db_views.py

from app.admin.manager import admin_manager
from app.admin.views import BaseModelView
from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import current_user
from app.models import db
from sqlalchemy import inspect, text
import json
from collections import defaultdict

class DatabaseManagementView:
    """View for database management operations"""
    
    def __init__(self):
        self.name = "Database Management"
        self.category = "System"
        self.icon = "fa-database"
        self.endpoint = "db_management"
    
    def get_schema_info(self):
        """Get comprehensive database schema information"""
        inspector = inspect(db.engine)
        
        schema_info = {
            'tables': {},
            'relationships': defaultdict(list),
            'statistics': {
                'total_tables': 0,
                'total_columns': 0,
                'total_indexes': 0,
                'total_foreign_keys': 0
            }
        }
        
        tables = inspector.get_table_names()
        schema_info['statistics']['total_tables'] = len(tables)
        
        for table_name in tables:
            # Columns
            columns = inspector.get_columns(table_name)
            schema_info['statistics']['total_columns'] += len(columns)
            
            # Primary keys
            pk_info = inspector.get_pk_constraint(table_name)
            
            # Foreign keys
            fks = inspector.get_foreign_keys(table_name)
            schema_info['statistics']['total_foreign_keys'] += len(fks)
            
            # Indexes
            indexes = inspector.get_indexes(table_name)
            schema_info['statistics']['total_indexes'] += len(indexes)
            
            # Record count
            try:
                count = db.session.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
            except:
                count = 0
            
            schema_info['tables'][table_name] = {
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
                'primary_keys': pk_info.get('constrained_columns', []),
                'foreign_keys': [
                    {
                        'columns': fk['constrained_columns'],
                        'references': f"{fk['referred_table']}.{fk['referred_columns']}",
                        'name': fk.get('name', '')
                    } for fk in fks
                ],
                'indexes': [
                    {
                        'name': idx['name'],
                        'columns': idx['column_names'],
                        'unique': idx['unique']
                    } for idx in indexes
                ],
                'record_count': count,
                'is_lookup_table': any(x in table_name.lower() for x in ['status', 'type', 'category'])
            }
            
            # Build relationship map
            for fk in fks:
                schema_info['relationships'][fk['referred_table']].append({
                    'from_table': table_name,
                    'from_columns': fk['constrained_columns'],
                    'to_columns': fk['referred_columns']
                })
        
        return schema_info
    
    def get_database_stats(self):
        """Get database performance and size statistics"""
        stats = {
            'basic': {},
            'table_sizes': [],
            'column_types': defaultdict(int)
        }
        
        try:
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            # Basic stats
            stats['basic']['total_tables'] = len(tables)
            stats['basic']['total_columns'] = 0
            stats['basic']['total_records'] = 0
            
            # Table sizes and column types
            for table_name in tables:
                columns = inspector.get_columns(table_name)
                stats['basic']['total_columns'] += len(columns)
                
                # Column types
                for col in columns:
                    col_type = str(col['type'])
                    stats['column_types'][col_type] += 1
                
                # Record count
                try:
                    count = db.session.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
                    stats['basic']['total_records'] += count
                    stats['table_sizes'].append({
                        'name': table_name,
                        'columns': len(columns),
                        'records': count
                    })
                except:
                    pass
            
            # Sort table sizes by record count
            stats['table_sizes'].sort(key=lambda x: x['records'], reverse=True)
            
        except Exception as e:
            stats['error'] = str(e)
        
        return stats

def init_db_management_views():
    """Initialize database management views"""
    try:
        # Add database management to admin menu
        admin_manager.add_category('System', 'fa-cogs')
        
        # Create and register the database management view
        db_view = DatabaseManagementView()
        
        # Add to menu (we'll handle this differently since it's not a ModelView)
        menu_item = {
            'name': db_view.name,
            'model_name': db_view.endpoint,
            'view': db_view,
            'icon': db_view.icon,
            'is_special_view': True
        }
        
        if db_view.category not in admin_manager._menu:
            admin_manager._menu[db_view.category] = []
        admin_manager._menu[db_view.category].append(menu_item)
        
        print(f"✅ Database management view registered")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database management views: {e}")
        return False