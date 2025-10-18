#  scripts/comprehensive_admin_analyzer.py

from ..app import create_app, db
from sqlalchemy import inspect, text
import json
from flask import url_for
from collections import defaultdict
import os

def analyze_complete_system():
    app = create_app()
    
    with app.app_context():
        print("=" * 100)
        print("🔍 COMPREHENSIVE SYSTEM ANALYSIS FOR LOCAL ADMIN INTERFACE")
        print("=" * 100)
        
        # Analyze database schema
        schema_info = analyze_database_schema(app)
        
        # Analyze Flask routes
        routes_info = analyze_flask_routes(app)
        
        # Generate complete admin interface
        generate_complete_admin_interface(schema_info, routes_info)
        
        return schema_info, routes_info

def analyze_database_schema(app):
    """Analyze complete database schema"""
    inspector = inspect(db.engine)
    
    print("\n🗃️  DATABASE SCHEMA ANALYSIS")
    print("=" * 60)
    
    tables = inspector.get_table_names()
    schema_info = {
        'tables': {},
        'statistics': {
            'total_tables': len(tables),
            'table_categories': defaultdict(int)
        }
    }
    
    for table_name in sorted(tables):
        category = categorize_table(table_name)
        schema_info['statistics']['table_categories'][category] += 1
        
        print(f"\n📊 TABLE: {table_name} [{category}]")
        print("-" * 50)
        
        # Columns
        columns = inspector.get_columns(table_name)
        schema_info['tables'][table_name] = {
            'category': category,
            'columns': [],
            'primary_keys': [],
            'foreign_keys': [],
            'indexes': [],
            'row_count': 0
        }
        
        # Column details
        print("   📋 Columns:")
        for col in columns:
            col_info = {
                'name': col['name'],
                'type': str(col['type']),
                'nullable': col['nullable'],
                'default': str(col.get('default', '')),
                'primary_key': col.get('primary_key', False),
                'autoincrement': col.get('autoincrement', False)
            }
            schema_info['tables'][table_name]['columns'].append(col_info)
            
            # Visual indicators
            indicators = []
            if col.get('primary_key'): indicators.append("🔑")
            if col.get('autoincrement'): indicators.append("🔄")
            if not col['nullable']: indicators.append("❌")
            if col.get('default'): indicators.append("⚡")
            
            indicator_str = " " + "".join(indicators) if indicators else ""
            print(f"      • {col['name']}: {col['type']}{indicator_str}")
        
        # Primary keys
        pks = inspector.get_pk_constraint(table_name)
        if pks['constrained_columns']:
            schema_info['tables'][table_name]['primary_keys'] = pks['constrained_columns']
            print(f"   🔑 Primary Keys: {', '.join(pks['constrained_columns'])}")
        
        # Foreign keys
        fks = inspector.get_foreign_keys(table_name)
        if fks:
            print("   🔗 Foreign Keys:")
            for fk in fks:
                fk_info = {
                    'columns': fk['constrained_columns'],
                    'references': f"{fk['referred_table']}.{fk['referred_columns']}",
                    'name': fk.get('name', '')
                }
                schema_info['tables'][table_name]['foreign_keys'].append(fk_info)
                print(f"      • {fk['constrained_columns']} → {fk['referred_table']}.{fk['referred_columns']}")
        
        # Indexes
        indexes = inspector.get_indexes(table_name)
        if indexes:
            print("   📈 Indexes:")
            for idx in indexes:
                idx_info = {
                    'name': idx['name'],
                    'columns': idx['column_names'],
                    'unique': idx['unique']
                }
                schema_info['tables'][table_name]['indexes'].append(idx_info)
                unique_indicator = " 🎯" if idx['unique'] else ""
                print(f"      • {idx['name']}: {idx['column_names']}{unique_indicator}")
        
        # Row count
        try:
            count = db.session.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
            schema_info['tables'][table_name]['row_count'] = count
            print(f"   📊 Row Count: {count}")
        except Exception as e:
            print(f"   📊 Row Count: Error - {e}")
    
    return schema_info

def analyze_flask_routes(app):
    """Analyze all Flask routes in the application"""
    print("\n\n🌐 FLASK ROUTES ANALYSIS")
    print("=" * 60)
    
    routes_info = {
        'routes': [],
        'endpoints_by_blueprint': defaultdict(list),
        'methods_by_route': defaultdict(list)
    }
    
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint != 'static':  # Skip static files
                route_info = {
                    'endpoint': rule.endpoint,
                    'methods': sorted(list(rule.methods - {'HEAD', 'OPTIONS'})),
                    'path': rule.rule,
                    'blueprint': get_blueprint_from_endpoint(rule.endpoint)
                }
                routes_info['routes'].append(route_info)
                routes_info['endpoints_by_blueprint'][route_info['blueprint']].append(route_info)
                
                for method in route_info['methods']:
                    routes_info['methods_by_route'][method].append(route_info['path'])
        
        # Print routes organized by blueprint
        for blueprint, routes in sorted(routes_info['endpoints_by_blueprint'].items()):
            print(f"\n📦 {blueprint or 'MAIN APP'}:")
            for route in sorted(routes, key=lambda x: x['path']):
                methods = ', '.join(route['methods'])
                print(f"   {route['path']} [{methods}] → {route['endpoint']}")
    
    return routes_info

def get_blueprint_from_endpoint(endpoint):
    """Extract blueprint name from endpoint"""
    if '.' in endpoint:
        return endpoint.split('.')[0]
    return 'main'

def categorize_table(table_name):
    """Categorize tables for organization"""
    categories = {
        'user': 'User Management',
        'role': 'User Management', 
        'permission': 'User Management',
        'auth': 'User Management',
        'patient': 'Clinical Data',
        'appointment': 'Appointments',
        'treatment': 'Clinical Data',
        'clinical': 'Clinical Data',
        'medical': 'Clinical Data',
        'invoice': 'Financial',
        'payment': 'Financial',
        'claim': 'Financial',
        'billing': 'Financial',
        'inventory': 'Inventory',
        'product': 'Inventory',
        'supplier': 'Inventory',
        'order': 'Inventory',
        'analytics': 'Analytics',
        'report': 'Analytics',
        'dashboard': 'Analytics',
        'kpi': 'Analytics',
        'audit': 'System',
        'log': 'System',
        'settings': 'System'
    }
    
    for key, category in categories.items():
        if key in table_name.lower():
            return category
    
    if any(x in table_name.lower() for x in ['status', 'type', 'category']):
        return 'Lookup Tables'
    
    return 'System'

def generate_complete_admin_interface(schema_info, routes_info):
    """Generate a complete local admin interface mimic"""
    
    print("\n" + "=" * 100)
    print("🚀 COMPLETE LOCAL ADMIN INTERFACE SETUP")
    print("=" * 100)
    
    generate_admin_html_template(schema_info, routes_info)
    generate_admin_css()
    generate_admin_javascript(schema_info, routes_info)
    generate_admin_routes(routes_info)
    generate_admin_configuration(schema_info)

def generate_admin_html_template(schema_info, routes_info):
    """Generate HTML template for the admin interface"""
    
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dentaloist Local Admin</title>
    <link rel="stylesheet" href="/admin-static/css/admin.css">
</head>
<body>
    <div class="admin-container">
        <!-- Sidebar -->
        <div class="sidebar">
            <div class="sidebar-header">
                <h2>🦷 Dentaloist Admin</h2>
                <div class="system-stats">
                    <div class="stat">
                        <span class="stat-number">{schema_info['statistics']['total_tables']}</span>
                        <span class="stat-label">Tables</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">{len(routes_info['routes'])}</span>
                        <span class="stat-label">Routes</span>
                    </div>
                </div>
            </div>
            
            <nav class="sidebar-nav">
"""
    
    # Add navigation sections
    categories = defaultdict(list)
    for table_name, table_info in schema_info['tables'].items():
        categories[table_info['category']].append(table_name)
    
    for category in sorted(categories.keys()):
        html_template += f"""
                <div class="nav-section">
                    <h3>{category}</h3>
                    <ul>
"""
        for table_name in sorted(categories[category]):
            row_count = schema_info['tables'][table_name]['row_count']
            html_template += f"""
                        <li>
                            <a href="#table-{table_name}" class="nav-link" data-table="{table_name}">
                                📊 {table_name}
                                <span class="row-count">{row_count}</span>
                            </a>
                        </li>
"""
        html_template += """
                    </ul>
                </div>
"""
    
    html_template += """
            </nav>
        </div>
        
        <!-- Main Content -->
        <div class="main-content">
            <header class="content-header">
                <h1 id="content-title">System Overview</h1>
                <div class="header-actions">
                    <button id="refresh-btn" class="btn btn-primary">🔄 Refresh</button>
                    <button id="export-btn" class="btn btn-secondary">📤 Export Data</button>
                </div>
            </header>
            
            <div class="content-area">
                <!-- System Overview -->
                <div id="system-overview" class="content-section active">
                    <div class="overview-cards">
                        <div class="card">
                            <h3>📊 Database Statistics</h3>
                            <div class="card-content">
"""
    
    # Database statistics
    for category, count in sorted(schema_info['statistics']['table_categories'].items()):
        html_template += f"""
                                <div class="stat-item">
                                    <span class="stat-category">{category}:</span>
                                    <span class="stat-value">{count} tables</span>
                                </div>
"""
    
    html_template += """
                            </div>
                        </div>
                        
                        <div class="card">
                            <h3>🌐 Application Routes</h3>
                            <div class="card-content">
"""
    
    # Route statistics
    for blueprint, routes in sorted(routes_info['endpoints_by_blueprint'].items()):
        html_template += f"""
                                <div class="stat-item">
                                    <span class="stat-category">{blueprint or 'Main'}:</span>
                                    <span class="stat-value">{len(routes)} routes</span>
                                </div>
"""
    
    html_template += """
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Table Details will be loaded here dynamically -->
                <div id="table-details" class="content-section"></div>
            </div>
        </div>
    </div>
    
    <script src="/admin-static/js/admin.js"></script>
</body>
</html>
"""
    
    # Save HTML template
    os.makedirs('admin_templates', exist_ok=True)
    with open('admin_templates/admin.html', 'w') as f:
        f.write(html_template)
    
    print("✅ Generated admin.html template")

def generate_admin_css():
    """Generate CSS for the admin interface"""
    
    css = """
/* Admin Interface Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #f5f5f5;
    color: #333;
}

.admin-container {
    display: flex;
    min-height: 100vh;
}

/* Sidebar */
.sidebar {
    width: 300px;
    background: #2c3e50;
    color: white;
    overflow-y: auto;
}

.sidebar-header {
    padding: 20px;
    border-bottom: 1px solid #34495e;
}

.sidebar-header h2 {
    margin-bottom: 15px;
    font-size: 1.5em;
}

.system-stats {
    display: flex;
    gap: 15px;
}

.stat {
    text-align: center;
}

.stat-number {
    display: block;
    font-size: 1.5em;
    font-weight: bold;
}

.stat-label {
    font-size: 0.8em;
    opacity: 0.8;
}

.sidebar-nav {
    padding: 15px 0;
}

.nav-section {
    margin-bottom: 20px;
}

.nav-section h3 {
    padding: 10px 20px;
    font-size: 0.9em;
    text-transform: uppercase;
    opacity: 0.7;
    letter-spacing: 1px;
}

.nav-section ul {
    list-style: none;
}

.nav-section li {
    border-left: 3px solid transparent;
    transition: all 0.3s;
}

.nav-section li:hover {
    border-left-color: #3498db;
    background: rgba(255,255,255,0.1);
}

.nav-link {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 20px;
    color: white;
    text-decoration: none;
    transition: all 0.3s;
}

.nav-link:hover {
    background: rgba(255,255,255,0.05);
}

.row-count {
    background: #34495e;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.8em;
}

/* Main Content */
.main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.content-header {
    background: white;
    padding: 20px 30px;
    border-bottom: 1px solid #e0e0e0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.content-header h1 {
    font-size: 1.8em;
    color: #2c3e50;
}

.header-actions {
    display: flex;
    gap: 10px;
}

.btn {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.3s;
}

.btn-primary {
    background: #3498db;
    color: white;
}

.btn-primary:hover {
    background: #2980b9;
}

.btn-secondary {
    background: #95a5a6;
    color: white;
}

.btn-secondary:hover {
    background: #7f8c8d;
}

.content-area {
    flex: 1;
    padding: 30px;
    overflow-y: auto;
}

.content-section {
    display: none;
}

.content-section.active {
    display: block;
}

/* Overview Cards */
.overview-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.card {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    overflow: hidden;
}

.card h3 {
    padding: 20px;
    background: #f8f9fa;
    border-bottom: 1px solid #e9ecef;
    margin: 0;
}

.card-content {
    padding: 20px;
}

.stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid #f8f9fa;
}

.stat-item:last-child {
    border-bottom: none;
}

.stat-category {
    font-weight: 500;
}

.stat-value {
    color: #6c757d;
    font-weight: bold;
}

/* Table Styles */
.table-container {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    overflow: hidden;
}

.table-header {
    padding: 20px;
    background: #f8f9fa;
    border-bottom: 1px solid #e9ecef;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.table-content {
    overflow-x: auto;
}

.data-table {
    width: 100%;
    border-collapse: collapse;
}

.data-table th,
.data-table td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #e9ecef;
}

.data-table th {
    background: #f8f9fa;
    font-weight: 600;
    color: #495057;
}

.data-table tr:hover {
    background: #f8f9fa;
}

.column-type {
    font-family: monospace;
    font-size: 0.8em;
    color: #6c757d;
}

.column-props {
    display: flex;
    gap: 5px;
    flex-wrap: wrap;
}

.prop-tag {
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 0.7em;
    font-weight: bold;
}

.prop-pk { background: #ffeaa7; color: #2d3436; }
.prop-fk { background: #a29bfe; color: white; }
.prop-unique { background: #55efc4; color: #2d3436; }
.prop-nullable { background: #dfe6e9; color: #2d3436; }

/* Responsive */
@media (max-width: 768px) {
    .admin-container {
        flex-direction: column;
    }
    
    .sidebar {
        width: 100%;
        height: auto;
    }
    
    .overview-cards {
        grid-template-columns: 1fr;
    }
}
"""
    
    os.makedirs('admin_templates/static/css', exist_ok=True)
    with open('admin_templates/static/css/admin.css', 'w') as f:
        f.write(css)
    
    print("✅ Generated admin.css")

def generate_admin_javascript(schema_info, routes_info):
    """Generate JavaScript for dynamic admin functionality"""
    
    # Convert schema info to JSON for JavaScript
    schema_json = json.dumps(schema_info, indent=2)
    
    js = f"""
// Admin Interface JavaScript
const schemaInfo = {schema_json};

document.addEventListener('DOMContentLoaded', function() {{
    // Navigation
    const navLinks = document.querySelectorAll('.nav-link');
    const contentTitle = document.getElementById('content-title');
    const tableDetails = document.getElementById('table-details');
    const systemOverview = document.getElementById('system-overview');
    
    navLinks.forEach(link => {{
        link.addEventListener('click', function(e) {{
            e.preventDefault();
            const tableName = this.getAttribute('data-table');
            showTableDetails(tableName);
        }});
    }});
    
    // Refresh button
    document.getElementById('refresh-btn').addEventListener('click', function() {{
        location.reload();
    }});
    
    // Export button
    document.getElementById('export-btn').addEventListener('click', function() {{
        exportData();
    }});
    
    function showTableDetails(tableName) {{
        const tableInfo = schemaInfo.tables[tableName];
        if (!tableInfo) return;
        
        // Update UI
        contentTitle.textContent = `📊 ${{tableName}}`;
        systemOverview.classList.remove('active');
        tableDetails.classList.add('active');
        tableDetails.innerHTML = generateTableHTML(tableName, tableInfo);
        
        // Load sample data
        loadSampleData(tableName);
    }}
    
    function generateTableHTML(tableName, tableInfo) {{
        return `
            <div class="table-container">
                <div class="table-header">
                    <h3>Table Structure: ${{tableName}}</h3>
                    <div class="table-stats">
                        <span>${{tableInfo.columns.length}} columns • ${{tableInfo.row_count}} rows</span>
                    </div>
                </div>
                <div class="table-content">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Column Name</th>
                                <th>Data Type</th>
                                <th>Properties</th>
                                <th>Default</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${{tableInfo.columns.map(column => `
                                <tr>
                                    <td><strong>${{column.name}}</strong></td>
                                    <td><span class="column-type">${{column.type}}</span></td>
                                    <td>
                                        <div class="column-props">
                                            ${{column.primary_key ? '<span class="prop-tag prop-pk">PK</span>' : ''}}
                                            ${{column.autoincrement ? '<span class="prop-tag prop-pk">AI</span>' : ''}}
                                            ${{column.nullable ? '<span class="prop-tag prop-nullable">NULL</span>' : '<span class="prop-tag">NOT NULL</span>'}}
                                            ${{tableInfo.foreign_keys.some(fk => fk.columns.includes(column.name)) ? '<span class="prop-tag prop-fk">FK</span>' : ''}}
                                            ${{tableInfo.indexes.some(idx => idx.unique && idx.columns.includes(column.name)) ? '<span class="prop-tag prop-unique">UNIQUE</span>' : ''}}
                                        </div>
                                    </td>
                                    <td>${{column.default || '-'}}</td>
                                </tr>
                            `).join('')}}
                        </tbody>
                    </table>
                </div>
            </div>
            
            <div style="margin-top: 20px;">
                <h4>Sample Data</h4>
                <div id="sample-data-${{tableName}}">
                    <p>Loading sample data...</p>
                </div>
            </div>
        `;
    }}
    
    async function loadSampleData(tableName) {{
        try {{
            const response = await fetch(`/admin-api/data/${{tableName}}?limit=10`);
            const data = await response.json();
            displaySampleData(tableName, data);
        }} catch (error) {{
            document.getElementById(`sample-data-${{tableName}}`).innerHTML = 
                '<p>Error loading sample data</p>';
        }}
    }}
    
    function displaySampleData(tableName, data) {{
        const container = document.getElementById(`sample-data-${{tableName}}`);
        if (!data || data.length === 0) {{
            container.innerHTML = '<p>No data found</p>';
            return;
        }}
        
        const headers = Object.keys(data[0]);
        const html = `
            <div class="table-container">
                <div class="table-content">
                    <table class="data-table">
                        <thead>
                            <tr>
                                ${{headers.map(header => `<th>${{header}}</th>`).join('')}}
                            </tr>
                        </thead>
                        <tbody>
                            ${{data.map(row => `
                                <tr>
                                    ${{headers.map(header => `<td>${{formatCellValue(row[header])}}</td>`).join('')}}
                                </tr>
                            `).join('')}}
                        </tbody>
                    </table>
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }}
    
    function formatCellValue(value) {{
        if (value === null || value === undefined) return '<em>null</em>';
        if (typeof value === 'boolean') return value ? '✅' : '❌';
        if (typeof value === 'object') return JSON.stringify(value).substring(0, 50) + '...';
        return String(value);
    }}
    
    function exportData() {{
        // Simple export functionality
        const dataStr = JSON.stringify(schemaInfo, null, 2);
        const dataBlob = new Blob([dataStr], {{type: 'application/json'}});
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'dentaloist-schema-export.json';
        link.click();
        URL.revokeObjectURL(url);
    }}
}});
"""
    
    os.makedirs('admin_templates/static/js', exist_ok=True)
    with open('admin_templates/static/js/admin.js', 'w') as f:
        f.write(js)
    
    print("✅ Generated admin.js")

def generate_admin_routes(routes_info):
    """Generate Flask routes for the admin interface"""
    
    routes_code = """
# Admin Interface Routes
from flask import Blueprint, render_template, jsonify, request
from app import db
from sqlalchemy import text

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
def admin_dashboard():
    \"\"\"Main admin dashboard\"\"\"
    return render_template('admin.html')

@admin_bp.route('/api/data/<table_name>')
def get_table_data(table_name):
    \"\"\"API endpoint to get sample data from any table\"\"\"
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
    \"\"\"API endpoint to get complete database schema\"\"\"
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
"""
    
    with open('admin_templates/admin_routes.py', 'w') as f:
        f.write(routes_code)
    
    print("✅ Generated admin_routes.py")

def generate_admin_configuration(schema_info):
    """Generate configuration and setup instructions"""
    
    config = f"""
# DENTALOIST LOCAL ADMIN INTERFACE - SETUP INSTRUCTIONS
# =====================================================

# QUICK SETUP:
1. Copy the generated files to your Flask app:
   - admin_templates/ → your templates directory
   - admin_routes.py → your app directory

2. Add to your main app.py:
   from admin_routes import admin_bp
   app.register_blueprint(admin_bp)

3. Access at: http://localhost:5000/admin

# DATABASE SUMMARY:
Total Tables: {schema_info['statistics']['total_tables']}

Table Categories:
"""
    
    for category, count in sorted(schema_info['statistics']['table_categories'].items()):
        config += f"  - {category}: {count} tables\n"
    
    config += """
# FEATURES:
✅ Complete database schema browser
✅ Sample data viewer for all tables  
✅ Route explorer
✅ Responsive design
✅ Export functionality
✅ Real-time data loading

# SECURITY NOTES:
- This is a LOCAL admin interface for development
- Add authentication before deploying to production
- Consider restricting access to sensitive tables

# CUSTOMIZATION:
- Modify admin_templates/static/css/admin.css for styling
- Add authentication in admin_routes.py
- Extend functionality in admin_templates/static/js/admin.js
"""
    
    with open('admin_templates/SETUP_INSTRUCTIONS.md', 'w') as f:
        f.write(config)
    
    print("✅ Generated SETUP_INSTRUCTIONS.md")
    print("\n🎉 LOCAL ADMIN INTERFACE GENERATED SUCCESSFULLY!")
    print("📁 Files created in 'admin_templates/' directory")
    print("🚀 Follow SETUP_INSTRUCTIONS.md to integrate with your Flask app")

if __name__ == '__main__':
    schema_info, routes_info = analyze_complete_system()
