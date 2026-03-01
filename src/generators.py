"""Generators for working with transaction data.

This module provides generator functions for efficient processing of large
volumes of transaction data, allowing financial analysts to quickly find
and analyze transaction information.
"""

from __future__ import annotations

from typing import Any, Generator, Iterator


def filter_by_currency(
    transactions: list[dict[str, Any]], currency: str
) -> Iterator[dict[str, Any]]:
    """Filter transactions by currency.

    Args:
        transactions: List of transaction dictionaries.
        currency: Currency code to filter by (e.g., 'USD', 'EUR').

    Yields:
        Transaction dictionaries matching the specified currency.

    Example:
        >>> transactions = [
        ...     {"id": 1, "currency": "USD", "amount": 100},
        ...     {"id": 2, "currency": "EUR", "amount": 50},
        ...     {"id": 3, "currency": "USD", "amount": 200},
        ... ]
        >>> usd_transactions = list(filter_by_currency(transactions, "USD"))
        >>> len(usd_transactions)
        2
    """
    for transaction in transactions:
        if transaction.get("currency") == currency:
            yield transaction


def transaction_descriptions(
    transactions: list[dict[str, Any]],
) -> Generator[str, None, None]:
    """Generate descriptions for each transaction.

    Args:
        transactions: List of transaction dictionaries.

    Yields:
        Description string for each transaction.

    Example:
        >>> transactions = [
        ...     {"id": 1, "description": "Payment for services"},
        ...     {"id": 2, "description": "Refund"},
        ... ]
        >>> descriptions = list(transaction_descriptions(transactions))
        >>> descriptions[0]
        'Payment for services'
    """
    for transaction in transactions:
        description = transaction.get("description", "")
        if description:
            yield description


def card_number_generator(
    start: int = 1, stop: int = 9999999999999999
) -> Generator[str, None, None]:
    """Generate bank card numbers in the format XXXX XXXX XXXX XXXX.

    Generates card numbers in the range from start to stop (inclusive).
    Default range is from 0000 0000 0000 0001 to 9999 9999 9999 9999.

    Args:
        start: Starting card number (1 to 9999999999999999). Default: 1.
        stop: Ending card number (1 to 9999999999999999). Default: 9999999999999999.

    Yields:
        Card number strings formatted as XXXX XXXX XXXX XXXX.

    Raises:
        ValueError: If start or stop values are outside valid range.

    Example:
        >>> gen = card_number_generator(start=1, stop=5)
        >>> next(gen)
        '0000 0000 0000 0001'
        >>> next(gen)
        '0000 0000 0000 0002'
    """
    if not 1 <= start <= 9999999999999999:
        raise ValueError("start must be between 1 and 9999999999999999")
    if not 1 <= stop <= 9999999999999999:
        raise ValueError("stop must be between 1 and 9999999999999999")
    if start > stop:
        raise ValueError("start must be less than or equal to stop")

    for card_num in range(start, stop + 1):
        # Format card number as 16-digit string with leading zeros
        formatted = str(card_num).zfill(16)
        # Add spaces to create XXXX XXXX XXXX XXXX format
        card_string = f"{formatted[0:4]} {formatted[4:8]} {formatted[8:12]} {formatted[12:16]}"
        yield card_string
