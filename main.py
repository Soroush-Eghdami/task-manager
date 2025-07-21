import json # For saving and loading in JSON format
import os # For cheking if the file exixst
from colorama import Fore, Style, init # For coloring the output
from datetime import datetime, timedelta # For handling the deadlines

init(autoreset=True)  # Resetting the color of each print

# Global variable for storing tasks
tasks =[] 

# For adding tasks
def add():
    title = input("Enter the task title: ")
    description = input("Enter the task description: ")
    deadline = input("Enter your deadline (YYYY-MM-DD): ")
    priority = input("What is the priority (low / medium / high):")

    # Stroing all data in a dictionary 
    task ={
        "title": title,
        "description": description,
        "deadline": deadline,
        "priority": priority,
        "stats" : "not Started"
    }

    # Storing all datas in our Global variable
    tasks.append(task)
    return task


# For listing the tasks
def listing():
    # If the task list is empty, return a message
    if len(tasks) == 0:
        return "List is empty"

    # Asking the user how they want the list to be sorted
    print("How would you like to sort: ", 
          "\n1. By Deadline (sooner first):",  
          "\n2. By Priority:")
    sort_choice = input("Enter your choice: ")

    # Cheking the user choice for sorting
    match sort_choice:
        case '1':
            # Function for converting deadline string into datetime object
            def date(task):
                date = task["deadline"]
                if (
                    len(date) == 10
                    and date[4] == '-'
                    and date[7] == '-'
                    and all(part.isdigit() for part in date.split("-"))
                ):
                    return datetime.strptime(date, "%Y-%m-%d")
                return datetime.max  # If the date is invalid, push it to the end

            # Sorting tasks based on date
            sorted_tasks = sorted(tasks, key=date)

        case '2':
            # Custom order for sorting priorities
            priority_order = {"high": 1, "medium": 2, "low": 3}
            # Sorting tasks based on priority
            sorted_tasks = sorted(tasks, key=lambda x: priority_order.get(x["priority"].lower(), 4))

        case _:
            print("Invalid choice. Showing unsorted list.")
            sorted_tasks = tasks  # If invalid input, show the list as it is

    count = 1 # For numbering the tasks

    # Looping through sorted tasks and printing each one
    for task in sorted_tasks:
        # Coloring based on priority
        priority_color = {
            "high": Fore.RED,
            "medium": Fore.YELLOW,
            "low": Fore.GREEN
        }.get(task["priority"].lower(), "")

        # Printing the task details
        print("Task", count,
              "\nTitle: ", task["title"],
              "\nDescription: ", task["description"],
              "\nDeadline: ", task["deadline"],
              "\nPriority: ", priority_color + task["priority"],
              "\nStatus: ", task["stats"])
        count += 1 # Updating the task number
    print()



def complete():

    # If the task list is empty, return a message
    if len(tasks) == 0: 
        return "List is empty"
    
    listing() # Calls the Listing function
    num = input("Enter the tak number you want to mark as completed: ")

    if not num.isdigit() or int(num) < 1 or int(num) > len(tasks): # IF the input was not a number or not in the valid range 
        return "Please enter a valid number. "
    
    # For the selecttask number 
    num = int(num)
    if 1 <= num <= len(tasks):
        tasks[num - 1]["stats"] = "Completed"  
        return "Task marked as completed."
    else: 
        return "Invalid task number."
    
def delete():
    # If the task list is empty, return a message
    if len(tasks) == 0:
        return "List is empty"
    
    listing()# Calls the Listing function
    num = input("Enter the task number you want to delete: ")

    if not num.isdigit() or int(num) < 1 or int(num) > len(tasks): # IF the input was not a number or not in the valid range 
        return "Please enter a valid number."
    
    num = int(num)
    if 1 <= num <= len(tasks):
        tasks.pop(num - 1)
        return "Task deleted successfully."
    else:
        return "Invalid task number."
    
def edit():

    # If the task list is empty, return a message
    if len(tasks) == 0:
        return "List is empty"
    
    listing() # Calls the Listing function
    num = input("Enter the task number you want to edit: ")

    if not num.isdigit(): # IF the input was not a number 
        return "Please enter a valid number."
    
    num = int(num)
    if 1 <= num <= len(tasks):
        task = tasks[num - 1]
        # Showing a list of choices
        print("Which field do you want to edit? ", 
              "\n1. Title", 
              "\n2. Description", 
              "\n3. Deadline", 
              "\n4. Priority")
        field = input("Enter your choice: ")


        # Cheking the user input (choice) for starting the action
        match (field):
            case '1':
                task["title"] = input("Enter new title: ")
            case '2':
                task["description"] = input("Enter new description: ")
            case '3':
                task["deadline"] = input("Enter new deadline (YYYY-MM-DD): ")
            case '4':
                task["priority"] = input("Enter new priority (Low / Medium / High): ")
            case _:
                return "Invalid choice."
        
        return "task updated with success."
    
def save():
    with open("tasks.json", "w") as f: # Opening the json file 
        json.dump(tasks, f, indent=4) # Saving the tasks in the json file
    return "Tasks saved to file."

def load():
        global tasks
        if os.path.exists("tasks.json"): # Cheking if the file exists
            with open("tasks.json", "r") as f: # Opening the file
                tasks = json.load(f) # Loading the tasks
            return "Tasks loaded from file."
        else:
            tasks = [] # If the file did'nt exist return an empty list
            return "No saved tasks found."



def menu():
    while True: # for looping in menu
        print("Hi ",
              "\n1. Add a task and saving the task: ",  
              "\n2. List all tasks: ", 
              "\n3. Mark as completed: ", 
              "\n4. Delete a task: ", 
              "\n5. Edit a task: ",
              "\n6. load tasks from a file: ",
              "\n7. Exit: ")
        
        # Getting the user choice
        choice = input("Please select your choice: ") 
        
        # Matching the choice with a related function
        match (choice):
            case '1':
                add()
                save()
            case '2':
                listing()
            case '3':
                print(complete())
            case '4':
                print(delete())
            case '5':
                print(edit())
            case '6':
                print(load())
            case '7':
                print("Exiting the program. Goodbye!")
                break
            case _:
                print("Invalid choice.\n")

print(load())
menu()