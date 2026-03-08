import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime


BG = "#f5f5f5"
CARD_BG = "#fbfbfb"
TEXT_PRIMARY = "#111827"
TEXT_SECONDARY = "#6b7280"
ACCENT = "#1f2937"
ACCENT_HOVER = "#111827"
BORDER = "#e7e7e7"


def add_task(event=None):
    task = entry_task.get().strip()
    description = entry_desc.get().strip() or "-"
    due_date = entry_due.get_date().strftime("%Y-%m-%d")
    priority = combo_priority.get()

    if not task:
        messagebox.showwarning("Missing Task", "Please enter a task name.")
        entry_task.focus_set()
        return

    row_id = tree.insert("", "end", values=(task, description, due_date, priority))
    tree.item(row_id, tags=(priority.lower(),))

    clear_inputs()
    refresh_summary()


def clear_inputs():
    entry_task.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    entry_due.set_date(datetime.today())
    combo_priority.current(1)
    entry_task.focus_set()


def delete_task():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Select at least one task to delete.")
        return

    for item in selected:
        tree.delete(item)

    refresh_summary()


def edit_task():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Select a task to edit.")
        return

    item_id = selected[0]
    values = tree.item(item_id, "values")
    open_editor(item_id, values)


def open_editor(item_id, values):
    editor = tk.Toplevel(root)
    editor.title("Edit Task")
    editor.configure(bg=BG)
    editor.resizable(False, False)
    editor.transient(root)
    editor.grab_set()

    panel = tk.Frame(editor, bg=CARD_BG, bd=1, relief="flat", highlightthickness=1, highlightbackground=BORDER)
    panel.pack(padx=12, pady=12, fill="both", expand=True)

    tk.Label(panel, text="Task", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", padx=12, pady=(12, 5))
    task_entry = ttk.Entry(panel, width=38)
    task_entry.grid(row=1, column=0, padx=12, pady=(0, 10), sticky="ew")
    task_entry.insert(0, values[0])

    tk.Label(panel, text="Description", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9)).grid(row=2, column=0, sticky="w", padx=12, pady=(0, 5))
    desc_entry = ttk.Entry(panel, width=38)
    desc_entry.grid(row=3, column=0, padx=12, pady=(0, 10), sticky="ew")
    desc_entry.insert(0, values[1] if values[1] != "-" else "")

    row_two = tk.Frame(panel, bg=CARD_BG)
    row_two.grid(row=4, column=0, padx=12, pady=(0, 10), sticky="ew")
    row_two.columnconfigure(0, weight=1)
    row_two.columnconfigure(1, weight=1)

    tk.Label(row_two, text="Due Date", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9)).grid(row=0, column=0, sticky="w", pady=(0, 5))
    due_entry = DateEntry(row_two, date_pattern="yyyy-mm-dd", width=14, background=ACCENT, foreground="white", borderwidth=0)
    due_entry.grid(row=1, column=0, sticky="w")

    try:
        due_entry.set_date(datetime.strptime(values[2], "%Y-%m-%d"))
    except ValueError:
        due_entry.set_date(datetime.today())

    tk.Label(row_two, text="Priority", bg=CARD_BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9)).grid(row=0, column=1, sticky="w", pady=(0, 5), padx=(10, 0))
    priority_box = ttk.Combobox(row_two, state="readonly", values=["High", "Medium", "Low"], width=12)
    priority_box.grid(row=1, column=1, sticky="w", padx=(10, 0))
    priority_box.set(values[3] if values[3] in ["High", "Medium", "Low"] else "Medium")

    actions = tk.Frame(panel, bg=CARD_BG)
    actions.grid(row=5, column=0, padx=12, pady=(0, 12), sticky="e")

    def save_changes():
        new_task = task_entry.get().strip()
        if not new_task:
            messagebox.showwarning("Missing Task", "Task name cannot be empty.")
            task_entry.focus_set()
            return

        new_desc = desc_entry.get().strip() or "-"
        new_due = due_entry.get_date().strftime("%Y-%m-%d")
        new_priority = priority_box.get()

        tree.item(item_id, values=(new_task, new_desc, new_due, new_priority), tags=(new_priority.lower(),))
        refresh_summary()
        editor.destroy()

    ttk.Button(actions, text="Cancel", style="Ghost.TButton", command=editor.destroy).pack(side="right", padx=(6, 0))
    ttk.Button(actions, text="Save", style="Primary.TButton", command=save_changes).pack(side="right")

    panel.columnconfigure(0, weight=1)
    task_entry.focus_set()


def on_select(_event=None):
    refresh_summary()


def refresh_summary():
    total = len(tree.get_children())
    selected_count = len(tree.selection())

    if selected_count:
        summary_var.set(f"{total} tasks | {selected_count} selected")
    else:
        summary_var.set(f"{total} tasks")


def build_styles():
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("Base.TFrame", background=BG)
    style.configure(
        "TEntry",
        fieldbackground="#ffffff",
        foreground=TEXT_PRIMARY,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        insertcolor=TEXT_PRIMARY,
        padding=6,
    )
    style.configure(
        "TCombobox",
        fieldbackground="#ffffff",
        foreground=TEXT_PRIMARY,
        bordercolor=BORDER,
        lightcolor=BORDER,
        darkcolor=BORDER,
        arrowsize=14,
        padding=4,
    )

    style.configure(
        "Treeview",
        background=CARD_BG,
        fieldbackground=CARD_BG,
        foreground=TEXT_PRIMARY,
        rowheight=32,
        borderwidth=0,
        relief="flat",
        font=("Segoe UI", 9),
    )
    style.configure(
        "Treeview.Heading",
        background="#f7f7f7",
        foreground=TEXT_SECONDARY,
        font=("Segoe UI Semibold", 9),
        relief="flat",
        borderwidth=0,
    )
    style.map("Treeview", background=[("selected", "#ededed")], foreground=[("selected", TEXT_PRIMARY)])

    style.configure(
        "Primary.TButton",
        font=("Segoe UI Semibold", 9),
        foreground="white",
        background=ACCENT,
        borderwidth=0,
        focusthickness=2,
        focuscolor=ACCENT,
        padding=(12, 6),
    )
    style.map("Primary.TButton", background=[("active", ACCENT_HOVER)])

    style.configure(
        "Ghost.TButton",
        font=("Segoe UI", 9),
        foreground=TEXT_PRIMARY,
        background="#f4f4f4",
        bordercolor=BORDER,
        borderwidth=1,
        padding=(12, 6),
    )
    style.map("Ghost.TButton", background=[("active", "#e9e9e9")])


# Window
root = tk.Tk()
root.title("TaskFlow")
root.geometry("920x600")
root.minsize(780, 520)
root.configure(bg=BG)

build_styles()

main = tk.Frame(root, bg=BG)
main.pack(fill="both", expand=True, padx=18, pady=16)

# Header
header = tk.Frame(main, bg=BG)
header.pack(fill="x", pady=(0, 10))

header_title = tk.Label(header, text="TaskFlow", bg=BG, fg=TEXT_PRIMARY, font=("Segoe UI Semibold", 22))
header_title.pack(anchor="w")

header_subtitle = tk.Label(
    header,
    text="Simple task planning with a clean, focused workspace",
    bg=BG,
    fg=TEXT_SECONDARY,
    font=("Segoe UI", 10),
)
header_subtitle.pack(anchor="w", pady=(2, 0))

# Input card
input_card = tk.Frame(main, bg=CARD_BG, bd=1, relief="flat", highlightthickness=1, highlightbackground=BORDER)
input_card.pack(fill="x", pady=(0, 10))

fields = tk.Frame(input_card, bg=CARD_BG)
fields.pack(fill="x", padx=12, pady=10)

for col in range(4):
    fields.columnconfigure(col, weight=1)

label_font = ("Segoe UI", 9)


def field_label(text, row, col):
    tk.Label(fields, text=text, bg=CARD_BG, fg=TEXT_SECONDARY, font=label_font).grid(
        row=row, column=col, sticky="w", padx=6, pady=(0, 5)
    )


field_label("Task", 0, 0)
field_label("Description", 0, 1)
field_label("Due Date", 0, 2)
field_label("Priority", 0, 3)

entry_task = ttk.Entry(fields)
entry_task.grid(row=1, column=0, sticky="ew", padx=6)

entry_desc = ttk.Entry(fields)
entry_desc.grid(row=1, column=1, sticky="ew", padx=6)

entry_due = DateEntry(fields, date_pattern="yyyy-mm-dd", background=ACCENT, foreground="white", borderwidth=0)
entry_due.grid(row=1, column=2, sticky="ew", padx=6)

combo_priority = ttk.Combobox(fields, values=["High", "Medium", "Low"], state="readonly")
combo_priority.grid(row=1, column=3, sticky="ew", padx=6)
combo_priority.current(1)

actions = tk.Frame(input_card, bg=CARD_BG)
actions.pack(fill="x", padx=12, pady=(0, 10))

add_button = ttk.Button(actions, text="Add Task", style="Primary.TButton", command=add_task)
add_button.pack(side="right")

edit_button = ttk.Button(actions, text="Edit Selected", style="Ghost.TButton", command=edit_task)
edit_button.pack(side="right", padx=(0, 8))

delete_button = ttk.Button(actions, text="Delete Selected", style="Ghost.TButton", command=delete_task)
delete_button.pack(side="right", padx=(0, 8))

# Table card
table_card = tk.Frame(main, bg=CARD_BG, bd=1, relief="flat", highlightthickness=1, highlightbackground=BORDER)
table_card.pack(fill="both", expand=True)

table_container = tk.Frame(table_card, bg=CARD_BG)
table_container.pack(fill="both", expand=True, padx=6, pady=6)

columns = ("Task", "Description", "Due Date", "Priority")
tree = ttk.Treeview(table_container, columns=columns, show="headings", selectmode="extended")

col_widths = {"Task": 205, "Description": 285, "Due Date": 115, "Priority": 105}
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=col_widths[col], anchor="w")

tree.tag_configure("high", foreground="#1f2937")
tree.tag_configure("medium", foreground="#4b5563")
tree.tag_configure("low", foreground="#9ca3af")

scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Footer
footer = tk.Frame(main, bg=BG)
footer.pack(fill="x", pady=(10, 0))

summary_var = tk.StringVar(value="0 tasks")
summary = tk.Label(footer, textvariable=summary_var, bg=BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9))
summary.pack(side="left")

hint = tk.Label(footer, text="Tip: Double-click a task to edit", bg=BG, fg=TEXT_SECONDARY, font=("Segoe UI", 9))
hint.pack(side="right")

# Bindings
entry_task.bind("<Return>", add_task)
tree.bind("<<TreeviewSelect>>", on_select)
tree.bind("<Double-1>", lambda _event: edit_task())

clear_inputs()
refresh_summary()

root.mainloop()
