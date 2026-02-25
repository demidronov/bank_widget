"""Functions for preparing data for the client banking widget."""

from __future__ import annotations

from datetime import datetime

from .masks import get_mask_account, get_mask_card_number

__all__ = ["mask_account_card", "get_date"]


def mask_account_card(description: str) -> str:
    """Mask card or account number in a one-line description.

    The function accepts a single string that contains a human-readable
    name and a number, for example:

    - "Visa Platinum 7000792289606361"
    - "Maestro 7000792289606361"
    - "Account 73654108430135874305"

    The string is not split into separate arguments; instead, the
    function extracts the last "word" as a number and decides whether
    it is a card or an account based on the text prefix.
    Returns:
        The original description with the number masked, using the
        appropriate masking function for cards or accounts.
    """

    parts = description.split()
    if len(parts) < 2:
        return description

    number = parts[-1]
    prefix = " ".join(parts[:-1])

    # If description starts with "Account" or "Счет", treat it as a bank account.
    if prefix.lower().startswith("account") or prefix.lower().startswith("счет"):
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{prefix} {masked_number}"


def get_date(date_str: str) -> str:
    """Convert an ISO-like datetime string to DD.MM.YYYY format.

    Example:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
    """

    dt = datetime.fromisoformat(date_str)
    formatted = dt.strftime("%d.%m.%Y")
    return formatted
