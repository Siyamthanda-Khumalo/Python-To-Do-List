import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
from datetime import datetime


def add_task():
    task = entry_task.get().strip()
    desc = entry_desc.get().strip()
    due = entry_due.get_date().strftime("%Y-%m-%d")
    priority = combo_priority.get()

    if not task:
        messagebox.showwarning("Warning", "Please enter a task name.")
        return

    tree.insert("", "end", values=(task, desc if desc else "—", due, priority))

    entry_task.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    entry_due.set_date(datetime.today())
    combo_priority.current(1)

# Delete task
def delete_task():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a task to delete.")
        return
    for item in selected:
        tree.delete(item)

# Edit task
def edit_task():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a task to edit.")
        return
    item = selected[0]
    values = tree.item(item, "values")

    new_task = simpledialog.askstring("Edit Task", "Task name:", initialvalue=values[0]) or values[0]
    new_desc = simpledialog.askstring("Edit Description", "Task description:", initialvalue=values[1]) or values[1]
    new_due = simpledialog.askstring("Edit Due Date", "YYYY-MM-DD:", initialvalue=values[2]) or values[2]
    new_priority = simpledialog.askstring("Edit Priority", "High / Medium / Low:", initialvalue=values[3]) or values[3]

    tree.item(item, values=(new_task, new_desc, new_due, new_priority))

# ----------- UI Setup -----------
root = tk.Tk()
root.title("Modern To-Do List")
root.geometry("900x550")
root.configure(bg="#f4f6f9")

# Modern ttk theme
style = ttk.Style(root)
style.theme_use("clam")

# Treeview style
style.configure("Treeview",
                background="#ffffff",
                foreground="#000000",
                rowheight=32,
                fieldbackground="#ffffff",
                font=("Segoe UI", 11))
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
style.map("Treeview", background=[("selected", "#e0e0e0")])

# Input frame
input_frame = tk.Frame(root, bg="#f4f6f9")
input_frame.pack(fill="x", padx=20, pady=10)

# Labels + Inputs
lbl_font = ("Segoe UI", 11)

tk.Label(input_frame, text="Task", font=lbl_font, bg="#f4f6f9").grid(row=0, column=0, sticky="w", padx=5, pady=5)
entry_task = tk.Entry(input_frame, font=("Segoe UI", 11), width=25, relief="flat", bd=2, highlightthickness=1, highlightbackground="#cccccc")
entry_task.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Description", font=lbl_font, bg="#f4f6f9").grid(row=0, column=2, sticky="w", padx=5, pady=5)
entry_desc = tk.Entry(input_frame, font=("Segoe UI", 11), width=25, relief="flat", bd=2, highlightthickness=1, highlightbackground="#cccccc")
entry_desc.grid(row=0, column=3, padx=5, pady=5)

tk.Label(input_frame, text="Due Date", font=lbl_font, bg="#f4f6f9").grid(row=1, column=0, sticky="w", padx=5, pady=5)
entry_due = DateEntry(input_frame, font=("Segoe UI", 11), width=22,
                      background="#2e86de", foreground="white", borderwidth=0, date_pattern="yyyy-mm-dd")
entry_due.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Priority", font=lbl_font, bg="#f4f6f9").grid(row=1, column=2, sticky="w", padx=5, pady=5)
combo_priority = ttk.Combobox(input_frame, values=["High", "Medium", "Low"], font=("Segoe UI", 11), width=22, state="readonly")
combo_priority.grid(row=1, column=3, padx=5, pady=5)
combo_priority.current(1)

# Buttons
btn_frame = tk.Frame(root, bg="#f4f6f9")
btn_frame.pack(fill="x", padx=20, pady=10)

btn_style = {"font": ("Segoe UI", 11, "bold"), "bg": "#2e86de", "fg": "white", "relief": "flat", "activebackground": "#1b4f72", "cursor": "hand2"}

tk.Button(btn_frame, text="➕ Add Task", command=add_task, **btn_style).pack(side="left", padx=5, pady=5, ipadx=10, ipady=5)
tk.Button(btn_frame, text="✏ Edit Task", command=edit_task, **btn_style).pack(side="left", padx=5, pady=5, ipadx=10, ipady=5)
tk.Button(btn_frame, text="🗑 Delete Task", command=delete_task, **btn_style).pack(side="left", padx=5, pady=5, ipadx=10, ipady=5)

# Task Table
columns = ("Task", "Description", "Due Date", "Priority")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200, anchor="center")

tree.pack(fill="both", expand=True, padx=20, pady=10)

# Scrollbar
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

root.mainloop()
