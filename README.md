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
# Bank Widget Backend Utilities

This project contains small, focused helper functions used to prepare
data for a banking widget that displays recent successful transactions
in a client's personal account.

## Installation

The project is managed with [Poetry](https://python-poetry.org/).

```bash
poetry install --with lint
```

If you cannot access the public Python Package Index from your network,
use your internal mirror instead of the default ``pypi.org``.

## Provided modules

### `masks`

Functions for masking card and account numbers:

- `get_mask_card_number(card_number: str) -> str`
- `get_mask_account(account_number: str) -> str`

Example:

```python
from src.masks import get_mask_account, get_mask_card_number

print(get_mask_card_number("7000792289606362"))
print(get_mask_account("40817810099910004312"))
```

### `widget`

Functions for preparing values for display in the widget:

- `mask_account_card(description: str) -> str` — masks the number in
  a one-line description such as
  `"Visa Platinum 7000792289606361"` or
  `"Account 73654108430135874305"`.
- `get_date(date_str: str) -> str` — converts a date-time string like
  `"2024-03-11T02:26:18.671407"` to `"11.03.2024"`.

Example:

```python
from src.widget import get_date, mask_account_card

masked = mask_account_card("Visa Platinum 7000792289606361")
print(masked)

formatted = get_date("2024-03-11T02:26:18.671407")
print(formatted)
```

### `processing`

Functions for filtering and sorting operations data:

- `filter_by_state(operations, state="EXECUTED") -> list` — returns
  only operations whose `"state"` matches the given value.
- `sort_by_date(operations, descending=True) -> list` — returns
  operations sorted by the `"date"` field (by default from newest
  to oldest).

Example:

```python
from src.processing import filter_by_state, sort_by_date

operations = [
    {"state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
    {"state": "CANCELED", "date": "2024-01-01T10:00:00.000000"},
]

executed = filter_by_state(operations)  # only EXECUTED operations
sorted_ops = sort_by_date(executed)    # sorted by date, newest first
```

