<<<<<<< HEAD
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
# Bank Widget

Небольшой виджет для отображения банковских операций клиента. Проект содержит
утилиты для маскирования номеров карт/счетов и простые функции обработки данных
операций.

Установка
---------

Клонируйте репозиторий и установите зависимости (если есть):

```bash
git clone https://github.com/demidronov/bank_widget.git
cd bank_widget
python -m venv .venv
.\.venv\Scripts\activate  # Windows
pip install -r requirements.txt  # при необходимости
```

При использовании Poetry:

```bash
poetry install --with lint
```

Использование
-------------

В модуле `src.processing` реализованы две функции:

- `filter_by_state(operations, state='EXECUTED')` — возвращает новый список словарей,
  содержащий только операции с полем `state`, равным переданному значению.

- `sort_by_date(operations, descending=True)` — возвращает новый список операций,
  отсортированный по полю `date`. По умолчанию сортировка по убыванию (новые
  операции в начале).

Примеры
-------

```python
from src.processing import filter_by_state, sort_by_date

ops = [
    {"id": 1, "state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
    {"id": 2, "state": "PENDING", "date": "2023-12-01T10:00:00"},
]

executed = filter_by_state(ops)
sorted_ops = sort_by_date(executed)
```

Разработка
---------

Проект ведётся по GitFlow: есть ветки `main` и `develop`. Новая функциональность
разрабатывается в ветках с префиксом `feature/`.
