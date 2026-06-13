from task_manager.validation import validate_task_title, validate_task_description, validate_due_date

tasks = []

def add_task(title, description, due_date):
    if not validate_task_title(title):
        return "Invalid title"
    if not validate_task_description(description):
        return "Invalid description"
    if not validate_due_date(due_date):
        return "Invalid due date"
    task = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": False
    }
    tasks.append(task)
    return "Task added successfully"

def mark_task_as_complete(title):
    for task in tasks:
        if task["title"] == title:
            task["completed"] = True
            return "Task marked as complete"
    return "Task not found"

def view_pending_tasks():
    pending = []
    for task in tasks:
        if task["completed"] == False:
            pending.append(task)
    return pending

def calculate_progress():
    if len(tasks) == 0:
        return 0
    completed = 0
    for task in tasks:
        if task["completed"] == True:
            completed += 1
    return (completed / len(tasks)) * 100