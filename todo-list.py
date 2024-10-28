import json
from prompt_toolkit import prompt

with open('tasks.json', 'r') as file:
    tasks = json.load(file)
   # print("Data Read from JSON File:", file_data)

options = [
    "1. Add a task",
    "2. View tasks",
    "3. Update a task",
    "4. Delete a task",
    "5. Exit"
]

statuses = ["Pending", "Completed"]

print("\n==============================")
print("Welcome to the TO-DO list app!")
print("==============================")

# main loop for app
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

# adding new task
def add():
    # create new task
    new_task = {}
    new_task["id"] = len(tasks) + 1 

    # get description 
    while True:
        print("\nAdd new task or type 0 to return to previous menu:")
        task_description = input("> ")
        # return to main menu
        if task_description == "0":
            return 
        if len(task_description) > 0:
            new_task["description"] = task_description
            break
        else:
            print("\nTask description cannot be empty! Please try again.")

    # get status
    while True:
        print("Choose a status")

        for i, status in enumerate(statuses, 1):
            print(f"{i}. {status}")

        task_status = input("> ")
        
        if task_status == "1":
            new_task["status"] = "Pending"
            break
        elif task_status == "2":
            new_task["status"] = "Completed"
            break
        else:
            print("\nInvalid choice. Please choose 1 or 2.")

    # save task
    if "description" in new_task and "status" in new_task:
        tasks.append(new_task)
        try:
            with open('tasks.json', 'w') as file:
                json.dump(tasks, file, indent=4)
            print("\nTask successfully added!")

        except Exception as e:
            print(f"\nError saving task: {e}")
            tasks.remove(new_task)
    else:
        print("\nTask was not added due to incomplete information.")        

# view all tasks
def view():
    # check if tasks exist
    if not tasks:
        print("\nYou don't have tasks")
        return
     
    else:
        print("\nYour TO-DO list: ")
        for task in tasks:
            print(f"{task['id']}. {task['description']} \n   Status: {task['status']}") 

# updating task
def update():
    global tasks
    # check if tasks exist
    if not tasks:
        print("\nNo tasks to update!")
        return
    
    print("\nChoose a task number for updating or type 0 to return to previous menu:")

    # for task in tasks:
    #     print(f"{task['id']}. {task['description']} \n   Status: {task['status']}")

    while True:
        task_id = input("> ")
        if task_id == "0":
            return
        
        try: 
            task_id = int(task_id)
        except ValueError:
            print("Please enter a valid number!")
            continue

        if not any(task['id'] == task_id for task in tasks):
            print(f"Task number {task_id} not found! Please try again.")
            continue

        updating_task = next((task for task in tasks if task['id'] == task_id))

        while True:
            # prompt_toolkit for updating
            new_description = prompt("Edit description: ", default=updating_task["description"])
            if len(new_description) > 0:
                updating_task["description"] = new_description
                break
            else:
                print("\nTask description cannot be empty! Please try again.")

        while True:
            print("Choose a status")

            for i, status in enumerate(statuses, 1):
                print(f"{i}. {status}")

            task_status = input("> ")
            
            if task_status == "1":
                updating_task["status"] = "Pending"
                break
            elif task_status == "2":
                updating_task["status"] = "Completed"
                break
            else:
                print("\nInvalid choice. Please choose 1 or 2.")

        if "description" in updating_task and "status" in updating_task:
            try:
                with open('tasks.json', 'w') as file:
                    json.dump(tasks, file, indent=4)
                    print("\nTask successfully adupdated!")

            except Exception as e:
                print(f"\nError saving task: {e}")
        else:
            print("\nTask was not added due to incomplete information.")

        break
        
        

def delete():
    global tasks

    if not tasks:
        print("\nNo tasks to delete!")
        return
    
    print("\nChoose a task number for deleting or type 0 to return to previous menu:")
    # for task in tasks:
    #     print(f"{task['id']}. {task['description']} \n   Status: {task['status']}")
    
    while True:

        task_id = input("> ")
        if task_id == "0":
            return
        
        try: 
            task_id = int(task_id)
        except ValueError:
            print("Please enter a valid number!")
            continue

        # if task_id > len(tasks):
        #     print("Task with this number doesn't exist. Please try again.")
        #     continue

        if not any(task['id'] == task_id for task in tasks):
            print(f"Task number {task_id} not found! Please try again.")
            continue

        original_length = len(tasks)
        tasks = list(filter(lambda task: task['id'] != task_id, tasks))

        if len(tasks) == original_length:
                    print("Failed to delete task!")
                    continue

        for index, task in enumerate(tasks, 1):
                task['id'] = index

        try:
            with open('tasks.json', 'w') as file:
                json.dump(tasks, file, indent=4)
            print("\nTask successfully deleted!")
        except Exception as e:
            print(f"Error saving to file: {e}")
        break

main()                