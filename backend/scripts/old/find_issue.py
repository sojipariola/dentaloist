import os
import sys

from ..app import create_app
import re
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

app = create_app()

# Search for remote_side usage in your model files
def find_remote_side_issues():
    import os
    models_path = 'app/models'
    
    for root, dirs, files in os.walk(models_path):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                    if 'remote_side' in content:
                        print(f"Found remote_side in {filepath}")
                        # Look for problematic patterns
                        lines = content.split('\n')
                        for i, line in enumerate(lines, 1):
                            if 'remote_side' in line and '=id' in line.replace(' ', ''):
                                print(f"  Line {i}: {line.strip()}")

find_remote_side_issues()