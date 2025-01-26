import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime

def add_task_window(root, task_list_frame, on_task_added):
    def add_task():
        title = title_entry.get().strip()
        description = description_entry.get("1.0", "end-1c").strip()
        label_color = color_var.get().strip()
        deadline = deadline_picker.get_date().strftime('%Y-%m-%d')  # Get the selected date

        if not title:
            messagebox.showwarning("Input Error", "Task title is required.")
            return

        task_details = {
            "title": title,
            "description": description or "No Description",
            "color": label_color,
            "deadline": deadline,
            "completed": False,
            "created_at": datetime.now(),
        }

        # Add the task to the global task list
        on_task_added(task_details)

        # Clear the input fields after adding the task
        title_entry.delete(0, tk.END)
        description_entry.delete("1.0", tk.END)
        color_var.set("Blue")
        deadline_picker.set_date(datetime.today())

    # Create the task form
    task_form_window = tk.Toplevel(root)
    task_form_window.title("Add Task")
    task_form_window.geometry("400x300")

    # Title Entry
    tk.Label(task_form_window, text="Title:").grid(row=0, column=0, padx=5, pady=5)
    title_entry = tk.Entry(task_form_window, width=40)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    # Description Textbox
    tk.Label(task_form_window, text="Description:").grid(row=1, column=0, padx=5, pady=5)
    description_entry = tk.Text(task_form_window, width=30, height=4)
    description_entry.grid(row=1, column=1, padx=5, pady=5)

    # Color Option Menu
    tk.Label(task_form_window, text="Label Color:").grid(row=2, column=0, padx=5, pady=5)
    color_var = tk.StringVar(value="Blue")
    color_menu = tk.OptionMenu(task_form_window, color_var, "Blue", "Green", "Orange", "Red", "Yellow")
    color_menu.grid(row=2, column=1, padx=5, pady=5)


    # Deadline Picker
    tk.Label(task_form_window, text="Deadline:").grid(row=5, column=0, padx=5, pady=5)
    deadline_picker = DateEntry(task_form_window, width=15, background="blue", foreground="white", date_pattern="yyyy-MM-dd")
    deadline_picker.grid(row=5, column=1, padx=5, pady=5)

    # Add Task Button
    save_button = tk.Button(task_form_window, text="Save Task", command=add_task)
    save_button.grid(row=6, column=0, columnspan=2, pady=10)

