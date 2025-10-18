# backend/scripts/check_login_form.py
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_login_form():
    print("🔍 CHECKING LOGIN FORM HTML")
    print("=" * 50)
    
    # Look for login form templates
    templates_path = 'app/templates'
    login_templates = []
    
    if os.path.exists(templates_path):
        for root, dirs, files in os.walk(templates_path):
            for file in files:
                if file.endswith('.html') and ('login' in file.lower() or 'auth' in file.lower()):
                    login_templates.append(os.path.join(root, file))
    
    if login_templates:
        print(f"📁 Found login templates:")
        for template in login_templates:
            print(f"   - {template}")
            
            # Check for form fields
            with open(template, 'r') as f:
                content = f.read()
                
                # Check for common issues
                issues = []
                
                # Check for input fields without id/name
                if '<input' in content and ('id=' not in content or 'name=' not in content):
                    issues.append("Input fields missing id or name attributes")
                
                # Check for missing autocomplete
                if '<input' in content and 'autocomplete=' not in content:
                    issues.append("Input fields missing autocomplete attribute")
                
                # Check for missing labels
                if '<input' in content and '<label' not in content:
                    issues.append("Input fields missing associated labels")
                
                if issues:
                    print(f"   ❌ Issues found:")
                    for issue in issues:
                        print(f"      - {issue}")
                else:
                    print(f"   ✅ No accessibility issues found")
                    
                # Show form section
                if '<form' in content:
                    form_start = content.find('<form')
                    form_end = content.find('</form>') + 7
                    form_html = content[form_start:form_end]
                    
                    print(f"   📝 Form HTML:")
                    lines = form_html.split('\n')
                    for i, line in enumerate(lines[:10]):  # Show first 10 lines
                        print(f"      {line.strip()}")
    else:
        print("❌ No login templates found")

if __name__ == '__main__':
    check_login_form()