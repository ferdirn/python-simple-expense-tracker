import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Optional

DATA_FILE = "expenses.json"
TABLE_WIDTH = 70
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


@dataclass
class Expense:
    id: int
    amount: float
    category: str
    description: str
    date: str

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        return cls(**data)

    def to_dict(self) -> dict:
        return asdict(self)


class ExpenseTracker:
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file

    def load(self) -> list[Expense]:
        """Return all expenses from the data file, or [] if it does not exist."""
        if not os.path.exists(self.data_file):
            return []
        with open(self.data_file, "r") as f:
            return [Expense.from_dict(e) for e in json.load(f)]

    def save(self, expenses: list[Expense]) -> None:
        """Persist the expenses list to the data file as formatted JSON."""
        with open(self.data_file, "w") as f:
            json.dump([e.to_dict() for e in expenses], f, indent=2)

    def add(self, amount: float, category: str, description: str) -> Expense:
        """Append a new expense with an auto-incremented id and current timestamp."""
        expenses = self.load()
        expense = Expense(
            id=len(expenses) + 1,
            amount=float(amount),
            category=category,
            description=description,
            date=datetime.now().strftime(DATE_FORMAT),
        )
        expenses.append(expense)
        self.save(expenses)
        return expense

    def get_all(self) -> list[Expense]:
        return self.load()

    def total(self, category: Optional[str] = None) -> float:
        """Return total spending, optionally filtered to a single category."""
        expenses = self.load()
        if category:
            expenses = [e for e in expenses if e.category.lower() == category.lower()]
        return sum(e.amount for e in expenses)


def _format_table(expenses: list[Expense]) -> str:
    lines = [
        f"\n{'ID':<5} {'Date':<20} {'Category':<15} {'Amount':>10}  Description",
        "-" * TABLE_WIDTH,
    ]
    for e in expenses:
        lines.append(
            f"{e.id:<5} {e.date:<20} {e.category:<15} ${e.amount:>9.2f}  {e.description}"
        )
    lines.append("")
    return "\n".join(lines)


def _prompt_amount() -> Optional[float]:
    try:
        return float(input("Amount: $"))
    except ValueError:
        print("Invalid amount.")
        return None


def run_cli(tracker: ExpenseTracker) -> None:
    """Run the interactive CLI loop until the user exits."""
    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Total spending")
        print("4. Total by category")
        print("5. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            amount = _prompt_amount()
            if amount is None:
                continue
            category = input("Category (e.g. Food, Transport, Entertainment): ").strip()
            description = input("Description: ").strip()
            expense = tracker.add(amount, category, description)
            print(f"Added expense: {expense.description} (${expense.amount:.2f}) in '{expense.category}'")

        elif choice == "2":
            expenses = tracker.get_all()
            if not expenses:
                print("No expenses found.")
            else:
                print(_format_table(expenses))

        elif choice == "3":
            print(f"Total spending: ${tracker.total():.2f}")

        elif choice == "4":
            category = input("Category: ").strip()
            print(f"Total spending in '{category}': ${tracker.total(category):.2f}")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    run_cli(ExpenseTracker())
