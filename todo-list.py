import json
from prompt_toolkit import prompt

# Load tasks from JSON file
with open('tasks.json', 'r') as file:
    tasks = json.load(file)

# Define menu options for the application
options = [
    "1. Add a task",
    "2. View tasks",
    "3. Update a task",
    "4. Delete a task",
    "5. Exit"
]

# Define possible statuses for tasks
statuses = ["Pending", "Completed"]

# Welcome message
print("\n==============================")
print("Welcome to the TO-DO list app!")
print("==============================")

# Main loop for app
def main():

    while True:
        print("\nPlease, choose an option:")
        for option in options:
            print(option)

        choice = input("> ") # user choise

        if choice == "1":
            add()
        elif choice == "2":
            view()
        elif choice == "3":
            update()
        elif choice == "4":
            delete()
        elif choice == "5":
            print("\nThanks for using the TO-DO list app!")
            break
        else:
            print("\nInvalid choice. Please choose again.")

def get_task_status():
    # Get task status from user with validation
    while True:
        print("Choose a status")

        for i, status in enumerate(statuses, 1):
            print(f"{i}. {status}")

        task_status = input("> ")
        if task_status == "0":
            return None
        elif task_status == "1":
            return "Pending"
        elif task_status == "2":
            return "Completed"
        else:
            print("\nInvalid choice. Please choose 1 or 2.")

# Add new task
def add():
    # Create new task
    new_task = {}
    new_task["id"] = len(tasks) + 1 

    # Get task description from user with validation
    while True:
        print("\nAdd new task or type 0 to return to previous menu:")
        task_description = input("> ")
        # Return to main menu
        if task_description == "0":
            return 
        if len(task_description) > 0:
            new_task["description"] = task_description
            break
        else:
            print("\nTask description cannot be empty! Please try again.")

    # Get task status from user
    task_status = get_task_status()
    if task_status is None:
        print("\nTask was not added due to incomplete information.")
        return
    new_task["status"] = task_status
        
    # Save task to json file if all required fields are completed
    if "description" in new_task and "status" in new_task:
        tasks.append(new_task)
        try:
            with open('tasks.json', 'w') as file:
                json.dump(tasks, file, indent=4)
            print("\nTask successfully added!")

        except Exception as e:
            print(f"\nError saving task: {e}")
            tasks.remove(new_task) # Remove task if saving failed
    else:
        print("\nTask was not added due to incomplete information.")        

# View all tasks
def view():
    # Check if tasks exist
    if not tasks:
        print("\nYou don't have tasks")
        return
    # Print tasks 
    else:
        print("\n=================")
        print("Your TO-DO list: ")
        print("=================")      
        for task in tasks:
            print(f"{task['id']}. {task['description']} \n   Status: {task['status']}") 

# Update an existing task
def update():
    global tasks
    # Check if tasks exist
    if not tasks:
        print("\nNo tasks to update!")
        return
    # Get task number to update
    print("\nChoose a task number for updating or type 0 to return to previous menu:")

    # Validate task ID input
    while True:
        task_id = input("> ")
        if task_id == "0":
            return
        
        try: 
            task_id = int(task_id)
        except ValueError:
            print("Please enter a valid number!")
            continue

        # Check if task exists
        if not any(task['id'] == task_id for task in tasks):
            print(f"Task number {task_id} not found! Please try again.")
            continue

        # Get task to update from user
        updating_task = next((task for task in tasks if task['id'] == task_id))
        temp_task = updating_task.copy()  # Create a copy to store temporary changes

        # Update task description using prompt_toolkit
        while True:
            new_description = prompt("Edit description: ", default=updating_task["description"])
            if len(new_description) > 0:
                temp_task["description"] = new_description
                break
            else:
                print("\nTask description cannot be empty! Please try again.")

        # Update task status
        task_status = get_task_status()
        if task_status is None:
            print("\nTask was not updated due to incomplete information.")
            return
            
        temp_task["status"] = task_status

        # Save updated task to json file
        if "description" in updating_task and "status" in updating_task:
            try:
                updating_task.update(temp_task)
                with open('tasks.json', 'w') as file:
                    json.dump(tasks, file, indent=4)
                    print("\nTask successfully adupdated!")

            except Exception as e:
                print(f"\nError saving task: {e}")
        else:
            print("\nTask was not added due to incomplete information.")

        break
        
        
# Delete a task and reorder tasks id's
def delete():
    global tasks

    # Check if tasks exist
    if not tasks:
        print("\nNo tasks to delete!")
        return
    
    # Get task number to delete from user
    print("\nChoose a task number for deleting or type 0 to return to previous menu:")

    # Validate task ID input
    while True:
        task_id = input("> ")
        if task_id == "0":
            return
        
        try: 
            task_id = int(task_id)
        except ValueError:
            print("Please enter a valid number!")
            continue
        # Check if task exists
        if not any(task['id'] == task_id for task in tasks):
            print(f"Task number {task_id} not found! Please try again.")
            continue

        # Delete task and check if deletion was successful
        original_length = len(tasks)
        tasks = list(filter(lambda task: task['id'] != task_id, tasks))

        if len(tasks) == original_length:
                    print("Failed to delete task!")
                    continue
        # Reorder task id's            
        for index, task in enumerate(tasks, 1):
                task['id'] = index

        # Save updated task list to json file
        try:
            with open('tasks.json', 'w') as file:
                json.dump(tasks, file, indent=4)
            print("\nTask successfully deleted!")
        except Exception as e:
            print(f"Error saving to file: {e}")
        break

# Start the application
main()                