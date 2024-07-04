import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import time
import json
from datetime import datetime, timedelta
import sched

TASK_FILE = 'tasks.json'
HISTORY_FILE = 'history.json'
SCHEDULER_INTERVAL = 60  # Check every 60 seconds

def load_tasks():
    try:
        with open(TASK_FILE, 'r') as file:
            tasks = json.load(file)
            if isinstance(tasks, list) and all(isinstance(task, dict) for task in tasks):
                return tasks
            else:
                return []
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASK_FILE, 'w') as file:
        json.dump(tasks, file)

def load_history():
    try:
        with open(HISTORY_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_history(history):
    with open(HISTORY_FILE, 'w') as file:
        json.dump(history, file)

def add_task(task):
    tasks = load_tasks()
    tasks.append({"task": task, "completed": False})
    save_tasks(tasks)

def reset_tasks():
    tasks = load_tasks()
    if tasks:
        history = load_history()
        today = datetime.now().strftime('%Y-%m-%d')
        history[today] = tasks
        save_history(history)
    save_tasks([])  # Clear tasks

def view_tasks():
    return load_tasks()

def view_history():
    history = load_history()
    if history:
        history_text = ""
        for date, tasks in history.items():
            history_text += f"{date}:\n"
            for task in tasks:
                status = "Completed" if task["completed"] else "Incomplete"
                history_text += f"  - {task['task']} ({status})\n"
        return history_text
    else:
        return "No task history available."

def schedule_reset_tasks(scheduler):
    now = datetime.now()
    next_reset = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    delay = (next_reset - now).total_seconds()
    scheduler.enter(delay, 1, reset_tasks)
    scheduler.enter(delay + 86400, 1, schedule_reset_tasks, (scheduler,))

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        
        self.frame = tk.Frame(root)
        self.frame.pack(padx=50, pady=50)
        
        self.task_list_label = tk.Label(self.frame, text="Today's Tasks:")
        self.task_list_label.pack()
        
        self.task_list_frame = tk.Frame(self.frame)
        self.task_list_frame.pack()
        
        self.update_task_list()
        
        self.add_task_button = tk.Button(self.frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=5)
        
        self.view_history_button = tk.Button(self.frame, text="View Task History", command=self.view_history)
        self.view_history_button.pack(pady=5)
        
    def update_task_list(self):
        for widget in self.task_list_frame.winfo_children():
            widget.destroy()
        
        tasks = view_tasks()
        self.task_vars = []
        for task in tasks:
            var = tk.BooleanVar(value=task["completed"])
            chk = tk.Checkbutton(self.task_list_frame, text=task["task"], variable=var, command=self.save_task_status)
            chk.pack(anchor='w')
            self.task_vars.append({"task": task["task"], "var": var})
        
    def save_task_status(self):
        tasks = [{"task": task["task"], "completed": task["var"].get()} for task in self.task_vars]
        save_tasks(tasks)
        
    def add_task(self):
        task = simpledialog.askstring("Input", "Enter a task:")
        if task:
            add_task(task)
            self.update_task_list()
        
    def view_history(self):
        history = view_history()
        messagebox.showinfo("Task History", history)

if __name__ == '__main__':
    root = tk.Tk()
    app = TaskManagerApp(root)
    
    scheduler = sched.scheduler(time.time, time.sleep)
    reset_thread = threading.Thread(target=schedule_reset_tasks, args=(scheduler,), daemon=True)
    reset_thread.start()
    
    root.mainloop()
