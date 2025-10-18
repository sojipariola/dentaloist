#!/usr/bin/env python3
"""
Comprehensive test runner for the entire Dentaloist application
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Command failed: {command}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return False

def main():
    """Run all test suites"""
    print("🚀 Starting Comprehensive Dentaloist Test Suite")
    print("=" * 60)
    
    base_dir = Path(__file__).parent.parent
    backend_dir = base_dir / 'backend'
    frontend_dir = base_dir / 'vite-dentaloist'
    
    all_passed = True
    
    # 1. Backend Unit Tests
    print("\n1. Running Backend Unit Tests...")
    if run_command("python -m pytest tests/unit/ -v", cwd=backend_dir):
        print("✅ Backend unit tests passed")
    else:
        print("❌ Backend unit tests failed")
        all_passed = False
    
    # 2. Backend Integration Tests
    print("\n2. Running Backend Integration Tests...")
    if run_command("python -m pytest tests/integration/ -v", cwd=backend_dir):
        print("✅ Backend integration tests passed")
    else:
        print("❌ Backend integration tests failed")
        all_passed = False
    
    # 3. Frontend Unit Tests
    print("\n3. Running Frontend Unit Tests...")
    if run_command("npm test -- --coverage", cwd=frontend_dir):
        print("✅ Frontend unit tests passed")
    else:
        print("❌ Frontend unit tests failed")
        all_passed = False
    
    # 4. Frontend E2E Tests
    print("\n4. Running Frontend E2E Tests...")
    if run_command("npx playwright test", cwd=frontend_dir):
        print("✅ Frontend E2E tests passed")
    else:
        print("❌ Frontend E2E tests failed")
        all_passed = False
    
    # 5. Cross-Platform Integration Tests
    print("\n5. Running Cross-Platform Integration Tests...")
    if run_command("python -m pytest tests/integration/ -v", cwd=base_dir / 'tests'):
        print("✅ Cross-platform integration tests passed")
    else:
        print("❌ Cross-platform integration tests failed")
        all_passed = False
    
    # 6. Performance Tests
    print("\n6. Running Performance Tests...")
    if run_command("python -m pytest tests/performance/ -v", cwd=base_dir / 'tests'):
        print("✅ Performance tests passed")
    else:
        print("❌ Performance tests failed")
        all_passed = False
    
    # 7. Security Tests
    print("\n7. Running Security Tests...")
    if run_command("python -m pytest tests/security/ -v", cwd=base_dir / 'tests'):
        print("✅ Security tests passed")
    else:
        print("❌ Security tests failed")
        all_passed = False
    
    # Final Results
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TEST SUITES PASSED! Application is ready for deployment.")
    else:
        print("💥 SOME TESTS FAILED! Please fix the issues above.")
        sys.exit(1)

if __name__ == '__main__':
    main()