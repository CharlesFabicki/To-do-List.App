import tkinter as tk
from datetime import datetime
from tkinter import simpledialog, messagebox
from tkcalendar import Calendar


class Task:
    def __init__(self, description, deadline=None):
        self.description = description
        self.done = False
        self.deadline = deadline


class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, description, deadline):
        task = Task(description, deadline)
        self.tasks.append(task)

    def mark_task_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].done = True

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]

    def mark_all_done(self):
        for task in self.tasks:
            task.done = True

    def get_task_list(self):
        return self.tasks

    def save_tasks(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            for task in self.tasks:
                status = "[Done]" if task.done else "[To Do]"
                deadline_str = task.deadline.strftime("%d-%m-%Y %H:%M") if task.deadline else "None"
                file.write(f"{status} {task.description} - Deadline: {deadline_str}\n")

    def load_tasks(self, filename):
        self.tasks = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split(' - Deadline: ')
                    description = parts[0]

                    done = "[Done]" in description
                    description = description.replace("[Done]", "").replace("[To Do]", "").strip()

                    deadline_str = parts[1]
                    if deadline_str != "None":
                        deadline = datetime.strptime(deadline_str, "%d-%m-%Y %H:%M")
                    else:
                        deadline = None

                    task = Task(description, deadline)
                    task.done = done
                    self.tasks.append(task)
        except FileNotFoundError:
            self.tasks = []

    def clear_completed(self):
        self.tasks = [task for task in self.tasks if not task.done]


def get_deadline():
    deadline_str = simpledialog.askstring("Deadline", "Enter the deadline (DD-MM-YYYY HH:MM):")
    if deadline_str:
        try:
            deadline = datetime.strptime(deadline_str, "%d-%m-%Y %H:%M")
            return deadline
        except ValueError:
            messagebox.showerror("Error", "Invalid deadline format. Please use DD-MM-YYYY HH:MM.")
    return None


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.configure(bg="#2E2E2E")  # Dark background color

        self.todo_list = ToDoList()

        self.deadline_calendar = Calendar(root, selectmode="day", date_pattern="dd-mm-yyyy")
        self.deadline_calendar.pack()
        self.hide_calendar()

        self.task_entry = tk.Entry(root, width=55, bg="#444444", fg="white",
                                   font=("Helvetica", 16))
        self.task_entry.pack(pady=10)
        self.task_entry.insert(0, "Please Enter Your Task Here")
        self.task_entry.bind("<FocusIn>", self.on_task_entry_focus_in)
        self.task_entry.bind("<FocusOut>", self.on_task_entry_focus_out)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task, bg="#006400",
                                    fg="white", width=35, font=("Helvetica", 12, "bold"))  # Dark green button color
        self.add_button.pack()

        self.mark_done_button = tk.Button(root, text="Mark as Done", command=self.mark_task_done, bg="#DAA520",
                                          fg="white", width=35,
                                          font=("Helvetica", 12, "bold"))  # Very dark yellow button color
        self.mark_done_button.pack()

        self.mark_all_done_button = tk.Button(root, text="Mark All as Done", command=self.mark_all_done, bg="#DAA520",
                                              fg="white", width=35,
                                              font=("Helvetica", 12, "bold"))
        self.mark_all_done_button.pack()

        self.remove_button = tk.Button(root, text="Remove Task", command=self.remove_task, bg="#DC143C", fg="white",
                                       width=35, font=("Helvetica", 12, "bold"))
        self.remove_button.pack()

        self.save_button = tk.Button(root, text="Save Tasks", command=self.save_tasks, bg="#4169E1", fg="white",
                                     width=35, font=("Helvetica", 12, "bold"))
        self.save_button.pack()

        self.load_button = tk.Button(root, text="Load Tasks", command=self.load_tasks, bg="#4169E1", fg="white",
                                     width=35, font=("Helvetica", 12, "bold"))
        self.load_button.pack()

        self.edit_button = tk.Button(root, text="Edit Task", command=self.edit_task, bg="#8A2BE2", fg="white",
                                     width=35, font=("Helvetica", 12, "bold"))  # BlueViolet button color
        self.edit_button.pack()

        self.clear_completed_button = tk.Button(root, text="Clear Completed", command=self.clear_completed,
                                                bg="#FF4500", fg="white", width=35, font=("Helvetica", 12, "bold"))
        self.clear_completed_button.pack()

        self.clear_all_button = tk.Button(root, text="Clear All Tasks", command=self.clear_all_tasks, bg="#FF0000",
                                          fg="white", width=35, font=("Helvetica", 12, "bold"))  # Red button color
        self.clear_all_button.pack()

        self.task_listbox = tk.Listbox(root, width=80, height=12, bg="#333333", fg="white",
                                       font=("Helvetica", 12))  # Dark listbox colors
        self.task_listbox.pack(pady=10)

        self.exit_button = tk.Button(root, text="Exit", command=self.confirm_exit, bg="#222222",
                                     fg="white", width=35, font=("Helvetica", 12, "bold"))  # Dark exit button color
        self.exit_button.pack()

        self.date_time_label = tk.Label(root, text="", bg="#2E2E2E", fg="white", font=("Helvetica", 18))
        self.date_time_label.pack()

        self.update_date_time()
        self.update_task_list()

    def on_task_entry_focus_in(self, event):
        if self.task_entry.get() == "Please Enter Your Task Here":
            self.task_entry.delete(0, tk.END)

    def on_task_entry_focus_out(self, event):
        if not self.task_entry.get():
            self.task_entry.insert(0, "Please Enter Your Task Here")

    def confirm_exit(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit the app?"):
            self.root.destroy()

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Info", "No task selected to edit.")
            return

        selected_task = self.todo_list.get_task_list()[selected_index[0]]
        new_description = simpledialog.askstring("Edit Task", "                     Edit task description:                     ",
                                                 initialvalue=selected_task.description)
        if new_description is not None:
            selected_task.description = new_description
            self.update_task_list()

    def update_date_time(self):
        current_time = datetime.now().strftime("%d-%m-%Y [%H:%M:%S]")
        self.date_time_label.config(text=current_time)
        self.date_time_label.after(1000, self.update_date_time)  # Update every 1000ms (1 second)

    def add_task(self):
        description = self.task_entry.get()
        if not description:
            messagebox.showerror("Error", "Please enter a task description.")
            return

        self.show_calendar()  # Pokazujemy kalendarz

    def get_deadline_from_calendar(self):
        date_selected = self.deadline_calendar.get_date()
        if date_selected:
            try:
                deadline = datetime.strptime(date_selected, "%d-%m-%Y")
                return deadline
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use DD-MM-YYYY.")
        return None

    def confirm_date(self):
        deadline = self.get_deadline_from_calendar()
        if deadline is not None:
            description = self.task_entry.get()
            self.time_entry = simpledialog.askstring(
                "What time should this task be done?",
                "                                  Enter the time (HH:MM):                                  "
            )
            if self.time_entry:
                try:
                    time = datetime.strptime(self.time_entry, "%H:%M")
                    deadline = deadline.replace(hour=time.hour, minute=time.minute)
                    self.todo_list.add_task(description, deadline)
                    self.update_task_list()
                    self.task_entry.delete(0, tk.END)
                    self.hide_calendar()
                except ValueError:
                    messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")

    def show_calendar(self):
        self.deadline_calendar.pack()
        self.deadline_calendar.bind("<<CalendarSelected>>", lambda event: self.confirm_date())

    def hide_calendar(self):
        self.deadline_calendar.pack_forget()

    def get_deadline_from_calendar(self):
        date_selected = self.deadline_calendar.get_date()
        self.hide_calendar()
        if date_selected:
            try:
                deadline = datetime.strptime(date_selected, "%d-%m-%Y")
                return deadline
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please use DD-MM-YYYY.")
        return None

    def mark_task_done(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Info", "No task selected to mark as done.")
            return

        self.todo_list.mark_task_done(selected_index[0])
        self.update_task_list()

    def mark_all_done(self):
        self.todo_list.mark_all_done()
        self.update_task_list()

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Info", "No task selected to remove.")
            return

        self.todo_list.remove_task(selected_index[0])
        self.update_task_list()

    def save_tasks(self):
        self.todo_list.save_tasks("tasks.txt")

    def load_tasks(self):
        self.todo_list.load_tasks("tasks.txt")
        self.update_task_list()

    def clear_completed(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear completed tasks?"):
            self.todo_list.clear_completed()
            self.update_task_list()

    def clear_all_tasks(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?"):
            self.todo_list.tasks = []
            self.update_task_list()

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.todo_list.get_task_list():
            status = "Done" if task.done else "To Do"
            deadline_str = task.deadline.strftime("%d-%m-%Y [%H:%M]") if task.deadline else "No Deadline"
            self.task_listbox.insert(tk.END, f"[{status}] {task.description} - Due date: {deadline_str}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()



