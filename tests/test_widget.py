"""Tests for the widget module."""

from __future__ import annotations

import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "description,expected",
    [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
        ("Visa Classic 4111111111111111", "Visa Classic 4111 11** **** 1111"),
    ],
)
def test_mask_account_card_with_cards(
    description: str, expected: str
) -> None:
    """Test masking of card descriptions."""
    result = mask_account_card(description)
    assert result == expected


@pytest.mark.parametrize(
    "description,expected",
    [
        ("Account 73654108430135874305", "Account **4305"),
        ("Account 40817810099910004312", "Account **4312"),
        ("Account 12345678901234567890", "Account **7890"),
    ],
)
def test_mask_account_card_with_accounts(
    description: str, expected: str
) -> None:
    """Test masking of account descriptions."""
    result = mask_account_card(description)
    assert result == expected


@pytest.mark.parametrize(
    "description,expected",
    [
        ("SingleWord", "SingleWord"),  # No number
        ("", ""),  # Empty string
        ("Visa", "Visa"),  # No number
    ],
)
def test_mask_account_card_edge_cases(
    description: str, expected: str
) -> None:
    """Test edge cases for descriptions without numbers."""
    result = mask_account_card(description)
    assert result == expected


@pytest.mark.parametrize(
    "description",
    [
        "account 1234567890123456",  # Lowercase "account"
        "ACCOUNT 1234567890123456",  # Uppercase "ACCOUNT"
        "Account Number 1234567890123456",  # Multiple words
    ],
)
def test_mask_account_card_case_insensitive(description: str) -> None:
    """Test that account detection is case-insensitive."""
    result = mask_account_card(description)
    # Should use account masking (last 4 digits)
    assert result.endswith("**3456")
    assert "Account" in result or "account" in result or "ACCOUNT" in result


def test_mask_account_card_with_card_descriptions_fixture(
    sample_card_descriptions: list[tuple[str, str]]
) -> None:
    """Test card descriptions using fixture data."""
    for description, expected in sample_card_descriptions:
        result = mask_account_card(description)
        assert result == expected


def test_mask_account_card_with_account_descriptions_fixture(
    sample_account_descriptions: list[tuple[str, str]]
) -> None:
    """Test account descriptions using fixture data."""
    for description, expected in sample_account_descriptions:
        result = mask_account_card(description)
        assert result == expected


def test_mask_account_card_with_edge_cases_fixture(
    edge_case_descriptions: list[tuple[str, str]]
) -> None:
    """Test edge cases using fixture data."""
    for description, expected in edge_case_descriptions:
        result = mask_account_card(description)
        assert result == expected


@pytest.mark.parametrize(
    "date_str,expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-01-01T10:00:00.000000", "01.01.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2024-02-29T12:00:00.000000", "29.02.2024"),  # Leap year
        ("2024-06-15T15:30:45.123456", "15.06.2024"),
    ],
)
def test_get_date_formatting(date_str: str, expected: str) -> None:
    """Test conversion of ISO date strings to DD.MM.YYYY format."""
    result = get_date(date_str)
    assert result == expected


@pytest.mark.parametrize(
    "date_str",
    [
        "2024-01-01T00:00:00",
        "2024-12-31T23:59:59",
        "2024-03-11T02:26:18.671407",
    ],
)
def test_get_date_without_microseconds(date_str: str) -> None:
    """Test that dates with and without microseconds work."""
    result = get_date(date_str)
    # Should be in DD.MM.YYYY format
    assert len(result) == 10
    assert result[2] == "." and result[5] == "."


def test_get_date_with_fixture(
    sample_dates: list[tuple[str, str]]
) -> None:
    """Test date formatting using fixture data."""
    for date_str, expected in sample_dates:
        result = get_date(date_str)
        assert result == expected


def test_get_date_invalid_format() -> None:
    """Test that invalid date format raises an error."""
    with pytest.raises(ValueError):
        get_date("invalid-date-format")


def test_get_date_empty_string() -> None:
    """Test that empty date string raises an error."""
    with pytest.raises(ValueError):
        get_date("")
