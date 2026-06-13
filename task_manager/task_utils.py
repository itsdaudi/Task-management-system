from task_manager.validation import validate_task_title, validate_task_description, validate_due_date

tasks = []


def _is_valid(validation_result):
    if isinstance(validation_result, tuple):
        return validation_result[0]
    return bool(validation_result)


def add_task(title=None, description=None, due_date=None):
    if title is None:
        title = input("Enter task title: ")
    if description is None:
        description = input("Enter task description: ")
    if due_date is None:
        due_date = input("Enter due date (YYYY-MM-DD): ")

    try:
        title_valid = _is_valid(validate_task_title(title))
        description_valid = _is_valid(validate_task_description(description))
        due_date_valid = _is_valid(validate_due_date(due_date))
    except ValueError as error:
        message = str(error)
        if "description" in message:
            return "Invalid description"
        return "Invalid due date"

    if not title_valid:
        return "Invalid title"
    if not description_valid:
        return "Invalid description"
    if not due_date_valid:
        return "Invalid due date"

    task = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": False,
    }
    tasks.append(task)
    return "Task added successfully!"


def mark_task_as_complete(identifier):
    for task in tasks:
        if task["title"] == identifier:
            task["completed"] = True
            return "Task marked as complete!"

    if isinstance(identifier, int):
        index = identifier - 1
        if 0 <= index < len(tasks):
            tasks[index]["completed"] = True
            return "Task marked as complete!"

    if isinstance(identifier, str) and identifier.isdigit():
        index = int(identifier) - 1
        if 0 <= index < len(tasks):
            tasks[index]["completed"] = True
            return "Task marked as complete!"

    return "Task not found"


def view_pending_tasks():
    return [task for task in tasks if not task["completed"]]


def calculate_progress(tasks_param=None):
    if tasks_param is None:
        tasks_param = tasks
    if not tasks_param:
        return 0.0
    completed = sum(1 for task in tasks_param if task["completed"])
    return (completed / len(tasks_param)) * 100
