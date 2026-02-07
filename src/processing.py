"""Data processing helpers for bank operations.

This module provides filtering and sorting utilities used by the
widget presentation layer and tests.
"""

from __future__ import annotations

from datetime import datetime
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
            ``"EXECUTED"``.

    Returns:
        A new list of dictionaries that contain only the operations
        whose ``state`` field equals ``state``.
    """

    operations_list = list(operations)
    return [op for op in operations_list if op.get("state") == state]


def sort_by_date(
    operations: Iterable[Mapping[str, Any]],
    descending: bool = True,
) -> List[Mapping[str, Any]]:
    """Return operations sorted by their ``date`` field.

    The function attempts to parse ISO-formatted datetime strings found in
    the ``date`` key. If parsing fails or the key is missing, the entry is
    treated as very old/new depending on the requested order so that
    entries with valid dates are ordered as expected.

    Args:
        operations: Iterable of operation dictionaries.
        descending: If ``True`` (default), sort from newest to oldest;
            if ``False``, sort from oldest to newest.

    Returns:
        A new list of dictionaries sorted by the parsed datetime values.
    """

    operations_list = list(operations)

    def _key(op: Mapping[str, Any]) -> datetime:
        val = op.get("date")
        if not isinstance(val, str):
            return datetime.min if descending else datetime.max
        try:
            return datetime.fromisoformat(val)
        except Exception:
            return datetime.min if descending else datetime.max

    return sorted(operations_list, key=_key, reverse=descending)
