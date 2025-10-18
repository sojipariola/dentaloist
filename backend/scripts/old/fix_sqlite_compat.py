import os
import re
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "app" / "models"
COMPAT_FILE = MODELS_DIR / "_compat.py"
BACKUP_DIR = MODELS_DIR.parent / "models_backup_before_sqlite_fix"

# 1️⃣ Backup existing models directory
if not BACKUP_DIR.exists():
    shutil.copytree(MODELS_DIR, BACKUP_DIR)
    print(f"✅ Backup created at: {BACKUP_DIR}")
else:
    print(f"⚠️ Backup already exists at: {BACKUP_DIR}")

# 2️⃣ Ensure compat helper exists
if not COMPAT_FILE.exists():
    with open(COMPAT_FILE, "w") as f:
        f.write('''\
from sqlalchemy.types import TypeDecorator, JSON, String
from sqlalchemy.dialects.postgresql import ARRAY

class ArrayOrJSON(TypeDecorator):
    """Emulates ARRAY for SQLite using JSON."""
    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'sqlite':
            return dialect.type_descriptor(JSON())
        else:
            return dialect.type_descriptor(ARRAY(String()))

    def process_bind_param(self, value, dialect):
        if value is None:
            return []
        return value

    def process_result_value(self, value, dialect):
        return value or []
''')
    print("✅ Created app/models/_compat.py")

# 3️⃣ Replace ARRAY(...) and JSONB with ArrayOrJSON
for model_file in MODELS_DIR.glob("*.py"):
    if model_file.name == "__init__.py" or model_file.name == "_compat.py":
        continue

    with open(model_file, "r") as f:
        content = f.read()

    original_content = content

    # Ensure import present
    if "ArrayOrJSON" not in content:
        if "from app.models._compat import ArrayOrJSON" not in content:
            content = (
                "from app.models._compat import ArrayOrJSON\n" + content
            )

    # Replace ARRAY(...) usage
    content = re.sub(
        r"ARRAY\s*\([^)]*\)",
        "ArrayOrJSON()",
        content
    )

    # Replace JSONB usage if any
    content = re.sub(
        r"JSONB\s*\([^)]*\)",
        "ArrayOrJSON()",
        content
    )

    if content != original_content:
        with open(model_file, "w") as f:
            f.write(content)
        print(f"🛠️ Updated: {model_file.name}")

print("✅ SQLite compatibility fix completed!")
print("👉 Next steps:")
print("   1. rm -rf migrations instance app.db")
print('   2. flask db init && flask db migrate -m "SQLite fix" && flask db upgrade')
print("   3. python3 setup_database.py")

'''
python3 scripts/fix_sqlite_compat.py


rm -rf migrations instance app.db
flask db init
flask db migrate -m "SQLite fix"
flask db upgrade
python3 setup_database.py


rm -rf instance app.db migrations
flask db init
flask db migrate -m "reset"
flask db upgrade
python3 setup_database.py

'''