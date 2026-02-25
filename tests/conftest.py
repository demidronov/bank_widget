"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import pytest


@pytest.fixture
def sample_card_numbers() -> list[tuple[str, str]]:
    """Fixture providing card number test cases (input, expected_output)."""
    return [
        ("7000792289606362", "7000 79** **** 6362"),
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("4111111111111111", "4111 11** **** 1111"),
        ("5555555555554444", "5555 55** **** 4444"),
    ]


@pytest.fixture
def sample_account_numbers() -> list[tuple[str, str]]:
    """Fixture providing account number test cases (input, expected_output)."""
    return [
        ("40817810099910004312", "**4312"),
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
        ("00000000000000000001", "**0001"),
    ]


@pytest.fixture
def sample_card_descriptions() -> list[tuple[str, str]]:
    """Fixture providing card description test cases (input, expected_output)."""
    return [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
        ("Visa Classic 4111111111111111", "Visa Classic 4111 11** **** 1111"),
    ]


@pytest.fixture
def sample_account_descriptions() -> list[tuple[str, str]]:
    """Fixture providing account description test cases (input, expected_output)."""
    return [
        ("Account 73654108430135874305", "Account **4305"),
        ("Account 40817810099910004312", "Account **4312"),
        ("Account 12345678901234567890", "Account **7890"),
    ]


@pytest.fixture
def sample_dates() -> list[tuple[str, str]]:
    """Fixture providing date string test cases (input, expected_output)."""
    return [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-01-01T10:00:00.000000", "01.01.2024"),
        ("2023-12-31T23:59:59.999999", "31.12.2023"),
        ("2024-02-29T12:00:00.000000", "29.02.2024"),  # Leap year
        ("2024-06-15T15:30:45.123456", "15.06.2024"),
    ]


@pytest.fixture
def edge_case_card_numbers() -> list[tuple[str, str]]:
    """Fixture providing edge case card numbers (input, expected_output)."""
    return [
        ("123456789012345", "123456789012345"),  # Less than 16 digits
        ("1234", "1234"),  # Too short
        ("", ""),  # Empty string
        ("7000 7922 8960 6362", "7000 79** **** 6362"),  # With spaces
        ("7000-7922-8960-6362", "7000 79** **** 6362"),  # With dashes
        ("abc7000792289606362def", "7000 79** **** 6362"),  # With letters
    ]


@pytest.fixture
def edge_case_account_numbers() -> list[tuple[str, str]]:
    """Fixture providing edge case account numbers (input, expected_output)."""
    return [
        ("123", "123"),  # Less than 4 digits
        ("", ""),  # Empty string
        ("4081 7810 0999 1000 4312", "**4312"),  # With spaces
        ("4081-7810-0999-1000-4312", "**4312"),  # With dashes
        ("abc40817810099910004312def", "**4312"),  # With letters
    ]


@pytest.fixture
def edge_case_descriptions() -> list[tuple[str, str]]:
    """Fixture providing edge case descriptions (input, expected_output)."""
    return [
        ("SingleWord", "SingleWord"),  # No number
        ("", ""),  # Empty string
        ("Visa", "Visa"),  # No number
    ]
