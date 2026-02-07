# Tests

This directory contains unit tests for the bank widget backend utilities.

## Running Tests

Run all tests:
```bash
pytest
```

Run tests with coverage report:
```bash
pytest --cov=src --cov-report=term-missing
```

Generate HTML coverage report:
```bash
pytest --cov=src --cov-report=html
```

The HTML report will be generated in the `htmlcov/` directory.

## Test Structure

- `conftest.py` - Shared pytest fixtures for test data
- `test_masks.py` - Tests for the `masks` module
- `test_widget.py` - Tests for the `widget` module

## Coverage

The project maintains **100% test coverage** for all source modules.

## Test Features

- **Fixtures**: Reusable test data fixtures defined in `conftest.py`
- **Parametrization**: Tests use `@pytest.mark.parametrize` for multiple test cases
- **Edge Cases**: Comprehensive testing of edge cases and error conditions
