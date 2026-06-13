import pytest

from task_manager.validation import (
    validate_due_date,
    validate_task_description,
    validate_task_title,
)


def test_validate_task_title_accepts_non_empty_title():
    assert validate_task_title("Write tests") == (True, "")


def test_validate_task_title_rejects_empty_title():
    assert validate_task_title("") == (False, "Task title cannot be empty.")


def test_validate_task_title_rejects_whitespace_title():
    assert validate_task_title("   ") == (False, "Task title cannot be empty.")


def test_validate_task_title_accepts_title_with_surrounding_spaces():
    assert validate_task_title("  Write tests  ") == (True, "")


def test_validate_task_title_accepts_single_character_title():
    assert validate_task_title("A") == (True, "")


def test_validate_task_title_accepts_unicode_title():
    assert validate_task_title("Tâche") == (True, "")


def test_validate_task_description_accepts_non_empty_description():
    assert validate_task_description("Finish the task") == (True, "")


def test_validate_task_description_rejects_empty_description():
    assert validate_task_description("") == (False, "Task description cannot be empty.")


def test_validate_task_description_rejects_whitespace_description():
    assert validate_task_description("   ") == (False, "Task description cannot be empty.")


def test_validate_task_description_accepts_description_with_surrounding_spaces():
    assert validate_task_description("  Finish the task  ") == (True, "")


def test_validate_task_description_accepts_500_character_description():
    assert validate_task_description("x" * 500) == (True, "")


def test_validate_task_description_rejects_description_over_500_characters():
    with pytest.raises(ValueError, match="cannot exceed 500 characters"):
        validate_task_description("x" * 501)


def test_validate_due_date_accepts_valid_date():
    assert validate_due_date("2026-06-13") == (True, "")


def test_validate_due_date_accepts_leap_year_date():
    assert validate_due_date("2024-02-29") == (True, "")


def test_validate_due_date_rejects_empty_date():
    assert validate_due_date("") == (False, "Due date cannot be empty.")


def test_validate_due_date_rejects_whitespace_date():
    assert validate_due_date("   ") == (False, "Due date cannot be empty.")


def test_validate_due_date_rejects_slash_separated_date():
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        validate_due_date("2026/06/13")


def test_validate_due_date_rejects_day_first_date():
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        validate_due_date("13-06-2026")


def test_validate_due_date_rejects_date_with_time():
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        validate_due_date("2026-06-13 10:00")


def test_validate_due_date_rejects_month_13():
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        validate_due_date("2026-13-13")


def test_validate_due_date_rejects_day_32():
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        validate_due_date("2026-06-32")


def test_validate_due_date_rejects_short_month():
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        validate_due_date("2026-6-13")


def test_validate_due_date_rejects_trailing_space():
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        validate_due_date("2026-06-13 ")


def test_validate_due_date_rejects_non_string_value():
    with pytest.raises(AttributeError):
        validate_due_date(None)
