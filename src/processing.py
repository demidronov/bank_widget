"""Data processing helpers for banking operations."""

from __future__ import annotations

import re
from typing import Any, Iterable, List, Mapping

__all__ = ["filter_by_state", "sort_by_date", "process_bank_search", "process_bank_operations"]


def filter_by_state(
    operations: Iterable[Mapping[str, Any]],
    state: str = "EXECUTED",
) -> List[Mapping[str, Any]]:
    """Return only operations with the given state.

    Args:
        operations: Iterable of operation dictionaries.
        state: Target state value for the ``state`` key, defaults to
            ``\"EXECUTED\"``.

    Returns:
        A new list of dictionaries that contain only the operations
        whose ``state`` field equals ``state``. Returns an empty list
        if no operations match or if the input is empty.

    Example:
        >>> ops = [
        ...     {"state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        ...     {"state": "CANCELED", "date": "2024-01-01T10:00:00.000000"},
        ...     {"state": "EXECUTED", "date": "2024-02-15T14:30:00.000000"},
        ... ]
        >>> filter_by_state(ops)
        [{'state': 'EXECUTED', 'date': '2024-03-11T02:26:18.671407'}, ...]
        >>> filter_by_state(ops, "CANCELED")
        [{'state': 'CANCELED', 'date': '2024-01-01T10:00:00.000000'}]
    """

    # Convert to list to handle any iterable and ensure we return a list
    operations_list = list(operations)
    return [op for op in operations_list if op.get("state") == state]


def sort_by_date(
    operations: Iterable[Mapping[str, Any]],
    descending: bool = True,
) -> List[Mapping[str, Any]]:
    """Return operations sorted by their ``date`` field.

    Args:
        operations: Iterable of operation dictionaries.
        descending: If ``True`` (default), sort from newest to oldest;
            if ``False``, sort from oldest to newest.

    Returns:
        A new list of dictionaries sorted by the ``date`` key. Returns
        an empty list if the input is empty. Operations without a ``date``
        field are sorted last (or first if descending=False).

    Example:
        >>> ops = [
        ...     {"state": "EXECUTED", "date": "2024-03-11T02:26:18.671407"},
        ...     {"state": "EXECUTED", "date": "2024-01-01T10:00:00.000000"},
        ...     {"state": "EXECUTED", "date": "2024-02-15T14:30:00.000000"},
        ... ]
        >>> sort_by_date(ops)
        [{'state': 'EXECUTED', 'date': '2024-03-11T02:26:18.671407'}, ...]
        >>> sort_by_date(ops, descending=False)
        [{'state': 'EXECUTED', 'date': '2024-01-01T10:00:00.000000'}, ...]
    """

    # Convert to list to handle any iterable and ensure we return a list
    operations_list = list(operations)
    # Sort by date field, using empty string as fallback for missing dates
    return sorted(
        operations_list,
        key=lambda op: op.get("date", ""),
        reverse=descending,
    )


def process_bank_search(
    data: list[dict[str, Any]],
    search: str,
) -> list[dict[str, Any]]:
    """Return operations that match the search string in their description.

    Uses regular expressions to search for the pattern in the ``description``
    field of each operation.

    Args:
        data: List of operation dictionaries.
        search: Regular expression pattern to search for in descriptions.

    Returns:
        A new list of dictionaries that contain the search pattern in their
        ``description`` field. Returns an empty list if no operations match
        or if the input is empty.

    Example:
        >>> ops = [
        ...     {"description": "Открытие вклада", "amount": 40542},
        ...     {"description": "Перевод с карты", "amount": 130},
        ... ]
        >>> process_bank_search(ops, "вклада")
        [{'description': 'Открытие вклада', 'amount': 40542}]
    """

    result = []
    for operation in data:
        description = operation.get("description", "")
        if re.search(search, description, re.IGNORECASE):
            result.append(operation)
    return result


def process_bank_operations(
    data: list[dict[str, Any]],
    categories: list[str],
) -> dict[str, int]:
    """Count operations by categories based on their description.

    Searches for each category string in the ``description`` field of
    operations. An operation is counted for a category if the category
    string appears in its description (case-insensitive).

    Args:
        data: List of operation dictionaries.
        categories: List of category keywords to search for in descriptions.

    Returns:
        A dictionary where keys are category names and values are counts
        of operations containing that category keyword in their description.

    Example:
        >>> ops = [
        ...     {"description": "Открытие вклада"},
        ...     {"description": "Перевод с карты на карту"},
        ...     {"description": "Открытие счета"},
        ... ]
        >>> process_bank_operations(ops, ["вклада", "перевод"])
        {'вклада': 1, 'перевод': 1}
    """

    result = {category: 0 for category in categories}
    for operation in data:
        description = operation.get("description", "").lower()
        for category in categories:
            if category.lower() in description:
                result[category] += 1
    return result

