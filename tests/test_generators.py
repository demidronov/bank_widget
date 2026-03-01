"""Tests for the generators module."""

from __future__ import annotations

import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


@pytest.fixture
def sample_transactions() -> list[dict[str, object]]:
    """Provide sample transaction data for testing."""
    return [
        {"id": 1, "currency": "USD", "amount": 100, "description": "Payment"},
        {"id": 2, "currency": "EUR", "amount": 150, "description": "Refund"},
        {"id": 3, "currency": "USD", "amount": 200, "description": "Deposit"},
        {"id": 4, "currency": "GBP", "amount": 50},  # missing description
    ]


class TestFilterByCurrency:
    """Tests for filter_by_currency function."""

    def test_filter_by_currency_single_match(
        self, sample_transactions: list[dict[str, object]]
    ) -> None:
        """Test filtering returns correct currency transactions."""
        result = list(filter_by_currency(sample_transactions, "USD"))
        assert len(result) == 2
        assert all(t["currency"] == "USD" for t in result)
        assert [t["id"] for t in result] == [1, 3]

    @pytest.mark.parametrize(
        "currency, expected_count, expected_ids",
        [
            ("USD", 2, [1, 3]),
            ("EUR", 1, [2]),
            ("GBP", 1, [4]),
            ("JPY", 0, []),
        ],
    )
    def test_filter_by_currency_various(
        self,
        sample_transactions: list[dict[str, object]],
        currency: str,
        expected_count: int,
        expected_ids: list[int],
    ) -> None:
        """Test filtering with various currencies."""
        result = list(filter_by_currency(sample_transactions, currency))
        assert len(result) == expected_count
        assert [t["id"] for t in result] == expected_ids

    def test_filter_by_currency_empty_list(self) -> None:
        """Test filtering on empty transaction list."""
        result = list(filter_by_currency([], "USD"))
        assert result == []

    def test_filter_by_currency_returns_generator(
        self, sample_transactions: list[dict[str, object]]
    ) -> None:
        """Test that function returns a generator/iterator."""
        result = filter_by_currency(sample_transactions, "USD")
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_filter_by_currency_case_sensitive(
        self, sample_transactions: list[dict[str, object]]
    ) -> None:
        """Test that currency filter is case-sensitive."""
        result = list(filter_by_currency(sample_transactions, "usd"))
        assert len(result) == 0


class TestTransactionDescriptions:
    """Tests for transaction_descriptions function."""

    def test_transaction_descriptions_basic(
        self, sample_transactions: list[dict[str, object]]
    ) -> None:
        """Test getting descriptions from transactions."""
        result = list(transaction_descriptions(sample_transactions))
        assert len(result) == 3  # Only 3 have descriptions
        assert "Payment" in result
        assert "Refund" in result
        assert "Deposit" in result

    @pytest.mark.parametrize(
        "transactions, expected_descriptions",
        [
            (
                [{"description": "Test"}],
                ["Test"],
            ),
            (
                [{"id": 1}, {"description": "Only this"}],
                ["Only this"],
            ),
            (
                [{"description": ""}, {"description": "Valid"}],
                ["Valid"],
            ),
            (
                [],
                [],
            ),
        ],
    )
    def test_transaction_descriptions_various(
        self,
        transactions: list[dict[str, object]],
        expected_descriptions: list[str],
    ) -> None:
        """Test descriptions with various inputs."""
        result = list(transaction_descriptions(transactions))
        assert result == expected_descriptions

    def test_transaction_descriptions_ignores_missing(
        self, sample_transactions: list[dict[str, object]]
    ) -> None:
        """Test that transactions without descriptions are skipped."""
        result = list(transaction_descriptions(sample_transactions))
        assert all(isinstance(desc, str) for desc in result)
        assert all(len(desc) > 0 for desc in result)

    def test_transaction_descriptions_returns_generator(
        self, sample_transactions: list[dict[str, object]]
    ) -> None:
        """Test that function returns a generator."""
        result = transaction_descriptions(sample_transactions)
        assert hasattr(result, "__iter__")
        assert hasattr(result, "__next__")

    def test_transaction_descriptions_lazy_evaluation(self) -> None:
        """Test that generator uses lazy evaluation."""
        transactions = [
            {"description": "First"},
            {"description": "Second"},
            {"description": "Third"},
        ]
        gen = transaction_descriptions(transactions)
        # Generator should not evaluate immediately
        first = next(gen)
        assert first == "First"
        assert next(gen) == "Second"


class TestCardNumberGenerator:
    """Tests for card_number_generator function."""

    def test_card_number_generator_format(self) -> None:
        """Test that generated card numbers have correct format."""
        gen = card_number_generator(start=1, stop=3)
        for card in gen:
            assert len(card) == 19  # XXXX XXXX XXXX XXXX
            parts = card.split()
            assert len(parts) == 4
            assert all(len(part) == 4 for part in parts)
            assert all(part.isdigit() for part in parts)

    @pytest.mark.parametrize(
        "start, stop, expected_count",
        [
            (1, 1, 1),
            (1, 5, 5),
            (1000, 1010, 11),
            (9999999999999995, 9999999999999999, 5),
        ],
    )
    def test_card_number_generator_count(
        self, start: int, stop: int, expected_count: int
    ) -> None:
        """Test that correct number of cards are generated."""
        gen = card_number_generator(start=start, stop=stop)
        result = list(gen)
        assert len(result) == expected_count

    def test_card_number_generator_sequence(self) -> None:
        """Test that card numbers are generated in correct sequence."""
        gen = card_number_generator(start=1, stop=5)
        cards = list(gen)
        assert cards[0] == "0000 0000 0000 0001"
        assert cards[1] == "0000 0000 0000 0002"
        assert cards[4] == "0000 0000 0000 0005"

    def test_card_number_generator_large_numbers(self) -> None:
        """Test card generation with large numbers."""
        gen = card_number_generator(start=9999999999999998, stop=9999999999999999)
        cards = list(gen)
        assert len(cards) == 2
        assert cards[0] == "9999 9999 9999 9998"
        assert cards[1] == "9999 9999 9999 9999"

    def test_card_number_generator_default_parameters(self) -> None:
        """Test generator with default parameters."""
        gen = card_number_generator()
        first_card = next(gen)
        assert first_card == "0000 0000 0000 0001"

    def test_card_number_generator_invalid_start_too_low(self) -> None:
        """Test that error is raised for invalid start value."""
        with pytest.raises(ValueError, match="start must be between"):
            gen = card_number_generator(start=0, stop=100)
            next(gen)

    def test_card_number_generator_invalid_start_too_high(self) -> None:
        """Test that error is raised when start exceeds max."""
        with pytest.raises(ValueError, match="start must be between"):
            gen = card_number_generator(start=10000000000000000, stop=100)
            next(gen)

    def test_card_number_generator_invalid_stop_too_low(self) -> None:
        """Test that error is raised for invalid stop value."""
        with pytest.raises(ValueError, match="stop must be between"):
            gen = card_number_generator(start=1, stop=0)
            next(gen)

    def test_card_number_generator_invalid_stop_too_high(self) -> None:
        """Test that error is raised when stop exceeds max."""
        with pytest.raises(ValueError, match="stop must be between"):
            gen = card_number_generator(start=1, stop=10000000000000000)
            next(gen)

    def test_card_number_generator_start_greater_than_stop(self) -> None:
        """Test that error is raised when start > stop."""
        with pytest.raises(ValueError, match="start must be less than or equal"):
            gen = card_number_generator(start=100, stop=50)
            next(gen)

    def test_card_number_generator_returns_generator(self) -> None:
        """Test that function returns a generator."""
        gen = card_number_generator()
        assert hasattr(gen, "__iter__")
        assert hasattr(gen, "__next__")

    def test_card_number_generator_lazy_evaluation(self) -> None:
        """Test that generator uses lazy evaluation."""
        gen = card_number_generator(start=1, stop=1000000)
        # Should not raise error even though range is large
        first = next(gen)
        assert first == "0000 0000 0000 0001"
        second = next(gen)
        assert second == "0000 0000 0000 0002"

    def test_card_number_generator_leading_zeros(self) -> None:
        """Test that card numbers have proper leading zeros."""
        gen = card_number_generator(start=1, stop=1000)
        cards = list(gen)
        # Check first card has leading zeros
        assert cards[0].startswith("0000 0000 0000")
        # Check card at position 999
        assert cards[99].startswith("0000 0000 0000")
        # Check last card
        assert cards[-1] == "0000 0000 0000 1000"
