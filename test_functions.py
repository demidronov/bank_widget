"""Test script to verify the new functions work correctly."""

from src.processing import process_bank_search, process_bank_operations

# Test data
test_data = [
    {
        "id": 1,
        "description": "Открытие вклада",
        "amount": 40542,
        "state": "EXECUTED"
    },
    {
        "id": 2,
        "description": "Перевод с карты на карту",
        "amount": 130,
        "state": "EXECUTED"
    },
    {
        "id": 3,
        "description": "Перевод организации",
        "amount": 8390,
        "state": "EXECUTED"
    },
    {
        "id": 4,
        "description": "Перевод со счета на счет",
        "amount": 8200,
        "state": "EXECUTED"
    },
    {
        "id": 5,
        "description": "Открытие счета",
        "amount": 5000,
        "state": "EXECUTED"
    }
]

# Test process_bank_search
print("=== Testing process_bank_search ===")
print("\nSearching for 'вклада':")
result1 = process_bank_search(test_data, "вклада")
print(f"Found {len(result1)} transactions:")
for r in result1:
    print(f"  - {r['description']}")

print("\nSearching for 'перевод' (case-insensitive):")
result2 = process_bank_search(test_data, "перевод")
print(f"Found {len(result2)} transactions:")
for r in result2:
    print(f"  - {r['description']}")

print("\nSearching for 'Открытие':")
result3 = process_bank_search(test_data, "Открытие")
print(f"Found {len(result3)} transactions:")
for r in result3:
    print(f"  - {r['description']}")

# Test process_bank_operations
print("\n\n=== Testing process_bank_operations ===")
categories = ["вклада", "перевод", "открытие"]
result4 = process_bank_operations(test_data, categories)
print(f"Categories: {result4}")

print("\nTest completed successfully!")
