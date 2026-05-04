import pytest
from expense_tracker import Expense, ExpenseTracker, _format_table


@pytest.fixture
def tracker(tmp_path) -> ExpenseTracker:
    """Provide an ExpenseTracker backed by a temporary file that is cleaned up after each test."""
    return ExpenseTracker(data_file=str(tmp_path / "expenses.json"))


def test_load_expenses_empty(tracker: ExpenseTracker):
    """get_all returns an empty list when no data file exists."""
    assert tracker.get_all() == []


def test_add_and_load_expense(tracker: ExpenseTracker):
    """add persists amount, category, and description correctly."""
    tracker.add(25.50, "Food", "Lunch")
    expenses = tracker.get_all()
    assert len(expenses) == 1
    assert expenses[0].amount == 25.50
    assert expenses[0].category == "Food"
    assert expenses[0].description == "Lunch"


def test_total_spending(tracker: ExpenseTracker):
    """total returns the sum of all expenses."""
    tracker.add(10.0, "Food", "Coffee")
    tracker.add(20.0, "Transport", "Bus")
    assert tracker.total() == 30.0


def test_total_spending_by_category(tracker: ExpenseTracker):
    """total filters correctly when a category is provided."""
    tracker.add(10.0, "Food", "Coffee")
    tracker.add(20.0, "Transport", "Bus")
    assert tracker.total("Food") == 10.0


def test_view_expenses_empty(tracker: ExpenseTracker):
    """get_all returns an empty list, which the CLI treats as 'no expenses'."""
    assert tracker.get_all() == []


def test_view_expenses_table_output(tracker: ExpenseTracker, capsys):
    """_format_table includes expense data in its output."""
    tracker.add(12.50, "Food", "Lunch")
    expenses = tracker.get_all()
    print(_format_table(expenses))
    captured = capsys.readouterr()
    assert "Food" in captured.out
    assert "12.50" in captured.out
    assert "Lunch" in captured.out


def test_ids_are_sequential(tracker: ExpenseTracker):
    """Each new expense receives an id one greater than the previous."""
    tracker.add(5.0, "Food", "Snack")
    tracker.add(15.0, "Food", "Dinner")
    expenses = tracker.get_all()
    assert expenses[0].id == 1
    assert expenses[1].id == 2
