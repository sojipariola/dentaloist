FRONTEND TESTS
# Run unit tests
npm run test
# Run e2e tests (make sure dev server is running)
npm run test:e2e


BACKEND TESTS 
# Run all tests
python -m pytest tests/ -v
# Run specific test file
python -m pytest tests/test_core_models.py -v
# Run tests with coverage
python -m pytest tests/ --cov=app --cov-report=html
# Run tests in parallel
python -m pytest tests/ -n auto


# Install test dependencies first
pip install pytest pytest-cov
# Run all tests
python -m pytest tests/ -v
# Run specific test file
python -m pytest tests/test_base_models.py -v
# Run tests with coverage (if you have pytest-cov)
python -m pytest tests/ --cov=app --cov-report=term-missing
# Run tests and stop on first failure
python -m pytest tests/ -x
# Run tests and show stdout
python -m pytest tests/ -s