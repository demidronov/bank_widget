"""Tests for utils module."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from typing import Any

import pytest

from src.utils import load_transactions


@pytest.fixture
def sample_transactions() -> list[dict[str, Any]]:
    """Fixture providing sample transaction data."""
    return [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {
                "amount": "31957.58",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {
                "amount": "8221.37",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
    ]


class TestLoadTransactions:
    """Test cases for load_transactions function."""

    def test_load_valid_json_file(
        self, sample_transactions: list[dict[str, Any]]
    ) -> None:
        """Test loading a valid JSON file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(sample_transactions, f)
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert result == sample_transactions
            assert len(result) == 2
        finally:
            Path(temp_path).unlink()

    def test_load_nonexistent_file(self) -> None:
        """Test loading a non-existent file returns empty list."""
        result = load_transactions("/nonexistent/path/to/file.json")
        assert result == []

    def test_load_empty_file(self) -> None:
        """Test loading an empty file returns empty list."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert result == []
        finally:
            Path(temp_path).unlink()

    def test_load_non_list_content(self) -> None:
        """Test loading JSON that is not a list returns empty list."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump({"key": "value"}, f)
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert result == []
        finally:
            Path(temp_path).unlink()

    def test_load_invalid_json(self) -> None:
        """Test loading invalid JSON returns empty list."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write("{invalid json content")
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert result == []
        finally:
            Path(temp_path).unlink()

    def test_load_empty_list(self) -> None:
        """Test loading a valid JSON with empty list."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump([], f)
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert result == []
        finally:
            Path(temp_path).unlink()

    def test_load_file_with_whitespace(
        self, sample_transactions: list[dict[str, Any]]
    ) -> None:
        """Test loading a file with whitespace."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            f.write("   \n\t")
            f.write(json.dumps(sample_transactions))
            temp_path = f.name

        try:
            result = load_transactions(temp_path)
            assert result == sample_transactions
        finally:
            Path(temp_path).unlink()
