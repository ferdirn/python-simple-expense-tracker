"""Simple CLI expense tracker that persists data to a JSON file."""

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
    """Represents a single expense entry."""

    id: int
    amount: float
    category: str
    description: str
    date: str

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """Construct an Expense from a plain dictionary."""
        return cls(**data)

    def to_dict(self) -> dict:
        """Serialize the expense to a plain dictionary."""
        return asdict(self)


class ExpenseTracker:
    """Manages persistence and querying of expenses stored in a JSON file."""

    def __init__(self, data_file: str = DATA_FILE):
        """Initialize the tracker with the path to the JSON storage file."""
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
        """Return all stored expenses."""
        return self.load()

    def total(self, category: Optional[str] = None) -> float:
        """Return total spending, optionally filtered to a single category."""
        expenses = self.load()
        if category:
            expenses = [e for e in expenses if e.category.lower() == category.lower()]
        return sum(e.amount for e in expenses)


class ExpenseCLI:
    """Interactive command-line interface for the expense tracker."""

    MENU = (
        "\n=== Expense Tracker ===",
        "1. Add expense",
        "2. View all expenses",
        "3. Total spending",
        "4. Total by category",
        "5. Exit",
    )

    def __init__(self, tracker: ExpenseTracker):
        """Initialize the CLI with an ExpenseTracker instance."""
        self.tracker = tracker

    def run(self) -> None:
        """Start the interactive CLI loop until the user exits."""
        while True:
            print("\n".join(self.MENU))
            choice = input("Choose an option: ").strip()
            handler = self._handlers().get(choice)
            if handler:
                handler()
            else:
                print("Invalid option. Please choose 1-5.")

    def _handlers(self) -> dict:
        """Return a mapping of menu-option strings to their handler callables."""
        return {
            "1": self._handle_add,
            "2": self._handle_view,
            "3": self._handle_total,
            "4": self._handle_total_by_category,
            "5": self._handle_exit,
        }

    def _handle_add(self) -> None:
        """Prompt for expense details and persist a new expense."""
        amount = self._prompt_amount()
        if amount is None:
            return
        category = input("Category (e.g. Food, Transport, Entertainment): ").strip()
        description = input("Description: ").strip()
        expense = self.tracker.add(amount, category, description)
        print(f"Added expense: {expense.description} (${expense.amount:.2f}) in '{expense.category}'")

    def _handle_view(self) -> None:
        """Print all expenses as a formatted table, or a 'no expenses' message."""
        expenses = self.tracker.get_all()
        if not expenses:
            print("No expenses found.")
        else:
            print(self._format_table(expenses))

    def _handle_total(self) -> None:
        """Print the overall total spending across all categories."""
        print(f"Total spending: ${self.tracker.total():.2f}")

    def _handle_total_by_category(self) -> None:
        """Prompt for a category and print total spending within it."""
        category = input("Category: ").strip()
        print(f"Total spending in '{category}': ${self.tracker.total(category):.2f}")

    def _handle_exit(self) -> None:
        """Print a farewell message and exit the process."""
        print("Goodbye!")
        raise SystemExit(0)

    @staticmethod
    def _format_table(expenses: list[Expense]) -> str:
        """Render a list of expenses as a formatted table string."""
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

    @staticmethod
    def _prompt_amount() -> Optional[float]:
        """Prompt the user for an amount and return it, or None on invalid input."""
        try:
            return float(input("Amount: $"))
        except ValueError:
            print("Invalid amount.")
            return None


# Keep module-level helpers for backwards compatibility with existing tests
def _format_table(expenses: list[Expense]) -> str:
    """Backwards-compatible shim delegating to ExpenseCLI._format_table."""
    return ExpenseCLI._format_table(expenses)


if __name__ == "__main__":
    ExpenseCLI(ExpenseTracker()).run()
