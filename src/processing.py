"""Functions for processing bank operation data."""

from __future__ import annotations

from typing import Any

__all__ = ["filter_by_state", "sort_by_date"]


def filter_by_state(
    operations: list[dict[str, Any]], state: str = "EXECUTED"
) -> list[dict[str, Any]]:
    """Filter operations by state.

    Accepts a list of dictionaries containing bank operation data and
    an optional state value. Returns a new list containing only those
    dictionaries whose 'state' key matches the specified value.

    Args:
        operations: List of dictionaries with operation data.
        state: The state value to filter by (default: 'EXECUTED').

    Returns:
        A new list of dictionaries filtered by the specified state.

    Example:
        >>> operations = [
        ...     {"id": 1, "state": "EXECUTED"},
        ...     {"id": 2, "state": "CANCELLED"},
        ...     {"id": 3, "state": "EXECUTED"},
        ... ]
        >>> filter_by_state(operations)
        [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}]
    """
    return [op for op in operations if op.get("state") == state]


def sort_by_date(
    operations: list[dict[str, Any]], reverse: bool = True
) -> list[dict[str, Any]]:
    """Sort operations by date.

    Accepts a list of dictionaries and an optional parameter for sorting
    order. Returns a new list sorted by the 'date' key. By default, sorts
    in descending order (newest first).

    Args:
        operations: List of dictionaries with operation data.
        reverse: Sort order; True for descending (default), False for ascending.

    Returns:
        A new list of dictionaries sorted by date.

    Example:
        >>> operations = [
        ...     {"id": 1, "date": "2024-01-01"},
        ...     {"id": 2, "date": "2024-01-03"},
        ...     {"id": 3, "date": "2024-01-02"},
        ... ]
        >>> sort_by_date(operations)
        [
        ...     {"id": 2, "date": "2024-01-03"},
        ...     {"id": 3, "date": "2024-01-02"},
        ...     {"id": 1, "date": "2024-01-01"},
        ... ]
    """
    return sorted(operations, key=lambda op: op.get("date", ""), reverse=reverse)
