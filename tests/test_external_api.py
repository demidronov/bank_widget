"""Tests for external_api module."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from src.external_api import convert_to_rub, get_exchange_rate


class TestGetExchangeRate:
    """Test cases for get_exchange_rate function."""

    @patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "test_api_key"})
    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_success(
        self, mock_get: MagicMock
    ) -> None:
        """Test successful exchange rate retrieval."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "rates": {"RUB": 85.5},
        }
        mock_get.return_value = mock_response

        result = get_exchange_rate("USD", "RUB")

        assert result == 85.5
        mock_get.assert_called_once()

    @patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "test_api_key"})
    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_eur(self, mock_get: MagicMock) -> None:
        """Test EUR to RUB exchange rate."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "rates": {"RUB": 93.5},
        }
        mock_get.return_value = mock_response

        result = get_exchange_rate("EUR", "RUB")

        assert result == 93.5

    @patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": ""})
    def test_get_exchange_rate_no_api_key(self) -> None:
        """Test that None is returned when API key is missing."""
        result = get_exchange_rate("USD", "RUB")
        assert result is None

    @patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "test_api_key"})
    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_api_failure(self, mock_get: MagicMock) -> None:
        """Test handling of API failure."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": False}
        mock_get.return_value = mock_response

        result = get_exchange_rate("USD", "RUB")

        assert result is None

    @patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "test_api_key"})
    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_request_exception(
        self, mock_get: MagicMock
    ) -> None:
        """Test handling of request exception."""
        import requests

        mock_get.side_effect = requests.RequestException("Connection error")

        result = get_exchange_rate("USD", "RUB")

        assert result is None

    @patch.dict("os.environ", {"EXCHANGE_RATES_API_KEY": "test_api_key"})
    @patch("src.external_api.requests.get")
    def test_get_exchange_rate_missing_rate(self, mock_get: MagicMock) -> None:
        """Test handling when requested currency is not in response."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "rates": {},
        }
        mock_get.return_value = mock_response

        result = get_exchange_rate("USD", "RUB")

        assert result == 1.0  # Default value when rate not found


class TestConvertToRub:
    """Test cases for convert_to_rub function."""

    def test_convert_rub_currency(self) -> None:
        """Test conversion of RUB currency (should return as is)."""
        transaction: dict[str, Any] = {
            "operationAmount": {
                "amount": "1000.50",
                "currency": {"name": "руб.", "code": "RUB"},
            }
        }

        result = convert_to_rub(transaction)

        assert result == 1000.5

    @patch("src.external_api.get_exchange_rate")
    def test_convert_usd_to_rub(self, mock_rate: MagicMock) -> None:
        """Test conversion of USD to RUB."""
        mock_rate.return_value = 85.5

        transaction: dict[str, Any] = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "USD", "code": "USD"},
            }
        }

        result = convert_to_rub(transaction)

        assert result == 8550.0
        mock_rate.assert_called_once_with("USD", "RUB")

    @patch("src.external_api.get_exchange_rate")
    def test_convert_eur_to_rub(self, mock_rate: MagicMock) -> None:
        """Test conversion of EUR to RUB."""
        mock_rate.return_value = 93.5

        transaction: dict[str, Any] = {
            "operationAmount": {
                "amount": "50.00",
                "currency": {"name": "EUR", "code": "EUR"},
            }
        }

        result = convert_to_rub(transaction)

        assert result == 4675.0
        mock_rate.assert_called_once_with("EUR", "RUB")

    @patch("src.external_api.get_exchange_rate")
    def test_convert_usd_api_failure(self, mock_rate: MagicMock) -> None:
        """Test USD conversion when API fails (should return original amount)."""
        mock_rate.return_value = None

        transaction: dict[str, Any] = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "USD", "code": "USD"},
            }
        }

        result = convert_to_rub(transaction)

        assert result == 100.0

    @patch("src.external_api.get_exchange_rate")
    def test_convert_unsupported_currency(self, mock_rate: MagicMock) -> None:
        """Test conversion of unsupported currency (should return original amount)."""
        transaction: dict[str, Any] = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {"name": "GBP", "code": "GBP"},
            }
        }

        result = convert_to_rub(transaction)

        assert result == 100.0
        # get_exchange_rate should not be called for unsupported currencies
        mock_rate.assert_not_called()

    def test_convert_missing_amount_field(self) -> None:
        """Test conversion with missing amount field raises KeyError."""
        transaction: dict[str, Any] = {
            "operationAmount": {
                "currency": {"name": "USD", "code": "USD"},
            }
        }

        with pytest.raises(KeyError):
            convert_to_rub(transaction)

    def test_convert_missing_currency_field(self) -> None:
        """Test conversion with missing currency field raises KeyError."""
        transaction: dict[str, Any] = {
            "operationAmount": {
                "amount": "100.00",
            }
        }

        with pytest.raises(KeyError):
            convert_to_rub(transaction)

    @patch("src.external_api.get_exchange_rate")
    def test_convert_complex_amount(self, mock_rate: MagicMock) -> None:
        """Test conversion with complex amount string."""
        mock_rate.return_value = 85.5

        transaction: dict[str, Any] = {
            "operationAmount": {
                "amount": "8221.37",
                "currency": {"name": "USD", "code": "USD"},
            }
        }

        result = convert_to_rub(transaction)

        assert result == pytest.approx(702927.135)
