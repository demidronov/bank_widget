"""Utility functions for masking card and account numbers.

These helpers are intended for use in widgets and other presentation
layers where full card or account numbers must not be exposed.
"""

from __future__ import annotations

from .logging_config import setup_logger

logger = setup_logger(__name__)


def get_mask_card_number(card_number: str) -> str:
    """Return a masked representation of a bank card number.

    The function keeps the first 6 and last 4 digits visible and masks
    the middle part. The output is formatted in groups for readability.

    Example:
        >>> get_mask_card_number("7000792289606362")
        '7000 79** **** 6362'

    If the input does not contain at least 16 digits, the original
    string is returned unchanged.
    """
    logger.info("Started masking card number")
    
    digits = "".join(ch for ch in card_number if ch.isdigit())
    if len(digits) < 16:
        logger.warning(f"Card number has insufficient digits (found {len(digits)}, need 16). Returning original.")
        return card_number

    first_four = digits[:4]
    next_two = digits[4:6]
    last_four = digits[-4:]
    
    result = f"{first_four} {next_two}** **** {last_four}"
    logger.debug(f"Card number masked successfully. Result: {result}")
    
    return result


def get_mask_account(account_number: str) -> str:
    """Return a masked representation of a bank account number.

    The function hides all digits except the last four and prefixes
    the result with two asterisks.

    Example:
        >>> get_mask_account("40817810099910004312")
        '**4312'

    If the input does not contain at least 4 digits, the original
    string is returned unchanged.
    """
    logger.info("Started masking account number")
    
    digits = "".join(ch for ch in account_number if ch.isdigit())
    if len(digits) < 4:
        logger.warning(f"Account number has insufficient digits (found {len(digits)}, need 4). Returning original.")
        return account_number

    result = f"**{digits[-4:]}"
    logger.debug(f"Account number masked successfully. Result: {result}")
    
    return result
