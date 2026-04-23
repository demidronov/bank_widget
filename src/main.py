"""Main module for bank transaction processing application."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .processing import filter_by_state, sort_by_date, process_bank_search
from .widget import get_date, mask_account_card


def load_json_data(filename: str) -> list[dict[str, Any]]:
    """Load transaction data from a JSON file.

    Args:
        filename: Path to the JSON file.

    Returns:
        List of transaction dictionaries.
    """
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def load_csv_data(filename: str) -> list[dict[str, Any]]:
    """Load transaction data from a CSV file.

    Args:
        filename: Path to the CSV file.

    Returns:
        List of transaction dictionaries.
    """
    data = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader and reader.fieldnames:
            for row in reader:
                data.append(row)
    return data


def load_xlsx_data(filename: str) -> list[dict[str, Any]]:
    """Load transaction data from an XLSX file.

    Args:
        filename: Path to the XLSX file.

    Returns:
        List of transaction dictionaries.

    Note:
        Requires openpyxl package to be installed.
    """
    try:
        import openpyxl
    except ImportError:
        raise ImportError(
            "openpyxl is required to load XLSX files. "
            "Install it with: pip install openpyxl"
        )

    workbook = openpyxl.load_workbook(filename)
    sheet = workbook.active
    if not sheet:
        return []

    data = []
    headers = None

    for row_idx, row in enumerate(sheet.iter_rows(values_only=True), 1):
        if row_idx == 1:
            headers = list(row)
        else:
            if headers and any(cell is not None for cell in row):
                data.append(dict(zip(headers, row)))

    return data


def format_transaction(transaction: dict[str, Any]) -> str:
    """Format a single transaction for display.

    Args:
        transaction: Transaction dictionary.

    Returns:
        Formatted string representation of the transaction.
    """
    date_str = transaction.get("date", "")
    description = transaction.get("description", "")
    from_to = transaction.get("from", "") or transaction.get("operationAmount", {})
    amount = transaction.get("operationAmount", {})

    # Format date
    formatted_date = get_date(date_str) if date_str else "N/A"

    # Get formatted amount
    if isinstance(amount, dict):
        amount_value = amount.get("amount", "0")
        currency = amount.get("currency", {}).get("code", "")
    else:
        amount_value = amount
        currency = transaction.get("currency", {}).get("code", "") if isinstance(
            transaction.get("currency"), dict
        ) else ""

    # Get from/to information
    from_account = transaction.get("from", "")
    to_account = transaction.get("to", "")

    if from_account and to_account:
        # Mask the accounts/cards
        from_masked = mask_account_card(from_account) if from_account else ""
        to_masked = mask_account_card(to_account) if to_account else ""
        from_to_str = f"{from_masked} -> {to_masked}"
    else:
        from_to_str = from_account if from_account else ""

    result = f"{formatted_date} {description}\n"
    if from_to_str:
        result += f"{from_to_str}\n"
    result += f"Сумма: {amount_value} {currency}.\n"

    return result


def display_transactions(transactions: list[dict[str, Any]]) -> None:
    """Display formatted transactions.

    Args:
        transactions: List of transaction dictionaries to display.
    """
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(transactions)}\n")
    for transaction in transactions:
        print(format_transaction(transaction))


def get_valid_status() -> str:
    """Prompt user for a valid transaction status.

    Returns:
        Uppercase status string (EXECUTED, CANCELED, or PENDING).
    """
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]

    while True:
        user_input = input(
            "Введите статус, по которому необходимо выполнить фильтрацию. "
            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
        )
        status = user_input.strip().upper()

        if status in valid_statuses:
            return status
        else:
            print(f'Статус операции "{user_input}" недоступен.\n')


def get_yes_no_input(prompt: str) -> bool:
    """Prompt user for a yes/no answer.

    Args:
        prompt: Prompt text to display.

    Returns:
        True if user answers yes (да), False if no (нет).
    """
    while True:
        response = input(prompt).strip().lower()
        if response in ["да", "yes", "y", "д"]:
            return True
        elif response in ["нет", "no", "n", "н"]:
            return False
        else:
            print("Пожалуйста, ответьте 'да' или 'нет'.\n")


def get_sort_direction() -> bool:
    """Prompt user for sort direction.

    Returns:
        True for descending (убывание), False for ascending (возрастание).
    """
    while True:
        response = input(
            "Отсортировать по возрастанию или по убыванию?\n"
        ).strip().lower()

        if response in [
            "возрастанию",
            "ascending",
            "asc",
            "по возрастанию",
            "возрастание",
        ]:
            return False
        elif response in [
            "убыванию",
            "descending",
            "desc",
            "по убыванию",
            "убывание",
        ]:
            return True
        else:
            print(
                "Пожалуйста, ответьте 'по возрастанию' или 'по убыванию'.\n"
            )


def main() -> None:
    """Main entry point for the bank transaction processing application."""
    print(
        "Привет! Добро пожаловать в программу работы с банковскими транзакциями."
    )
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла\n")

    file_choice = input("Выбор: ").strip()

    # Determine file type and load data
    if file_choice == "1":
        print("Для обработки выбран JSON-файл.\n")
        filename = input("Введите путь к JSON-файлу: ").strip()
        try:
            data = load_json_data(filename)
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
            return
        except json.JSONDecodeError:
            print(f"Ошибка при чтении JSON-файла {filename}.")
            return

    elif file_choice == "2":
        print("Для обработки выбран CSV-файл.\n")
        filename = input("Введите путь к CSV-файлу: ").strip()
        try:
            data = load_csv_data(filename)
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
            return
        except Exception as e:
            print(f"Ошибка при чтении CSV-файла: {e}")
            return

    elif file_choice == "3":
        print("Для обработки выбран XLSX-файл.\n")
        filename = input("Введите путь к XLSX-файлу: ").strip()
        try:
            data = load_xlsx_data(filename)
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
            return
        except Exception as e:
            print(f"Ошибка при чтении XLSX-файла: {e}")
            return

    else:
        print("Неверный выбор.")
        return

    if not data:
        print("Файл пуст или не содержит данных.")
        return

    # Filter by status
    print()
    status = get_valid_status()
    print(f'Операции отфильтрованы по статусу "{status}"\n')

    filtered_data = filter_by_state(data, status)

    if not filtered_data:
        print("Не найдено транзакций со статусом:", status)
        return

    # Ask about sorting by date
    if get_yes_no_input("Отсортировать операции по дате? Да/Нет\n"):
        descending = get_sort_direction()
        filtered_data = sort_by_date(filtered_data, descending=descending)
        print()

    # Ask about filtering by currency (RUB only)
    if get_yes_no_input("Выводить только рублевые транзакции? Да/Нет\n"):
        filtered_data = [
            op for op in filtered_data
            if (isinstance(op.get("operationAmount"), dict) and
                op.get("operationAmount", {}).get("currency", {}).get("code") == "RUB") or
               (op.get("currency") == "RUB")
        ]
        print()

    # Ask about filtering by description
    if get_yes_no_input(
        "Отфильтровать список транзакций по определенному слову "
        "в описании? Да/Нет\n"
    ):
        search_word = input("Введите слово для поиска: ").strip()
        filtered_data = process_bank_search(filtered_data, search_word)
        print()

    # Display results
    print("Распечатываю итоговый список транзакций...\n")
    display_transactions(filtered_data)


if __name__ == "__main__":
    main()
