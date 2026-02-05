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
        whose ``state`` field equals ``state``.
    """

    return [op for op in operations if op.get("state") == state]


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
        A new list of dictionaries sorted by the ``date`` key.
    """

    return sorted(
        operations,
        key=lambda op: op.get("date", ""),
        reverse=descending,
    )

