"""Tests for the masks module."""

from __future__ import annotations

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number,expected",
    [
        ("7000792289606362", "7000 79** **** 6362"),
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("4111111111111111", "4111 11** **** 1111"),
        ("5555555555554444", "5555 55** **** 4444"),
    ],
)
def test_get_mask_card_number_valid(card_number: str, expected: str) -> None:
    """Test masking of valid 16-digit card numbers."""
    result = get_mask_card_number(card_number)
    assert result == expected


@pytest.mark.parametrize(
    "card_number,expected",
    [
        ("123456789012345", "123456789012345"),  # Less than 16 digits
        ("1234", "1234"),  # Too short
        ("", ""),  # Empty string
    ],
)
def test_get_mask_card_number_short(card_number: str, expected: str) -> None:
    """Test that short card numbers are returned unchanged."""
    result = get_mask_card_number(card_number)
    assert result == expected


@pytest.mark.parametrize(
    "card_number,expected",
    [
        ("7000 7922 8960 6362", "7000 79** **** 6362"),  # With spaces
        ("7000-7922-8960-6362", "7000 79** **** 6362"),  # With dashes
        ("abc7000792289606362def", "7000 79** **** 6362"),  # With letters
    ],
)
def test_get_mask_card_number_with_formatting(
    card_number: str, expected: str
) -> None:
    """Test that card numbers with formatting are handled correctly."""
    result = get_mask_card_number(card_number)
    assert result == expected


def test_get_mask_card_number_with_fixture(
    sample_card_numbers: list[tuple[str, str]]
) -> None:
    """Test card number masking using fixture data."""
    for card_number, expected in sample_card_numbers:
        result = get_mask_card_number(card_number)
        assert result == expected


def test_get_mask_card_number_edge_cases_with_fixture(
    edge_case_card_numbers: list[tuple[str, str]]
) -> None:
    """Test edge cases using fixture data."""
    for card_number, expected in edge_case_card_numbers:
        result = get_mask_card_number(card_number)
        assert result == expected


@pytest.mark.parametrize(
    "account_number,expected",
    [
        ("40817810099910004312", "**4312"),
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
        ("00000000000000000001", "**0001"),
    ],
)
def test_get_mask_account_valid(account_number: str, expected: str) -> None:
    """Test masking of valid account numbers."""
    result = get_mask_account(account_number)
    assert result == expected


@pytest.mark.parametrize(
    "account_number,expected",
    [
        ("123", "123"),  # Less than 4 digits
        ("", ""),  # Empty string
    ],
)
def test_get_mask_account_short(account_number: str, expected: str) -> None:
    """Test that short account numbers are returned unchanged."""
    result = get_mask_account(account_number)
    assert result == expected


@pytest.mark.parametrize(
    "account_number,expected",
    [
        ("4081 7810 0999 1000 4312", "**4312"),  # With spaces
        ("4081-7810-0999-1000-4312", "**4312"),  # With dashes
        ("abc40817810099910004312def", "**4312"),  # With letters
    ],
)
def test_get_mask_account_with_formatting(
    account_number: str, expected: str
) -> None:
    """Test that account numbers with formatting are handled correctly."""
    result = get_mask_account(account_number)
    assert result == expected


def test_get_mask_account_with_fixture(
    sample_account_numbers: list[tuple[str, str]]
) -> None:
    """Test account number masking using fixture data."""
    for account_number, expected in sample_account_numbers:
        result = get_mask_account(account_number)
        assert result == expected


def test_get_mask_account_edge_cases_with_fixture(
    edge_case_account_numbers: list[tuple[str, str]]
) -> None:
    """Test edge cases using fixture data."""
    for account_number, expected in edge_case_account_numbers:
        result = get_mask_account(account_number)
        assert result == expected
