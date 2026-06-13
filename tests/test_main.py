import builtins

import main as main_module


def reset_tasks():
    main_module.tasks.clear()


def test_main_prints_menu_and_exits(monkeypatch, capsys):
    reset_tasks()
    monkeypatch.setattr(builtins, "input", lambda _: "5")

    main_module.main()

    output = capsys.readouterr().out
    assert "--- Task Manager ---" in output
    assert "1. Add Task" in output
    assert "2. Mark Task as Complete" in output
    assert "3. View Pending Tasks" in output
    assert "4. Calculate Progress" in output
    assert "5. Exit" in output


def test_main_exits_with_goodbye_message(monkeypatch, capsys):
    reset_tasks()
    monkeypatch.setattr(builtins, "input", lambda _: "5")

    main_module.main()

    assert "Goodbye!" in capsys.readouterr().out


def test_main_invalid_choice_prints_message(monkeypatch, capsys):
    reset_tasks()
    responses = iter(["9", "5"])
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))

    main_module.main()

    assert "Invalid choice. Please enter 1-5." in capsys.readouterr().out


def test_main_choice_1_prompts_task_fields_and_adds_task(monkeypatch, capsys):
    reset_tasks()
    responses = iter(["1", "Task 1", "This is a check", "2024-05-24", "5"])
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))

    main_module.main()

    assert main_module.tasks == [
        {"title": "Task 1", "description": "This is a check", "due_date": "2024-05-24", "completed": False}
    ]
    assert "Task added successfully!" in capsys.readouterr().out


def test_main_choice_2_marks_task_by_one_based_index(monkeypatch, capsys):
    reset_tasks()
    main_module.tasks.append({"title": "Task 1", "description": "This is a check", "due_date": "2024-05-24", "completed": False})
    responses = iter(["2", "1", "5"])
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))

    main_module.main()

    assert main_module.tasks[0]["completed"] is True
    assert "Task marked as complete!" in capsys.readouterr().out


def test_main_choice_2_marks_task_by_title(monkeypatch, capsys):
    reset_tasks()
    main_module.tasks.append({"title": "Task 1", "description": "This is a check", "due_date": "2024-05-24", "completed": False})
    responses = iter(["2", "Task 1", "5"])
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))

    main_module.main()

    assert main_module.tasks[0]["completed"] is True
    assert "Task marked as complete!" in capsys.readouterr().out


def test_main_choice_2_missing_task_prints_not_found(monkeypatch, capsys):
    reset_tasks()
    responses = iter(["2", "Missing task", "5"])
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))

    main_module.main()

    assert "Task not found" in capsys.readouterr().out


def test_main_choice_3_no_pending_prints_no_pending_tasks(monkeypatch, capsys):
    reset_tasks()
    responses = iter(["3", "5"])
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))

    main_module.main()

    assert "No pending tasks" in capsys.readouterr().out


def test_main_choice_3_prints_pending_tasks(monkeypatch, capsys):
    reset_tasks()
    main_module.tasks.append({"title": "Task 1", "description": "This is a check", "due_date": "2024-05-24", "completed": False})
    responses = iter(["3", "5"])
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))

    main_module.main()

    assert "- Task 1 | 2024-05-24" in capsys.readouterr().out


def test_main_choice_4_prints_progress_with_one_decimal(monkeypatch, capsys):
    reset_tasks()
    main_module.tasks.extend(
        [
            {"title": "Task 1", "description": "Done", "due_date": "2024-05-24", "completed": True},
            {"title": "Task 2", "description": "Open", "due_date": "2024-05-25", "completed": False},
        ]
    )
    responses = iter(["4", "5"])
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))

    main_module.main()

    assert "50.0" in capsys.readouterr().out


def test_main_invalid_choice_before_exit_is_handled(monkeypatch, capsys):
    reset_tasks()
    responses = iter(["6", "5"])
    monkeypatch.setattr(builtins, "input", lambda _: next(responses))

    main_module.main()

    output = capsys.readouterr().out
    assert "Invalid choice. Please enter 1-5." in output
    assert "Goodbye!" in output


def test_main_input_prompt_for_choice_is_correct(monkeypatch):
    reset_tasks()
    prompts = []
    responses = iter(["5"])
    monkeypatch.setattr(builtins, "input", lambda prompt: prompts.append(prompt) or next(responses))

    main_module.main()

    assert prompts[0] == "Choose an option: "
