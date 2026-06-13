import builtins

import pytest

import task_manager.task_utils as task_utils


@pytest.fixture(autouse=True)
def reset_tasks():
    task_utils.tasks.clear()
    yield
    task_utils.tasks.clear()


def test_add_task_success_appends_task():
    result = task_utils.add_task("Write tests", "Add pytest coverage", "2026-06-13")

    assert result == "Task added successfully!"
    assert task_utils.tasks == [
        {
            "title": "Write tests",
            "description": "Add pytest coverage",
            "due_date": "2026-06-13",
            "completed": False,
        }
    ]


def test_add_task_returns_invalid_title():
    result = task_utils.add_task("", "Description", "2026-06-13")

    assert result == "Invalid title"
    assert task_utils.tasks == []


def test_add_task_returns_invalid_description():
    result = task_utils.add_task("Write tests", "", "2026-06-13")

    assert result == "Invalid description"
    assert task_utils.tasks == []


def test_add_task_returns_invalid_due_date():
    result = task_utils.add_task("Write tests", "Description", "13-06-2026")

    assert result == "Invalid due date"
    assert task_utils.tasks == []


def test_add_task_returns_invalid_description_for_too_long_description():
    result = task_utils.add_task("Write tests", "x" * 501, "2026-06-13")

    assert result == "Invalid description"
    assert task_utils.tasks == []


def test_add_task_does_not_append_invalid_task():
    task_utils.add_task("", "Description", "2026-06-13")

    assert task_utils.tasks == []


def test_mark_task_as_complete_by_title_marks_matching_task():
    task_utils.tasks.append(
        {"title": "Write tests", "description": "Add pytest coverage", "due_date": "2026-06-13", "completed": False}
    )

    result = task_utils.mark_task_as_complete("Write tests")

    assert result == "Task marked as complete!"
    assert task_utils.tasks[0]["completed"] is True


def test_mark_task_as_complete_by_one_based_index_marks_matching_task():
    task_utils.tasks.append(
        {"title": "Write tests", "description": "Add pytest coverage", "due_date": "2026-06-13", "completed": False}
    )

    result = task_utils.mark_task_as_complete(1)

    assert result == "Task marked as complete!"
    assert task_utils.tasks[0]["completed"] is True


def test_mark_task_as_complete_by_numeric_string_one_based_index_marks_matching_task():
    task_utils.tasks.append(
        {"title": "Write tests", "description": "Add pytest coverage", "due_date": "2026-06-13", "completed": False}
    )

    result = task_utils.mark_task_as_complete("1")

    assert result == "Task marked as complete!"
    assert task_utils.tasks[0]["completed"] is True


def test_mark_task_as_complete_missing_title_returns_task_not_found():
    result = task_utils.mark_task_as_complete("Missing task")

    assert result == "Task not found"


def test_mark_task_as_complete_negative_index_returns_task_not_found():
    result = task_utils.mark_task_as_complete(-1)

    assert result == "Task not found"


def test_mark_task_as_complete_out_of_range_index_returns_task_not_found():
    result = task_utils.mark_task_as_complete(5)

    assert result == "Task not found"


def test_view_pending_tasks_returns_only_pending_tasks():
    task_utils.tasks.extend(
        [
            {"title": "Complete", "description": "Done", "due_date": "2026-06-13", "completed": True},
            {"title": "Pending", "description": "Open", "due_date": "2026-06-14", "completed": False},
        ]
    )

    assert task_utils.view_pending_tasks() == [task_utils.tasks[1]]


def test_view_pending_tasks_returns_empty_list_when_all_tasks_complete():
    task_utils.tasks.append(
        {"title": "Complete", "description": "Done", "due_date": "2026-06-13", "completed": True}
    )

    assert task_utils.view_pending_tasks() == []


def test_view_pending_tasks_returns_original_task_dicts():
    task_utils.tasks.append(
        {"title": "Pending", "description": "Open", "due_date": "2026-06-13", "completed": False}
    )

    pending_tasks = task_utils.view_pending_tasks()

    assert pending_tasks[0] is task_utils.tasks[0]


def test_calculate_progress_empty_tasks_returns_zero():
    assert task_utils.calculate_progress() == 0.0


def test_calculate_progress_all_pending_returns_zero():
    task_utils.tasks.extend(
        [
            {"title": "One", "description": "Open", "due_date": "2026-06-13", "completed": False},
            {"title": "Two", "description": "Open", "due_date": "2026-06-14", "completed": False},
        ]
    )

    assert task_utils.calculate_progress() == 0.0


def test_calculate_progress_all_complete_returns_hundred():
    task_utils.tasks.extend(
        [
            {"title": "One", "description": "Done", "due_date": "2026-06-13", "completed": True},
            {"title": "Two", "description": "Done", "due_date": "2026-06-14", "completed": True},
        ]
    )

    assert task_utils.calculate_progress() == 100.0


def test_calculate_progress_half_complete_returns_fifty():
    task_utils.tasks.extend(
        [
            {"title": "One", "description": "Done", "due_date": "2026-06-13", "completed": True},
            {"title": "Two", "description": "Open", "due_date": "2026-06-14", "completed": False},
        ]
    )

    assert task_utils.calculate_progress() == 50.0


def test_calculate_progress_uses_explicit_task_list():
    tasks = [
        {"title": "One", "description": "Done", "due_date": "2026-06-13", "completed": True},
        {"title": "Two", "description": "Open", "due_date": "2026-06-14", "completed": False},
        {"title": "Three", "description": "Open", "due_date": "2026-06-15", "completed": False},
    ]

    assert task_utils.calculate_progress(tasks) == pytest.approx(33.3333333333)


def test_add_task_preserves_completed_false():
    task_utils.add_task("Write tests", "Add pytest coverage", "2026-06-13")

    assert task_utils.tasks[0]["completed"] is False


def test_add_task_accepts_whitespace_title():
    result = task_utils.add_task("  Write tests  ", "Description", "2026-06-13")

    assert result == "Task added successfully!"
    assert task_utils.tasks[0]["title"] == "  Write tests  "


def test_add_task_accepts_whitespace_description():
    result = task_utils.add_task("Write tests", "  Description  ", "2026-06-13")

    assert result == "Task added successfully!"
    assert task_utils.tasks[0]["description"] == "  Description  "


def test_add_task_stores_due_date_exactly():
    task_utils.add_task("Write tests", "Description", "2026-06-13")

    assert task_utils.tasks[0]["due_date"] == "2026-06-13"


def test_add_task_no_args_prompts_and_adds_task(monkeypatch):
    responses = iter(["Prompted title", "Prompted description", "2026-06-13"])
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))

    result = task_utils.add_task()

    assert result == "Task added successfully!"
    assert task_utils.tasks[0]["title"] == "Prompted title"
