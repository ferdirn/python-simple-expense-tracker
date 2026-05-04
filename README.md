# Expense Tracker

A lightweight CLI application for tracking personal expenses. Data is persisted locally in a JSON file, so no database setup is required.

## Installation

No external dependencies are needed for the main application. To run the test suite, install pytest:

```bash
pip install pytest
```

## Usage

Run the interactive menu:

```bash
python expense_tracker.py
```

You will be presented with a menu:

```
=== Expense Tracker ===
1. Add expense
2. View all expenses
3. Total spending
4. Total by category
5. Exit
```

### Adding an Expense

Select option `1`, then provide:
- **Amount** — a positive number (e.g. `25.50`)
- **Category** — a label such as `Food`, `Transport`, or `Entertainment`
- **Description** — a short note (e.g. `Lunch at the office`)

### Viewing Expenses

Select option `2` to display all recorded expenses in a table:

```
ID    Date                 Category        Amount  Description
----------------------------------------------------------------------
1     2026-04-30 17:42:58  Food             $10.00  Buy a bread
2     2026-04-30 17:43:34  Transport        $25.00  Taxi to SCBD
```

### Totals

- Option `3` — overall total across all expenses.
- Option `4` — total for a specific category (case-insensitive match).

## Data Storage

Expenses are stored in `expenses.json` in the working directory. Each record has the following shape:

```json
{
  "id": 1,
  "amount": 10.0,
  "category": "Food",
  "description": "Buy a bread",
  "date": "2026-04-30 17:42:58"
}
```

## API Reference

The application is built around the `ExpenseTracker` class.

### `ExpenseTracker(data_file="expenses.json")`

Creates a tracker instance. Pass a custom `data_file` path to use a different storage location (useful for testing).

### `tracker.load() -> list[Expense]`

Reads all expenses from the data file. Returns an empty list if the file does not exist.

### `tracker.save(expenses: list[Expense]) -> None`

Persists the given list of `Expense` objects to the data file as formatted JSON.

### `tracker.add(amount, category, description) -> Expense`

Creates a new expense with an auto-incremented `id` and the current timestamp, appends it to the store, and returns the new `Expense`.

**Example:**
```python
from expense_tracker import ExpenseTracker

tracker = ExpenseTracker()
expense = tracker.add(12.50, "Food", "Coffee and muffin")
print(f"Added: {expense.description} (${expense.amount:.2f})")
# Added: Coffee and muffin ($12.50)
```

### `tracker.get_all() -> list[Expense]`

Returns all stored expenses.

### `tracker.total(category=None) -> float`

Returns the total amount spent. When `category` is provided, only expenses whose category matches (case-insensitive) are summed.

**Example:**
```python
tracker.total()           # 35.00
tracker.total("Food")     # 10.00
```

### `ExpenseCLI(tracker)`

Wraps `ExpenseTracker` in an interactive menu-driven interface.

```python
from expense_tracker import ExpenseCLI, ExpenseTracker

ExpenseCLI(ExpenseTracker()).run()
```

#### `cli.run() -> None`

Starts the interactive CLI loop until the user selects **Exit**.

## Running Tests

```bash
pytest test_expense_tracker.py -v
```

Tests use a temporary file via pytest's `tmp_path` fixture so they never touch the real `expenses.json`.

## License

MIT
