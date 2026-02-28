"""Tests for the processing module."""

from __future__ import annotations

import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "operations, state, expected",
    [
        (
            [
                {"id": 1, "state": "EXECUTED"},
                {"id": 2, "state": "CANCELLED"},
                {"id": 3, "state": "EXECUTED"},
            ],
            "EXECUTED",
            [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}],
        ),
        (
            [
                {"id": 1, "state": "EXECUTED"},
                {"id": 2},  # missing state key
                {"id": 3, "state": "EXECUTED"},
            ],
            "EXECUTED",
            [{"id": 1, "state": "EXECUTED"}, {"id": 3, "state": "EXECUTED"}],
        ),
        (
            [],
            "EXECUTED",
            [],
        ),
        (
            [
                {"id": 1, "state": "NEW"},
                {"id": 2, "state": "NEW"},
            ],
            "NEW",
            [{"id": 1, "state": "NEW"}, {"id": 2, "state": "NEW"}],
        ),
    ],
)
def test_filter_by_state_various(
    operations: list[dict[str, object]], state: str, expected: list[dict[str, object]]
) -> None:
    """Verify that only items with matching 'state' are returned."""
    result = filter_by_state(operations, state)
    assert result == expected


def test_filter_by_state_default() -> None:
    """Default state filter should be 'EXECUTED'."""
    ops = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "CANCELLED"},
    ]
    assert filter_by_state(ops) == [{"id": 1, "state": "EXECUTED"}]


@pytest.mark.parametrize(
    "operations, reverse, expected_order",
    [
        (
            [
                {"id": 1, "date": "2024-01-01"},
                {"id": 2, "date": "2024-01-03"},
                {"id": 3, "date": "2024-01-02"},
            ],
            True,
            [2, 3, 1],
        ),
        (
            [
                {"id": 1, "date": "2024-01-01"},
                {"id": 2, "date": "2024-01-03"},
                {"id": 3, "date": "2024-01-02"},
            ],
            False,
            [1, 3, 2],
        ),
        (
            [
                {"id": 1},  # missing date
                {"id": 2, "date": "2024-01-01"},
            ],
            True,
            [2, 1],  # missing date treated as empty string and moves last in reverse order
        ),
        (
            [],
            True,
            [],
        ),
    ],
)
def test_sort_by_date_various(
    operations: list[dict[str, object]], reverse: bool, expected_order: list[int]
) -> None:
    """Ensure sorting by date works in both directions and handles edge cases."""
    sorted_ops = sort_by_date(operations, reverse=reverse)
    assert [op.get("id") for op in sorted_ops] == expected_order


def test_sort_by_date_defaults() -> None:
    """Default sort order should be descending (reverse=True)."""
    ops = [
        {"id": 1, "date": "2024-01-01"},
        {"id": 2, "date": "2024-01-02"},
    ]
    result = sort_by_date(ops)
    assert result[0]["id"] == 2


def test_sort_by_date_same_dates() -> None:
    """Items with the same date should preserve relative order (stable sort)."""
    ops = [
        {"id": 1, "date": "2024-01-01"},
        {"id": 2, "date": "2024-01-01"},
    ]
    result = sort_by_date(ops)
    assert [op["id"] for op in result] == [1, 2]
