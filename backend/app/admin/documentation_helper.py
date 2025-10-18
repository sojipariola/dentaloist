# app/admin/documentation_helper.py
class DocumentationHelper:
    """Helper class for generating dynamic documentation content."""
    
    @staticmethod
    def get_available_sections(user):
        """Get documentation sections available to the user based on permissions."""
        sections = {
            'getting_started': {
                'title': 'Getting Started',
                'items': ['overview', 'quick_start', 'system_requirements'],
                'icon': '🚀'
            },
            'user_management': {
                'title': 'User Management', 
                'items': ['user_roles'],
                'icon': '👥',
                'required_permission': 'can_manage_users'
            },
            'patient_management': {
                'title': 'Patient Management',
                'items': ['patient_registration'],
                'icon': '🏥',
                'required_permission': 'can_manage_patients'
            },
            # Add more sections as needed
        }
        
        available_sections = {}
        for key, section in sections.items():
            if 'required_permission' not in section or getattr(user, section['required_permission'], False) or user.is_admin:
                available_sections[key] = section
                
        return available_sections
    
    @staticmethod
    def get_quick_links(user):
        """Get quick action links based on user permissions."""
        quick_links = []
        
        if user.is_admin or getattr(user, 'can_manage_users', False):
            quick_links.append({
                'title': 'User Management',
                'url': url_for('admin.model_view', model_name='user'),
                'description': 'Manage staff accounts and permissions',
                'icon': '👥'
            })
            
        if user.is_admin or getattr(user, 'can_manage_patients', False):
            quick_links.append({
                'title': 'Patient Records',
                'url': url_for('admin.model_view', model_name='patient'), 
                'description': 'Access and manage patient information',
                'icon': '🏥'
            })
            
        # Add more quick links based on permissions
        
        return quick_links