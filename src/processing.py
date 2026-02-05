"""Data processing helpers for banking operations."""

from __future__ import annotations

from typing import Any, Iterable, List, Mapping

__all__ = ["filter_by_state", "sort_by_date"]


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

