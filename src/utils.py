"""Utilities for loading and processing financial transactions."""

import json
from pathlib import Path
from typing import Any, List


def load_transactions(file_path: str) -> List[dict[str, Any]]:
    """
    Load financial transactions from a JSON file.

    Args:
        file_path: Path to the JSON file containing transactions

    Returns:
        List of transaction dictionaries. Returns empty list if:
        - File does not exist
        - File is empty
        - File content is not a list
        - JSON parsing fails
    """
    try:
        path = Path(file_path)

        # Check if file exists
        if not path.exists():
            return []

        # Read and parse JSON
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # Check if file is empty
        if not content:
            return []

        data = json.loads(content)

        # Check if content is a list
        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, IOError, OSError):
        return []
