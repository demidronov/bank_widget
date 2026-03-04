"""Test script to verify logging functionality."""

# Import the modules with logging
from src.masks import get_mask_card_number, get_mask_account
from src.utils import load_transactions
from pathlib import Path

# Test masks module
print("Testing masks module:")
print(f"  Card mask: {get_mask_card_number('7000792289606362')}")
print(f"  Account mask: {get_mask_account('40817810099910004312')}")
print(f"  Invalid card: {get_mask_card_number('123')}")

# Test utils module
print("\nTesting utils module:")
operations_file = Path(__file__).parent / "data" / "operations.json"
transactions = load_transactions(str(operations_file))
print(f"  Loaded {len(transactions)} transactions")

print("\nCheck the logs directory for generated log files.")
