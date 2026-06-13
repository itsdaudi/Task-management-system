from datetime import datetime
import re


def validate_task_title(title):
    if len(title.strip()) == 0:
        return False, "Task title cannot be empty."
    return True, ""


def validate_task_description(description):
    if len(description.strip()) == 0:
        return False, "Task description cannot be empty."
    if len(description) > 500:
        raise ValueError("Task description cannot exceed 500 characters.")
    return True, ""


def validate_due_date(due_date):
    if len(due_date.strip()) == 0:
        return False, "Due date cannot be empty."
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", due_date):
        raise ValueError("Due date must be in YYYY-MM-DD format.")
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
        return True, ""
    except ValueError:
        raise ValueError("Due date must be in YYYY-MM-DD format.")
