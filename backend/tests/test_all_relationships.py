"""
Diagnostic test to ensure all models and relationships can be imported cleanly.
Run from project root (backend folder):
    python tests/test_all_relationships01.py
"""

import sys
import pathlib
import importlib

# === Ensure Backend Root is in sys.path ===
BACKEND_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

print(f"📂 Added backend root to sys.path:\n  {BACKEND_ROOT}\n")

# === Define all model modules to test ===
MODEL_MODULES = [
    "app.models.analytics",
    "app.models.clinical",
    "app.models.core",
    "app.models.financial",
    "app.models.inventory",
    "app.models.role_permission",
    "app.models.system_models",
    "app.models.base",
    "app.models.lookups",
    "app.models._compat",
]

# === Import test ===
def test_model_imports():
    print("🔍 Testing model imports...\n")
    success, failed = [], []

    for module_name in MODEL_MODULES:
        try:
            module = importlib.import_module(module_name)
            print(f"✅ Imported {module_name}")
            success.append(module_name)
        except Exception as e:
            print(f"❌ Failed to import {module_name}\n   ↳ {e.__class__.__name__}: {e}\n")
            failed.append((module_name, e))

    print("\n=== Import Summary ===")
    print(f"✅ Successful: {len(success)}")
    print(f"❌ Failed: {len(failed)}")

    if failed:
        print("\nFailed modules:")
        for name, err in failed:
            print(f" - {name}: {err}")

    print("\n🔚 Done testing model imports.\n")

if __name__ == "__main__":
    test_model_imports()
