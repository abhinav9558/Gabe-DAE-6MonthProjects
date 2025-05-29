import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSACTION_FILE = os.path.join(SCRIPT_DIR, "created_transactions.csv")
BUDGET_FILE = os.path.join(SCRIPT_DIR, "created_budgets.csv")


class BudgetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        self.transactions_df = pd.DataFrame()
        self.budgets = {}
        self.load_budgets()

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()

        tk.Label(self.root, text="Budget Tracker Main Menu", font=('Helvetica', 16)).pack(pady=10)

        tk.Button(self.root, text="Load Transactions", command=self.load_transactions).pack(pady=5)
        tk.Button(self.root, text="View Budgets", command=self.view_budgets).pack(pady=5)
        tk.Button(self.root, text="Set Budget", command=self.set_budget).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_transactions(self):
        try:
            file_path = TRANSACTION_FILE
            if not os.path.isfile(file_path):
                # Create a new CSV with correct headers
                empty_df = pd.DataFrame(columns=[
                    "Date", "Description", "Amount", "Income/Expense", "Personal/Business", "Category"
                ])
                empty_df.to_csv(file_path, index=False) #Index = False will not include dataframe row numbers

            # Load with skip option for malformed rows
            self.transactions_df = pd.read_csv(file_path, on_bad_lines='skip') # on_bad_lines is a Pandas feature, skipping will remove improperly formatted rows.
            self.display_transactions()

        except Exception as e:
            messagebox.showerror("Error", f"Could not load transactions:\n{e}")

        self.tree = ttk.Treeview(self.root, columns=..., show="headings")
        tk.Button(self.root, text="Delete Selected Transaction", command=self.delete_transaction).pack(pady=5)

    def delete_transaction(self):
    selected_item = self.tree.selection()
    if not selected_item:
        messagebox.showwarning("No selection", "Please select a transaction to delete.")
        return

    # Get the transaction details from Treeview
    values = self.tree.item(selected_item, 'values')
    if not values:
        return

    # Remove from DataFrame
    try:
        self.transactions_df = self.transactions_df[
            ~((self.transactions_df["Date"] == values[0]) &
              (self.transactions_df["Description"] == values[1]) &
              (self.transactions_df["Amount"] == float(values[2])) &
              (self.transactions_df["Income/Expense"] == values[3]) &
              (self.transactions_df["Person"] == values[4]) &
              (self.transactions_df["Category"] == values[5]))
        ]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete transaction: {e}")
        return

    # Save to CSV
    self.transactions_df.to_csv(TRANSACTION_FILE, index=False)

    # Remove from Treeview
    self.tree.delete(selected_item)

    messagebox.showinfo("Deleted", "Transaction deleted successfully.")


    def load_budgets(self):
        if os.path.exists(BUDGET_FILE):
            try:
                df = pd.read_csv(BUDGET_FILE)
                self.budgets = dict(zip(df["Category"], df["Budget"]))
            except Exception as e:
                messagebox.showerror("Error", f"Could not load budgets:\n{e}")

    def save_budgets(self):
        df = pd.DataFrame(list(self.budgets.items()), columns=["Category", "Budget"])
        df.to_csv(BUDGET_FILE, index=False)


    def display_transactions(self):
        self.clear_frame()
        tk.Label(self.root, text="Transaction Table", font=('Helvetica', 14)).pack(pady=10)

        table_frame = tk.Frame(self.root)
        table_frame.pack()

        tree = ttk.Treeview(table_frame)
        tree["columns"] = list(self.transactions_df.columns)
        tree["show"] = "headings"

        for col in self.transactions_df.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        for index, row in self.transactions_df.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack()

        # ----- Add Transaction Form -----
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Add New Transaction", font=('Helvetica', 12)).grid(row=0, columnspan=2, pady=5)

        tk.Label(form_frame, text="Date").grid(row=1, column=0)
        date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        tk.Entry(form_frame, textvariable=date_var).grid(row=1, column=1)

        tk.Label(form_frame, text="Description").grid(row=2, column=0)
        desc_entry = tk.Entry(form_frame)
        desc_entry.grid(row=2, column=1)

        tk.Label(form_frame, text="Amount").grid(row=3, column=0)
        amount_entry = tk.Entry(form_frame)
        amount_entry.grid(row=3, column=1)

        tk.Label(form_frame, text="Income/Expense").grid(row=4, column=0)
        type_var = tk.StringVar(value="Expense")
        type_menu = ttk.Combobox(form_frame, textvariable=type_var, values=["Income", "Expense"], state="readonly")
        type_menu.grid(row=4, column=1)

        tk.Label(form_frame, text="Personal/Business").grid(row=5, column=0)
        account_var = tk.StringVar(value="Personal")
        account_menu = ttk.Combobox(form_frame, textvariable=account_var, values=["Personal", "Business"], state="readonly")
        account_menu.grid(row=5, column=1)

        tk.Label(form_frame, text="Category").grid(row=6, column=0)
        category_entry = tk.Entry(form_frame)
        category_entry.grid(row=6, column=1)

        def save_transaction():
            try:
                new_data = {
                    "Date": date_var.get(),
                    "Description": desc_entry.get(),
                    "Amount": float(amount_entry.get()),
                    "Income/Expense": type_var.get(),
                    "Personal/Business": account_var.get(),
                    "Category": category_entry.get()
                }

                new_row = pd.DataFrame([new_data])
                file_path = TRANSACTION_FILE

                file_exists = os.path.isfile(TRANSACTION_FILE)
                new_row.to_csv(file_path, mode='a', header=not file_exists, index=False)

                self.transactions_df = pd.concat([self.transactions_df, new_row], ignore_index=True)

                messagebox.showinfo("Success", "Transaction added!")
                self.display_transactions()

            except ValueError:
                messagebox.showerror("Error", "Amount must be a number.")

        tk.Button(form_frame, text="Add Transaction", command=save_transaction).grid(row=7, columnspan=2, pady=10)

        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu).pack(pady=10)


    def view_budgets(self):
        self.clear_frame()
        tk.Label(self.root, text="Category Budgets", font=('Helvetica', 14)).pack(pady=10)

        for category, amount in self.budgets.items():
            spent = self.transactions_df[
                self.transactions_df["Category"] == category
            ]["Amount"].sum()
            msg = f"{category}: Budget = {amount}, Spent = {spent}"
            tk.Label(self.root, text=msg).pack()

        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu).pack(pady=10)

    def set_budget(self):
        self.clear_frame()
        tk.Label(self.root, text="Set Category Budget", font=('Helvetica', 14)).pack(pady=10)

        # Load categories from transactions
        if os.path.exists(TRANSACTION_FILE):
            try:
                trans_df = pd.read_csv(TRANSACTION_FILE, on_bad_lines='skip')
                categories = sorted(trans_df["Category"].dropna().unique())
            except:
                categories = []
        else:
            categories = []

        tk.Label(self.root, text="Category").pack()

        category_var = tk.StringVar()
        if categories:
            category_dropdown = ttk.Combobox(self.root, textvariable=category_var, values=categories)
            category_dropdown.pack()
        else:
            category_entry = tk.Entry(self.root, textvariable=category_var)
            category_entry.pack()

        tk.Label(self.root, text="Budget Amount").pack()
        amount_entry = tk.Entry(self.root)
        amount_entry.pack()

        def save_budget():
            category = category_var.get()
            try:
                amount = float(amount_entry.get())
                self.budgets[category] = amount
                self.save_budgets()
                messagebox.showinfo("Success", f"Budget for {category} set to {amount}")
                self.create_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.")

        tk.Button(self.root, text="Save Budget", command=save_budget).pack(pady=10)
        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu).pack(pady=5)



if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTracker(root)
    root.mainloop()
