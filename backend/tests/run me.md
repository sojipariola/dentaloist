# Run the simple tests first
python3 -m pytest tests/test_auth_simple.py -v

# If that works, try the auth routes tests
python3 -m pytest tests/unit/test_auth_routes.py -v