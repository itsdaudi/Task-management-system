# task_manager.py

tasks = []


def add_task():
    """Add a new task"""
    title = input("Enter task title: ")
    description = input("Enter task description: ")
    due_date = input("Enter due date (YYYY-MM-DD): ")

    task = {
        "title": title,
        "description": description,
        "due_date": due_date,
        "completed": False,
    }
    tasks.append(task)
    print("Task added successfully!")


def mark_complete():
    """Mark a task as complete"""
    identifier = input("Enter task title to mark complete: ")

    for index, task in enumerate(tasks):
        if task["title"] == identifier or (
            identifier.isdigit() and int(identifier) - 1 == index
        ):
            task["completed"] = True
            print("Task marked as complete!")
            return

    print("Task not found")


def view_pending():
    """View all pending tasks"""
    pending_tasks = [task for task in tasks if not task["completed"]]

    if not pending_tasks:
        print("No pending tasks")
    else:
        for task in pending_tasks:
            print(f"- {task['title']} | {task['due_date']}")


def calculate_progress(tasks_param=None):
    """Calculate completion progress"""
    if tasks_param is None:
        tasks_param = tasks

    if not tasks_param:
        return 0.0

    completed = sum(1 for task in tasks_param if task["completed"])
    percentage = (completed / len(tasks_param)) * 100
    return percentage


def main():
    """Main program loop"""
    while True:
        print("\n--- Task Manager ---")
        print("1. Add Task")
        print("2. Mark Task as Complete")
        print("3. View Pending Tasks")
        print("4. Calculate Progress")
        print("5. Exit")

        try:
            choice = input("Choose an option: ")

            if choice == "1":
                add_task()
            elif choice == "2":
                mark_complete()
            elif choice == "3":
                view_pending()
            elif choice == "4":
                progress = calculate_progress()
                print(f"{progress:.1f}")
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1-5.")
        except ValueError:
            print("Please enter a valid number")
        except Exception as error:
            print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
