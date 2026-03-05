"""Utilities for loading and processing financial transactions."""

import json
from pathlib import Path
from typing import Any, List

from .logging_config import setup_logger

logger = setup_logger(__name__)


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
    logger.info(f"Started loading transactions from {file_path}")
    
    try:
        path = Path(file_path)

        # Check if file exists
        if not path.exists():
            logger.warning(f"File does not exist: {file_path}")
            return []

        # Read and parse JSON
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()

        # Check if file is empty
        if not content:
            logger.warning(f"File is empty: {file_path}")
            return []

        data = json.loads(content)

        # Check if content is a list
        if not isinstance(data, list):
            logger.error(f"File content is not a list: {file_path}")
            return []

        logger.info(f"Successfully loaded {len(data)} transactions from {file_path}")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error in {file_path}: {e}")
        return []
    except (IOError, OSError) as e:
        logger.error(f"File I/O error reading {file_path}: {e}")
        return []
