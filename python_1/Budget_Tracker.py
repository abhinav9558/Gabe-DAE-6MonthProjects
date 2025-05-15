import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# Determine current directory and data file
current_dir = os.getcwd()
DATA_FILE = os.path.join(current_dir, "transaction_data.csv")

# -------------------- Setup --------------------
root = tk.Tk()
root.title("Budget Tracker")
root.geometry("1280x720")

columns = ("Date", "Category", "Description", "Amount")
tree = ttk.Treeview(root, columns=columns, show="headings", selectmode="browse")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill=tk.BOTH, expand=True, pady=10)

# -------------------- Entry Inputs --------------------
entry_frame = tk.Frame(root)
entry_frame.pack(pady=10)

labels = [
    "Date", "Amount", "Vendor", "Income/Expense",
    "Vendor/Location", "Personal/Business", "Category", "Notes"
]

entry_vars = []
entries = []

for i, label in enumerate(labels):
    tk.Label(entry_frame, text=label).grid(row=0, column=i, padx=3)
    entry = tk.Entry(entry_frame, width=15)
    entry.grid(row=1, column=i, padx=3)
    entries.append(entry)

# Pre-fill some defaults
entries[0].insert(0, "2025-05-15")  # Date
entries[1].insert(0, "0.00")        # Amount
entries[3].insert(0, "Expense")     # Income/Expense
entries[5].insert(0, "Personal")    # Personal/Business


# -------------------- File Handling --------------------
def load_data_from_file():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert("", tk.END, values=row)

def save_entry_to_file(entry):
    with open(DATA_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(entry)

def write_all_to_file():
    with open(DATA_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for child in tree.get_children():
            writer.writerow(tree.item(child)["values"])


# -------------------- Actions --------------------
def add_entry():
    data = tuple(entry.get() for entry in entries)
    tree.insert("", tk.END, values=data)
    save_entry_to_file(data)

def edit_entry():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No selection", "Please select an entry to edit.")
        return
    updated_data = tuple(entry.get() for entry in entries)
    tree.item(selected, values=updated_data)
    write_all_to_file()

def delete_entry():
    selected = tree.selection()
    if selected:
        tree.delete(selected)
        write_all_to_file()
    else:
        messagebox.showwarning("No selection", "Please select an entry to delete.")

def clear_all():
    if messagebox.askyesno("Clear All", "Are you sure you want to delete all entries?"):
        for item in tree.get_children():
            tree.delete(item)
        write_all_to_file()

    # Update Treeview item
    updated_data = (
        date_entry.get(),
        category_entry.get(),
        desc_entry.get(),
        amount_entry.get(),
    )
    tree.item(selected, values=updated_data)
    write_all_to_file()

def populate_fields(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected)["values"]
        for entry, value in zip(entries, values):
            entry.delete(0, tk.END)
            entry.insert(0, value)


tree.bind("<<TreeviewSelect>>", populate_fields)

# -------------------- Buttons --------------------
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Entry", width=15, command=add_entry).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Edit Entry", width=15, command=edit_entry).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete Entry", width=15, command=delete_entry).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Clear All", width=15, command=clear_all).grid(row=0, column=3, padx=5)

# -------------------- Load Data on Start --------------------
load_data_from_file()

# -------------------- Run App --------------------
root.mainloop()
