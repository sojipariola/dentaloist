# tests/run_tests.py

import pytest
import sys

if __name__ == "__main__":
    # Run all tests
    exit_code = pytest.main(["-x", "-v", "tests/"])
    sys.exit(exit_code)