# Expense Tracker

A lightweight CLI application for tracking personal expenses. Data is persisted locally in a JSON file — no database or internet connection required.

## Features

- Add expenses with amount, category, and description
- View all expenses in a formatted table
- Calculate total spending across all categories
- Calculate total spending within a specific category (case-insensitive)
- Auto-incremented IDs and automatic timestamping
- Zero external runtime dependencies

## Installation

### Prerequisites

- Python 3.10 or later (uses `list[...]` generics without `from __future__ import annotations`)

### Setup

Clone or download the project, then enter its directory:

```bash
git clone <repo-url>
cd expense-tracker
```

No pip install step is needed to run the app. To run the test suite, install pytest:

```bash
pip install pytest
```

### Run the app

```bash
python expense_tracker.py
```

### Run the tests

```bash
pytest test_expense_tracker.py -v
```

## Usage

Launch the interactive menu:

```bash
python expense_tracker.py
```

```
=== Expense Tracker ===
1. Add expense
2. View all expenses
3. Total spending
4. Total by category
5. Exit
```

### Adding an expense

Select option `1`, then provide:

- **Amount** — a positive number (e.g. `25.50`)
- **Category** — a label such as `Food`, `Transport`, or `Entertainment`
- **Description** — a short note (e.g. `Lunch at the office`)

```
Choose an option: 1
Amount: $25.50
Category (e.g. Food, Transport, Entertainment): Food
Description: Lunch at the office
Added expense: Lunch at the office ($25.50) in 'Food'
```

### Viewing expenses

Select option `2` to display all recorded expenses in a table:

```
ID    Date                 Category              Amount  Description
----------------------------------------------------------------------
1     2026-05-04 09:12:00  Food                  $25.50  Lunch at the office
2     2026-05-04 10:45:00  Transport             $15.00  Taxi to airport
```

### Checking totals

- **Option `3`** — overall total across all expenses
- **Option `4`** — total for a specific category (case-insensitive)

```
Choose an option: 4
Category: food
Total spending in 'food': $25.50
```

## Data Storage

Expenses are saved to `expenses.json` in the working directory. Each record has the following shape:

```json
{
  "id": 1,
  "amount": 25.50,
  "category": "Food",
  "description": "Lunch at the office",
  "date": "2026-05-04 09:12:00"
}
```

The file is created automatically on first use and is human-readable formatted JSON.

## API Reference

### `Expense`

Dataclass representing a single expense entry.

| Field | Type | Description |
|-------|------|-------------|
| `id` | `int` | Auto-incremented unique identifier |
| `amount` | `float` | Expense amount in dollars |
| `category` | `str` | Category label (e.g. `Food`, `Transport`) |
| `description` | `str` | Short free-text note |
| `date` | `str` | Timestamp in `YYYY-MM-DD HH:MM:SS` format |

#### `Expense.from_dict(data: dict) -> Expense`

Construct an `Expense` from a plain dictionary (used when loading from JSON).

#### `expense.to_dict() -> dict`

Serialize the expense to a plain dictionary (used when saving to JSON).

---

### `ExpenseTracker(data_file="expenses.json")`

Manages persistence and querying of expenses stored in a JSON file. Pass a custom `data_file` path to use a different storage location — useful for testing.

```python
from expense_tracker import ExpenseTracker

tracker = ExpenseTracker()                          # default: expenses.json
tracker = ExpenseTracker(data_file="/tmp/test.json") # custom path
```

#### `tracker.add(amount, category, description) -> Expense`

Append a new expense with an auto-incremented `id` and current timestamp, then return it.

**Parameters:**
- `amount` (`float`): Dollar amount
- `category` (`str`): Category label
- `description` (`str`): Short note

**Returns:** the newly created `Expense`

**Example:**
```python
expense = tracker.add(12.50, "Food", "Coffee and muffin")
print(f"Added: {expense.description} (${expense.amount:.2f})")
# Added: Coffee and muffin ($12.50)
```

#### `tracker.get_all() -> list[Expense]`

Return all stored expenses. Returns an empty list if no data file exists yet.

```python
expenses = tracker.get_all()
for e in expenses:
    print(e.id, e.category, e.amount)
```

#### `tracker.total(category=None) -> float`

Return the total amount spent. When `category` is provided, only expenses whose category matches (case-insensitive) are summed.

**Parameters:**
- `category` (`str`, optional): Filter to a single category

**Returns:** `float` total

**Example:**
```python
tracker.total()          # 40.50  (all categories)
tracker.total("Food")    # 12.50  (Food only)
tracker.total("food")    # 12.50  (case-insensitive)
```

#### `tracker.load() -> list[Expense]`

Read and deserialize all expenses from the data file. Returns `[]` if the file does not exist.

#### `tracker.save(expenses: list[Expense]) -> None`

Persist the given list of `Expense` objects to the data file as formatted JSON, overwriting any previous contents.

---

### `ExpenseCLI(tracker)`

Interactive menu-driven command-line interface wrapping an `ExpenseTracker`.

```python
from expense_tracker import ExpenseCLI, ExpenseTracker

ExpenseCLI(ExpenseTracker()).run()
```

#### `cli.run() -> None`

Start the interactive loop, presenting the menu on each iteration until the user selects **Exit** (option `5`).

## Contributing

1. Fork the repository and create a feature branch.
2. Write tests for any new behaviour in `test_expense_tracker.py`.
3. Ensure the full test suite passes: `pytest test_expense_tracker.py -v`
4. Open a pull request with a clear description of the change.

## License

MIT
