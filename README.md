# Bank Widget

Backend utilities for a bank widget that displays recent successful transactions.

## Project Structure

```
.
├── src/                      # Source code
│   ├── __init__.py
│   ├── decorators.py         # Decorators for logging function execution
│   ├── external_api.py       # External API utilities
│   ├── file_readers.py       # Functions for reading CSV and XLSX files
│   ├── generators.py         # Generators for transaction data processing
│   ├── logging_config.py     # Logging configuration
│   ├── masks.py              # Card and account masking utilities
│   ├── processing.py         # Transaction processing functions
│   ├── utils.py              # Utility functions
│   └── widget.py             # Widget date formatting and masking
├── tests/                    # Unit tests
│   ├── __init__.py
│   ├── conftest.py           # Pytest fixtures and configuration
│   ├── test_decorators.py    # Tests for decorators module
│   ├── test_external_api.py  # Tests for external API module
│   ├── test_file_readers.py  # Tests for file_readers module
│   ├── test_generators.py    # Tests for generators module
│   ├── test_masks.py         # Tests for masks module
│   ├── test_processing.py    # Tests for processing module
│   ├── test_utils.py         # Tests for utils module
│   ├── test_widget.py        # Tests for widget module
│   └── README.md             # Tests documentation
├── pyproject.toml            # Project configuration
└── README.md                 # This file
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
- `test_decorators.py` - Tests for the `decorators` module
- `test_external_api.py` - Tests for the `external_api` module
- `test_file_readers.py` - Tests for the `file_readers` module
- `test_generators.py` - Tests for the `generators` module
- `test_masks.py` - Tests for the `masks` module
- `test_processing.py` - Tests for the `processing` module
- `test_utils.py` - Tests for the `utils` module
- `test_widget.py` - Tests for the `widget` module

## Coverage

The project maintains **97.58% test coverage** for all source modules.

## Test Features

- **Fixtures**: Reusable test data fixtures defined in `conftest.py`
- **Parametrization**: Tests use `@pytest.mark.parametrize` for multiple test cases
- **Edge Cases**: Comprehensive testing of edge cases and error conditions

## Modules

### generators.py
Provides generator functions for efficient processing of large volumes of transaction data:
- `filter_by_currency(transactions, currency)` - Returns an iterator that yields transactions matching a specified currency
- `transaction_descriptions(transactions)` - Generator that yields description strings for each transaction
- `card_number_generator(start, stop)` - Generates bank card numbers in XXXX XXXX XXXX XXXX format

#### Example Usage

```python
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

# Filter transactions by currency
transactions = [
    {"id": 1, "currency": "USD", "amount": 100, "description": "Payment"},
    {"id": 2, "currency": "EUR", "amount": 150, "description": "Refund"},
]

# Get USD transactions
for transaction in filter_by_currency(transactions, "USD"):
    print(transaction)

# Get all transaction descriptions
for description in transaction_descriptions(transactions):
    print(description)

# Generate card numbers
for card_number in card_number_generator(start=1, stop=10):
    print(card_number)  # Output: 0000 0000 0000 0001, 0000 0000 0000 0002, ...
```

### masks.py
Provides utilities for masking sensitive financial information:
- `get_mask_card_number()` - Masks credit/debit card numbers
- `get_mask_account()` - Masks bank account numbers

### widget.py
Provides widget-related utilities:
- `mask_account_card()` - Masks account/card descriptions
- `get_date()` - Formats ISO date strings to DD.MM.YYYY format

### processing.py
Transaction processing utilities for the bank widget:
- `filter_by_state()` - Filters transactions by state
- `sort_by_date()` - Sorts transactions by date

### file_readers.py
Provides functions for reading financial transactions from various file formats:
- `read_transactions_from_csv(file_path)` - Reads transactions from CSV files
- `read_transactions_from_xlsx(file_path)` - Reads transactions from Excel files

Both functions accept a file path (string or Path object) and return a list of dictionaries representing transactions.

#### Example Usage

```python
from src.file_readers import read_transactions_from_csv, read_transactions_from_xlsx

# Read from CSV file
csv_transactions = read_transactions_from_csv("transactions.csv")
for transaction in csv_transactions:
    print(transaction)

# Read from Excel file
xlsx_transactions = read_transactions_from_xlsx("transactions.xlsx")
for transaction in xlsx_transactions:
    print(transaction)
```

#### Features
- **Automatic format detection**: Automatically detects and handles CSV and XLSX formats
- **Path flexibility**: Accepts both string paths and `pathlib.Path` objects
- **Type hints**: Full type annotations for better IDE support and type checking
- **Error handling**: Comprehensive error handling with informative exception messages
- **Data conversion**: Automatically converts file data to list of dictionaries for easy processing


Содержит полезные декораторы для трассировки и логирования выполнения функций.

- `log(filename=None)` — декоратор для автоматического логирования вызовов функций.
  - Если `filename` указан, логи добавляются в указанный файл.
  - Если `filename` не указан, логи выводятся в консоль.
  - В лог включается временная метка, имя функции, входные аргументы, результат или информация об ошибке.

Пример использования:

```python
from src.decorators import log

@log()
def add(a, b):
    return a + b

@log(filename="app.log")
def do_work(x):
    if x < 0:
        raise ValueError("negative")
    return x * 2
```
