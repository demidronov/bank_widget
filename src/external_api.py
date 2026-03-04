"""External API integrations for currency conversion."""

import os
from typing import Any

import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_URL = "https://api.apilayer.com/exchangerates_data/latest"


def get_exchange_rate(currency_code: str, target_currency: str = "RUB") -> float | None:
    """
    Get exchange rate from currency_code to target_currency.

    Args:
        currency_code: Source currency code (e.g., 'USD', 'EUR')
        target_currency: Target currency code (default: 'RUB')

    Returns:
        Exchange rate as float, or None if API call fails
    """
    api_key = os.getenv("EXCHANGE_RATES_API_KEY", "")
    if not api_key:
        return None

    try:
        headers = {"apikey": api_key}
        params = {"base": currency_code, "symbols": target_currency}

        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("success", False) and "rates" in data:
            return float(data["rates"].get(target_currency, 1.0))

        return None

    except (requests.RequestException, ValueError, KeyError):
        return None


def convert_to_rub(transaction: dict[str, Any]) -> float:
    """
    Convert transaction amount to Russian rubles.

    Args:
        transaction: Transaction dictionary with operationAmount field

    Returns:
        Amount in RUB as float

    Raises:
        KeyError: If transaction doesn't have required fields
    """
    amount_str = transaction["operationAmount"]["amount"]
    currency_code = transaction["operationAmount"]["currency"]["code"]
    amount = float(amount_str)

    # If already in RUB, return as is
    if currency_code == "RUB":
        return amount

    # For USD and EUR, get exchange rate and convert
    if currency_code in ("USD", "EUR"):
        rate = get_exchange_rate(currency_code, "RUB")
        if rate is not None:
            return amount * rate

    # If conversion fails or currency not supported, return original amount
    return amount
