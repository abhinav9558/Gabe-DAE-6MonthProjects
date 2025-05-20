import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import csv
import os

# -------------------- File Setup --------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(current_dir, "transaction_data.csv")

# -------------------- App Setup --------------------
root = tk.Tk()
root.title("Transaction Tracker")
root.geometry("1280x720")

# Main menu frame
main_menu_frame = tk.Frame(root)
main_menu_frame.pack(fill=tk.BOTH, expand=True)
main_menu_frame.tkraise()


# Button to open the transactions frame
show_button = tk.Button(main_menu_frame, text="Show Transactions", command=lambda: show_frame(transactions_frame))
show_button.pack(pady=20)


transactions_frame = tk.Frame(root)  # This will be shown later on button click

def show_frame(frame_to_show):
    main_menu_frame.pack_forget()
    transactions_frame.pack_forget()

    frame_to_show.pack(fill=tk.BOTH, expand=True)
    frame_to_show.tkraise()

# -------------------- Transactions Setup --------------------
columns = ("Date", "Description", "Amount", "Income/Expense", "Personal/Business", "Category")
tree = ttk.Treeview(transactions_frame, columns=columns, show="headings", selectmode="browse")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(fill=tk.BOTH, expand=True, pady=10)

# -------------------- Entry Inputs --------------------
entry_frame = tk.Frame(transactions_frame)
entry_frame.pack(pady=10)

labels = list(columns)
entries = []

for i, label in enumerate(labels):
    tk.Label(entry_frame, text=label).grid(row=0, column=i, padx=3)
    entry = tk.Entry(entry_frame, width=15)
    entry.grid(row=1, column=i, padx=3)
    entries.append(entry)

# Pre-fill defaults
entries[0].insert(0, date.today())  # Date
entries[2].insert(0, "0.00")        # Amount
entries[3].insert(0, "Expense")     # Income/Expense
entries[4].insert(0, "Personal")    # Personal/Business

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

def populate_fields(event):
    selected = tree.selection()
    if selected:
        values = tree.item(selected)["values"]
        for entry, value in zip(entries, values):
            entry.delete(0, tk.END)
            entry.insert(0, value)

tree.bind("<<TreeviewSelect>>", populate_fields)

# -------------------- Buttons --------------------
button_frame = tk.Frame(transactions_frame)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Entry", width=15, command=add_entry).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Edit Entry", width=15, command=edit_entry).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete Entry", width=15, command=delete_entry).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Clear All", width=15, command=clear_all).grid(row=0, column=3, padx=5)

# Return button to go back to main menu
return_button = tk.Button(transactions_frame, text="Return to Menu", command=lambda: show_frame(main_menu_frame))
return_button.pack(pady=10)

# -------------------- Load Data on Start --------------------
load_data_from_file()

# -------------------- Run App --------------------
root.mainloop()
