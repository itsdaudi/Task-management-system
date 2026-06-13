from task_manager.task_utils import add_task, mark_task_as_complete, view_pending_tasks, calculate_progress

def main():
    while True:
        print("\n--- Task Manager ---")
        print("1. Add Task")
        print("2. Mark Task as Complete")
        print("3. View Pending Tasks")
        print("4. Calculate Progress")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            print(add_task(title, description, due_date))

        elif choice == "2":
            title = input("Enter task title to mark complete: ")
            print(mark_task_as_complete(title))

        elif choice == "3":
            pending = view_pending_tasks()
            if len(pending) == 0:
                print("No pending tasks!")
            else:
                for task in pending:
                    print(f"- {task['title']} | {task['due_date']}")

        elif choice == "4":
            print(f"Progress: {calculate_progress():.1f}%")

        elif choice == "5":
            print("Goodbye!")
            break

main()