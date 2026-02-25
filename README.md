# Bank Widget

Backend utilities for a bank widget that displays recent successful transactions.

## Project Structure

```
.
├── src/                    # Source code
│   ├── __init__.py
│   ├── masks.py           # Card and account masking utilities
│   ├── processing.py      # Transaction processing functions
│   └── widget.py          # Widget date formatting and masking
├── tests/                 # Unit tests
│   ├── __init__.py
│   ├── conftest.py        # Pytest fixtures and configuration
│   ├── test_masks.py      # Tests for masks module
│   └── test_widget.py     # Tests for widget module
├── pyproject.toml         # Project configuration
└── README.md              # This file
```

## Installation

```bash
poetry install
```

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

## Modules

### masks.py
Provides utilities for masking sensitive financial information:
- `get_mask_card_number()` - Masks credit/debit card numbers
- `get_mask_account()` - Masks bank account numbers

### widget.py
Provides widget-related utilities:
- `mask_account_card()` - Masks account/card descriptions
- `get_date()` - Formats ISO date strings to DD.MM.YYYY format

### processing.py
Transaction processing utilities for the bank widget.
