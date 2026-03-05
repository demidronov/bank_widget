"""Functions for reading financial transactions from CSV and XLSX files."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import pandas as pd

__all__ = ["read_transactions_from_csv", "read_transactions_from_xlsx"]


def read_transactions_from_csv(file_path: str | Path) -> list[dict[str, Any]]:
    """Read financial transactions from a CSV file.

    Accepts a path to a CSV file and reads financial transaction data
    from it. Returns a list of dictionaries where each dictionary represents
    a single transaction with its associated data.

    Args:
        file_path: Path to the CSV file containing transaction data.

    Returns:
        A list of dictionaries, where each dictionary represents a transaction
        with keys as column names from the CSV file and values as transaction data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the file is empty or not a valid CSV file.
        pd.errors.ParserError: If the CSV file cannot be parsed properly.

    Example:
        >>> transactions = read_transactions_from_csv("transactions.csv")
        >>> print(transactions)
        [
            {"id": 1, "amount": 100, "currency": "USD", "description": "Payment"},
            {"id": 2, "amount": 150, "currency": "EUR", "description": "Refund"},
        ]
    """
    file_path_obj = Path(file_path)

    if not file_path_obj.exists():
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    try:
        df = pd.read_csv(file_path_obj)
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Failed to parse CSV file: {file_path}") from e
    except Exception as e:
        raise ValueError(f"Failed to read CSV file: {file_path}") from e

    if df.empty:
        raise ValueError("CSV file is empty")

    return cast(list[dict[str, Any]], df.to_dict(orient="records"))


def read_transactions_from_xlsx(file_path: str | Path) -> list[dict[str, Any]]:
    """Read financial transactions from an Excel file.

    Accepts a path to an Excel file and reads financial transaction data
    from it. Returns a list of dictionaries where each dictionary represents
    a single transaction with its associated data.

    Args:
        file_path: Path to the XLSX file containing transaction data.

    Returns:
        A list of dictionaries, where each dictionary represents a transaction
        with keys as column names from the Excel file and values as transaction
        data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the file is empty or not a valid XLSX file.
        openpyxl.utils.exceptions.InvalidFileException: If the file format is
            invalid.

    Example:
        >>> transactions = read_transactions_from_xlsx("transactions.xlsx")
        >>> print(transactions)
        [
            {"id": 1, "amount": 100, "currency": "USD", "description": "Payment"},
            {"id": 2, "amount": 150, "currency": "EUR", "description": "Refund"},
        ]
    """
    file_path_obj = Path(file_path)

    if not file_path_obj.exists():
        raise FileNotFoundError(f"XLSX file not found: {file_path}")

    try:
        df = pd.read_excel(file_path_obj, engine="openpyxl")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"XLSX file not found: {file_path}") from e
    except Exception as e:
        raise ValueError(f"Failed to read XLSX file: {file_path}") from e

    if df.empty:
        raise ValueError("XLSX file is empty")

    return cast(list[dict[str, Any]], df.to_dict(orient="records"))
