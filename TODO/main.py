
from tkinter import *
from tkinter import messagebox, font
import random, subprocess, json, datetime
from addtask import add_task_window
from PIL import Image, ImageTk
from tokenizertext import tokenize_task_data

# Constants
CREDENTIALS_FILE = "users.json"
RANDOM_JOBS = ["buy grocery", "practice piano", "call mom", "clean the house", "read a book", "go for a walk",
               "watch a movie", "do laundry", "organize desk", "exercise"]
THEMES = [
    {'bg': '#ffffff', 'fg': 'black', 'button_bg': '#e0e0e0', 'button_fg': 'black', 'label_bg': '#ffffff',
     'label_fg': 'black'},
    {'bg': '#ffcccb', 'fg': 'black', 'button_bg': '#ff9999', 'button_fg': 'black', 'label_bg': '#ffcccb',
     'label_fg': 'black'},  # Light Pink
    {'bg': '#98fb98', 'fg': 'black', 'button_bg': '#32cd32', 'button_fg': 'white', 'label_bg': '#98fb98',
     'label_fg': 'black'},  # Light Green
]
CHECK_KEYWORDS = ['نوشتن', 'نوشت', 'بنویس', 'writing', 'email', 'نامه', 'draft', 'compose', 'report', 'دستور', 'پست',
                  'emailing', 'مقاله', 'write']

# Global Variables
tasks = []
task_vars = []  # List to hold BooleanVars for checkboxes
search_var = None
theme_index = 0  # Start from the first theme
current_user = None  # To track the currently logged-in user


# Authentication functions
def load_credentials():
    try:
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def authenticate(username, password):
    credentials = load_credentials()
    return credentials.get(username) == password


def login():
    global current_user
    username = username_entry.get()
    password = password_entry.get()
    if authenticate(username, password):
        current_user = username  # Set the current user
        login_window.destroy()
        main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")


def register():
    """Open the registration window to add a new user."""

    def save_new_user():
        new_username = new_username_entry.get().strip()
        new_password = new_password_entry.get().strip()

        if new_username and new_password:
            credentials = load_credentials()
            if new_username in credentials:
                messagebox.showerror("Registration Failed", "Username already exists!")
            else:
                credentials[new_username] = new_password
                with open(CREDENTIALS_FILE, "w") as file:
                    json.dump(credentials, file, indent=4)
                messagebox.showinfo("Registration Successful", "User registered successfully!")
                register_window.destroy()
        else:
            messagebox.showerror("Registration Failed", "Username and password cannot be empty!")

    register_window = Toplevel(login_window)
    register_window.title("Register New User")
    register_window.geometry("300x250")

    Label(register_window, text="Username:").pack(pady=5)
    new_username_entry = Entry(register_window)
    new_username_entry.pack(pady=5)

    Label(register_window, text="Password:").pack(pady=5)
    new_password_entry = Entry(register_window, show="*")
    new_password_entry.pack(pady=5)

    Button(register_window, text="Register", command=save_new_user).pack(pady=10)
    Button(register_window, text="Cancel", command=register_window.destroy).pack(pady=5)


# Task Management Functions
def save_tasks():
    """Save the current tasks to a user-specific JSON file."""
    if current_user:
        tasks_file = f"tasks_{current_user}.json"
        with open(tasks_file, "w") as file:
            json.dump(tasks, file, indent=4, default=str)


def load_tasks():
    """Load tasks from a user-specific JSON file."""
    global tasks
    if current_user:
        tasks_file = f"tasks_{current_user}.json"
        try:
            with open(tasks_file, "r") as file:
                content = file.read().strip()  # Read and remove extra spaces
                tasks = json.loads(content) if content else []
                for task in tasks:
                    if "deadline" in task:
                        try:
                            task["deadline"] = datetime.datetime.strptime(task["deadline"], "%Y-%m-%d").date()
                        except ValueError:
                            pass  # Skip invalid date formats
        except (FileNotFoundError, json.JSONDecodeError):
            tasks = []  # Set tasks to an empty list if there's an error


def get_color(color_name):
    """Return the hex color code based on the task's color."""
    colors = {
        "blue": "#ADD8E6",
        "red": "#FFCCCC",
        "green": "#CCFFCC",
        "orange": "#FFDAB9",
        "yellow": "#FFFFE0",
        "white": "#FFFFFF"
    }
    return colors.get(color_name.lower(), "#FFFFFF")  # Default to white if color not found


def toggle_theme():
    """Toggle between different themes."""
    global theme_index
    theme = THEMES[theme_index]
    root.tk_setPalette(background=theme['bg'], foreground=theme['fg'])
    root.option_add('*TButton.background', theme['button_bg'])
    root.option_add('*TButton.foreground', theme['button_fg'])
    root.option_add('*Label.background', theme['label_bg'])
    root.option_add('*Label.foreground', theme['label_fg'])
    root.option_add('*Entry.background', theme['button_bg'])
    root.option_add('*Entry.foreground', theme['button_fg'])
    root.option_add('*Button.background', theme['button_bg'])
    root.option_add('*Button.foreground', theme['button_fg'])
    theme_index = (theme_index + 1) % len(THEMES)


def update_task_status(index, var):
    """Update the 'done' status of the task when the checkbox is clicked."""
    tasks[index]["done"] = var.get()
    save_tasks()  # Save tasks to the file after updating status


def is_due_soon(due_date):
    """Check if the task is due soon (within the next 2 days)."""
    today = datetime.date.today()
    if isinstance(due_date, str):
        due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
    return (due_date - today).days <= 2 and (due_date - today).days >= 0


def check_keywords_in_task(title, description):
    """Check if any of the specified keywords exist in the task's title or description."""
    title_tokens, description_tokens = tokenize_task_data(title, description)
    return any(keyword in (title_tokens + description_tokens) for keyword in CHECK_KEYWORDS)


def update_list():
    """Refresh the task list with checkboxes and edit buttons."""
    search_text = search_var.get().lower()  # Get the current search text and convert to lowercase
    for widget in task_frame.winfo_children():
        widget.destroy()  # Clear previous widgets

    task_vars.clear()  # Reset the task_vars list
    for index, task in enumerate(tasks):
        if search_text in task["title"].lower() or search_text in task["description"].lower():
            var = BooleanVar(value=task.get("done", False))
            task_vars.append(var)

            task_frame_row = Frame(task_frame)
            task_frame_row.pack(fill="x", pady=2)

            due_soon = is_due_soon(task["deadline"])  # Check if the task is due soon

            checkbox = Checkbutton(
                task_frame_row,
                text=f"{task['title']} | {task['description']} | {task['deadline']}",
                variable=var,
                anchor="w",
                bg=get_color(task.get("color", "white")),
                fg="black",
                relief="flat",
                command=lambda idx=index, v=var: update_task_status(idx, v)
            )
            if due_soon:
                current_font = font.nametofont(checkbox.cget("font"))
                new_font = current_font.copy()
                new_font.configure(underline=True)
                checkbox.config(font=new_font)
            else:
                checkbox.config(font=font.nametofont(checkbox.cget("font")).copy().configure(underline=False))

            checkbox.pack(side="left", fill="x", expand=True, padx=5)

            edit_button = Button(
                task_frame_row,
                text="Edit",
                command=lambda idx=index: edit_task(idx),
                bg="yellow",
                fg="black",
                width=10
            )
            edit_button.pack(side="right", padx=5)

            if check_keywords_in_task(task["title"], task["description"]):
                help_button = Button(
                    task_frame_row,
                    text="Get Help from ChatGPT",
                    command=lambda idx=index: get_help_from_chatgpt(idx),
                    bg="blue",
                    fg="black",
                    width=20
                )
                help_button.pack(side="right", padx=10)


def get_help_from_chatgpt(task_index):
    """Handle the 'Get Help from ChatGPT' button click."""
    task = tasks[task_index]
    process = subprocess.Popen(
        ["python", "apichatgpt.py", task["description"]],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output, error = process.communicate()
    response_text = error.decode() if error else json.loads(output.decode()).get("response", "Error parsing response.")
    response_window = Toplevel(root)
    response_window.title("ChatGPT Response")
    response_window.geometry("500x300")
    Label(response_window, text="ChatGPT Response:", font=("Arial", 14)).pack(pady=5)
    response_textbox = Text(response_window, wrap="word", height=10, width=50)
    response_textbox.insert("1.0", response_text)
    response_textbox.config(state="disabled")
    response_textbox.pack(pady=5, padx=10)
    Button(response_window, text="Close", command=response_window.destroy).pack(pady=5)


def edit_task(index):
    """Open an edit window to modify a task."""
    task = tasks[index]
    edit_window = Toplevel(root)
    edit_window.title("Edit Task")
    edit_window.geometry("400x300")

    Label(edit_window, text="Title:").grid(row=0, column=0, padx=5, pady=5)
    title_entry = Entry(edit_window, width=40)
    title_entry.insert(0, task["title"])
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    Label(edit_window, text="Description:").grid(row=1, column=0, padx=5, pady=5)
    description_entry = Text(edit_window, width=30, height=4)
    description_entry.insert("1.0", task["description"])
    description_entry.grid(row=1, column=1, padx=5, pady=5)

    Label(edit_window, text="Label Color:").grid(row=2, column=0, padx=5, pady=5)
    color_var = StringVar(value=task["color"])
    color_menu = OptionMenu(edit_window, color_var, "Blue", "Green", "Orange", "Red", "Yellow")
    color_menu.grid(row=2, column=1, padx=5, pady=5)

    Button(
        edit_window, text="Save Changes",
        command=lambda: save_changes(index, title_entry, description_entry, color_var, edit_window)
    ).grid(row=3, column=0, columnspan=2, pady=10)


def save_changes(index, title_entry, description_entry, color_var, edit_window):
    """Save the changes to the task and close the edit window."""
    tasks[index]["title"] = title_entry.get().strip()
    tasks[index]["description"] = description_entry.get("1.0", "end-1c").strip()
    tasks[index]["color"] = color_var.get().strip()
    update_list()
    save_tasks()
    edit_window.destroy()


def add_task():
    """Add a new task."""

    def callback(new_task):
        new_task["done"] = False
        tasks.append(new_task)
        update_list()
        save_tasks()

    add_task_window(root, None, callback)


def Delete_All():
    """Delete all tasks."""
    global tasks
    tasks.clear()
    update_list()
    save_tasks()


def Delete_One_Task():
    """Delete the first selected (checked) task."""
    global tasks
    for i, var in enumerate(task_vars):
        if var.get():  # If the task is checked
            del tasks[i]
            break
    update_list()
    save_tasks()


def Sort_Tasks_ASC():
    """Sort tasks alphabetically (ascending)."""
    tasks.sort(key=lambda task: task["title"])
    update_list()


def Sort_Tasks_DESC():
    """Sort tasks alphabetically (descending)."""
    tasks.sort(key=lambda task: task["title"], reverse=True)
    update_list()


def Choose_Random():
    """Display a random task."""
    random_task = random.choice(RANDOM_JOBS)
    titel_random["text"] = random_task
    titel_random["fg"] = "black"


def num_of_tasks():
    """Display the total number of tasks."""
    titel_task_num["text"] = f"Number Of Tasks: {len(tasks)}"


# def set_logo(window):
#     """Set the logo for a window."""
#     logo_path = "/Users/homa/Desktop/Final to do/todo_107314.webp"
#     icon_image = Image.open(logo_path)
#     icon_photo = ImageTk.PhotoImage(icon_image)
#     window.iconphoto(False, icon_photo)


def main_app():
    global root, task_frame, search_var, titel_task_num, titel_random
    root = Tk()
    root.title("To-Do List")
    root.geometry("890x400")

    # Initialize the search variable after creating root
    search_var = StringVar()

    # Load logo and set window icon
    logo_path = "/Users/homa/Desktop/Final to do/todo_107314.webp"
    icon_image = Image.open(logo_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    root.iconphoto(False, icon_photo)

    # Configure grid weights
    root.grid_rowconfigure(0, weight=1)
    for i in range(1, 9):
        root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=3)

    # Widgets layout
    titel_lable = Label(root, text="To-Do List", font=("Arial", 16))
    titel_lable.grid(row=0, column=0, sticky="w", padx=10, pady=5)

    # Initialize the labels for random task and task count
    titel_random = Label(root, text=" ")
    titel_random.grid(row=0, column=1, sticky="w", padx=10, pady=5)

    titel_task_num = Label(root, text=" ")
    titel_task_num.grid(row=1, column=1, sticky="w", padx=10, pady=5)

    search_label = Label(root, text="🔍 Search:")
    search_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)

    search_entry = Entry(root, textvariable=search_var)
    search_entry.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
    search_var.trace("w", lambda name, index, mode: update_list())

    # Buttons
    buttons = [
        ("Add Task", add_task),
        ("Delete All", Delete_All),
        ("Delete Selected Task", Delete_One_Task),
        ("Sort Tasks (ASC)", Sort_Tasks_ASC),
        ("Sort Tasks (DES)", Sort_Tasks_DESC),
        ("Choose Random", Choose_Random),
        ("Number Of Tasks", num_of_tasks),
        ("Quit", root.destroy)
    ]

    for i, (text, command) in enumerate(buttons):
        Button(root, text=text, fg="black" if "Delete" not in text else "red", command=command).grid(row=3 + i, column=0, sticky="ew", padx=10, pady=5)

    # Theme button
    theme_button = Button(root, text="Change Theme", command=toggle_theme)
    theme_button.grid(row=0, column=1, sticky="e", padx=10, pady=5)

    # Task list frame (initialize here)
    task_frame = Frame(root)
    task_frame.grid(row=3, column=1, rowspan=7, sticky="nsew", padx=10, pady=5)

    load_tasks()
    update_list()

    # Start the main event loop
    root.mainloop()


# Login Window
login_window = Tk()
login_window.title("Login")
login_window.geometry("300x250")

Label(login_window, text="Username:").pack(pady=5)
username_entry = Entry(login_window)
username_entry.pack(pady=5)

Label(login_window, text="Password:").pack(pady=5)
password_entry = Entry(login_window, show="*")
password_entry.pack(pady=5)

Button(login_window, text="Login", command=login).pack(pady=10)
Button(login_window, text="Register", command=register).pack(pady=10)

login_window.mainloop()
