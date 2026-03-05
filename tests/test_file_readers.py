"""Tests for the file_readers module."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.file_readers import read_transactions_from_csv, read_transactions_from_xlsx


class TestReadTransactionsFromCsv:
    """Tests for read_transactions_from_csv function."""

    def test_read_csv_with_valid_file(self) -> None:
        """Test reading CSV file with valid data."""
        mock_data = [
            {"id": 1, "amount": 100, "currency": "USD"},
            {"id": 2, "amount": 150, "currency": "EUR"},
        ]

        with patch("pandas.read_csv") as mock_read_csv:
            mock_df = MagicMock()
            mock_df.empty = False
            mock_df.to_dict.return_value = mock_data
            mock_read_csv.return_value = mock_df

            with patch("pathlib.Path.exists", return_value=True):
                result = read_transactions_from_csv("test.csv")

            assert result == mock_data
            mock_read_csv.assert_called_once()
            mock_df.to_dict.assert_called_once_with(orient="records")

    def test_read_csv_file_not_found(self) -> None:
        """Test reading CSV when file does not exist."""
        with patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(FileNotFoundError, match="CSV file not found"):
                read_transactions_from_csv("nonexistent.csv")

    def test_read_csv_empty_file(self) -> None:
        """Test reading empty CSV file."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pandas.read_csv") as mock_read_csv:
                mock_df = MagicMock()
                mock_df.empty = True
                mock_read_csv.return_value = mock_df

                with pytest.raises(ValueError, match="CSV file is empty"):
                    read_transactions_from_csv("empty.csv")

    def test_read_csv_parser_error(self) -> None:
        """Test reading CSV with parser error."""
        import pandas as pd

        with patch("pathlib.Path.exists", return_value=True):
            with patch("pandas.read_csv") as mock_read_csv:
                mock_read_csv.side_effect = pd.errors.ParserError(
                    "Invalid CSV format"
                )

                with pytest.raises(pd.errors.ParserError):
                    read_transactions_from_csv("invalid.csv")

    def test_read_csv_general_error(self) -> None:
        """Test reading CSV with general exception."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pandas.read_csv") as mock_read_csv:
                mock_read_csv.side_effect = OSError("Disk read error")

                with pytest.raises(ValueError, match="Failed to read CSV file"):
                    read_transactions_from_csv("corrupted.csv")

    def test_read_csv_with_path_object(self) -> None:
        """Test reading CSV with Path object instead of string."""
        mock_data = [{"id": 1, "amount": 100}]

        with patch("pathlib.Path.exists", return_value=True):
            with patch("pandas.read_csv") as mock_read_csv:
                mock_df = MagicMock()
                mock_df.empty = False
                mock_df.to_dict.return_value = mock_data
                mock_read_csv.return_value = mock_df

                result = read_transactions_from_csv(Path("test.csv"))

                assert result == mock_data
                mock_read_csv.assert_called_once()

    def test_read_csv_multiple_rows(self) -> None:
        """Test reading CSV with multiple transaction rows."""
        mock_data = [
            {"id": 1, "amount": 100, "currency": "USD", "description": "Payment"},
            {"id": 2, "amount": 150, "currency": "EUR", "description": "Refund"},
            {"id": 3, "amount": 200, "currency": "GBP", "description": "Transfer"},
        ]

        with patch("pathlib.Path.exists", return_value=True):
            with patch("pandas.read_csv") as mock_read_csv:
                mock_df = MagicMock()
                mock_df.empty = False
                mock_df.to_dict.return_value = mock_data
                mock_read_csv.return_value = mock_df

                result = read_transactions_from_csv("transactions.csv")

                assert len(result) == 3
                assert result[0]["id"] == 1
                assert result[2]["currency"] == "GBP"


class TestReadTransactionsFromXlsx:
    """Tests for read_transactions_from_xlsx function."""

    def test_read_xlsx_with_valid_file(self) -> None:
        """Test reading XLSX file with valid data."""
        mock_data = [
            {"id": 1, "amount": 100, "currency": "USD"},
            {"id": 2, "amount": 150, "currency": "EUR"},
        ]

        with patch("pathlib.Path.exists", return_value=True):
            with patch("pandas.read_excel") as mock_read_excel:
                mock_df = MagicMock()
                mock_df.empty = False
                mock_df.to_dict.return_value = mock_data
                mock_read_excel.return_value = mock_df

                result = read_transactions_from_xlsx("test.xlsx")

                assert result == mock_data
                mock_read_excel.assert_called_once_with(
                    Path("test.xlsx"), engine="openpyxl"
                )
                mock_df.to_dict.assert_called_once_with(orient="records")

    def test_read_xlsx_file_not_found(self) -> None:
        """Test reading XLSX when file does not exist."""
        with patch("pathlib.Path.exists", return_value=False):
            with pytest.raises(FileNotFoundError, match="XLSX file not found"):
                read_transactions_from_xlsx("nonexistent.xlsx")

    def test_read_xlsx_empty_file(self) -> None:
        """Test reading empty XLSX file."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pandas.read_excel") as mock_read_excel:
                mock_df = MagicMock()
                mock_df.empty = True
                mock_read_excel.return_value = mock_df

                with pytest.raises(ValueError, match="XLSX file is empty"):
                    read_transactions_from_xlsx("empty.xlsx")

    def test_read_xlsx_invalid_format(self) -> None:
        """Test reading XLSX with invalid format."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pandas.read_excel") as mock_read_excel:
                mock_read_excel.side_effect = ValueError("Invalid XLSX format")

                with pytest.raises(ValueError, match="Failed to read XLSX file"):
                    read_transactions_from_xlsx("invalid.xlsx")

    def test_read_xlsx_general_error(self) -> None:
        """Test reading XLSX with general exception."""
        with patch("pathlib.Path.exists", return_value=True):
            with patch("pandas.read_excel") as mock_read_excel:
                mock_read_excel.side_effect = OSError("Disk read error")

                with pytest.raises(ValueError, match="Failed to read XLSX file"):
                    read_transactions_from_xlsx("corrupted.xlsx")

    def test_read_xlsx_with_path_object(self) -> None:
        """Test reading XLSX with Path object instead of string."""
        mock_data = [{"id": 1, "amount": 100}]

        with patch("pathlib.Path.exists", return_value=True):
            with patch("pandas.read_excel") as mock_read_excel:
                mock_df = MagicMock()
                mock_df.empty = False
                mock_df.to_dict.return_value = mock_data
                mock_read_excel.return_value = mock_df

                result = read_transactions_from_xlsx(Path("test.xlsx"))

                assert result == mock_data
                mock_read_excel.assert_called_once()

    def test_read_xlsx_multiple_rows(self) -> None:
        """Test reading XLSX with multiple transaction rows."""
        mock_data = [
            {"id": 1, "amount": 100, "currency": "USD", "description": "Payment"},
            {"id": 2, "amount": 150, "currency": "EUR", "description": "Refund"},
            {"id": 3, "amount": 200, "currency": "GBP", "description": "Transfer"},
            {"id": 4, "amount": 250, "currency": "JPY", "description": "Deposit"},
        ]

        with patch("pathlib.Path.exists", return_value=True):
            with patch("pandas.read_excel") as mock_read_excel:
                mock_df = MagicMock()
                mock_df.empty = False
                mock_df.to_dict.return_value = mock_data
                mock_read_excel.return_value = mock_df

                result = read_transactions_from_xlsx("transactions.xlsx")

                assert len(result) == 4
                assert result[0]["id"] == 1
                assert result[3]["currency"] == "JPY"

    def test_read_xlsx_uses_openpyxl_engine(self) -> None:
        """Test that read_xlsx uses openpyxl engine."""
        mock_data = [{"id": 1}]

        with patch("pathlib.Path.exists", return_value=True):
            with patch("pandas.read_excel") as mock_read_excel:
                mock_df = MagicMock()
                mock_df.empty = False
                mock_df.to_dict.return_value = mock_data
                mock_read_excel.return_value = mock_df

                read_transactions_from_xlsx("test.xlsx")

                # Check that engine parameter is passed
                call_args = mock_read_excel.call_args
                assert call_args[1]["engine"] == "openpyxl"
