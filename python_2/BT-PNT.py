import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSACTION_FILE = os.path.join(SCRIPT_DIR, "created_transactions.csv")
BUDGET_FILE = os.path.join(SCRIPT_DIR, "created_budgets.csv")

DEFAULT_CATEGORIES = [
    "Rent / Mortgage", "Utilities", "Internet & Cable", "Groceries",
    "Dining Out", "Fuel / Gas", "Clothing", "Health Insurance",
    "Medical", "Tuition", "Office Supplies", "Emergency Fund",
    "Credit Card Payments", "Movies", "Travel", "Gifts", "Miscellaneous"
]

class BudgetTracker:
    def __init__(self, root):
        """
        Initialize the Budget Tracker application.

        Sets up the main window, initializes data structures, loads budgets,
        and displays the main menu.

        Args:
            root: The Tkinter root window.

        Returns:
            None

        Side Effects:
            - Sets window title.
            - Initializes transactions DataFrame and budget dictionary.
            - Loads saved budgets.
            - Displays the main menu UI.
        """
        self.root = root
        self.root.title("Budget Tracker")
        self.transactions_df = pd.DataFrame()
        self.budgets = {}
        self.load_budgets()

        self.create_main_menu()

    def create_main_menu(self):
        """
        Create and display the main menu UI for the budget tracker.

        Clears the current frame and displays buttons for key actions.

        Args:
            self: Instance of the class.

        Returns:
            None

        Side Effects:
            - Clears existing UI elements.
            - Adds and displays new buttons and labels on the root window.
        """

        self.clear_frame()

        tk.Label(self.root, text="Budget Tracker Main Menu", font=('Helvetica', 16)).pack(pady=10)

        tk.Button(self.root, text="Load Transactions", command=self.load_transactions).pack(pady=5)
        tk.Button(self.root, text="View Budgets", command=self.view_budgets).pack(pady=5)
        tk.Button(self.root, text="Set Budget", command=self.set_budget).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)

    def clear_frame(self):
        """
        Remove all widgets from the main window.

        Clears the current UI by destroying all child widgets of the root window.

        Args:
            self: Instance of the class.

        Returns:
            None

        Side Effects:
            - Deletes all widgets from the root window.
        """

        for widget in self.root.winfo_children():
            widget.destroy()

    def load_transactions(self):
        """
        Load transactions from a CSV file into a DataFrame.

        Creates the file with default columns if it doesn't exist.
        On failure, prompts the user to retry or cancel.

        Args:
            self: Instance of the class.

        Returns:
            None

        Side Effects:
            - Updates self.transactions_df.
            - Displays transactions.
            - Shows error dialog on failure.
            - Prints status message.
        """

        success = False
        while not success:
            try:
                file_path = TRANSACTION_FILE
                if not os.path.isfile(file_path):
                    empty_df = pd.DataFrame(columns=[
                        "Date", "Description", "Amount", "Income/Expense", "Personal/Business", "Category"
                    ])
                    empty_df.to_csv(file_path, index=False)

                self.transactions_df = pd.read_csv(file_path, on_bad_lines='skip')
                self.display_transactions()
            
            except Exception as e:
                retry = messagebox.askretrycancel("Error", f"Could not load transactions:\n{e}\n\nRetry?")
                if not retry:
                    break  # Exit the loop if user cancels
            else:
                success = True
            finally:
                print("Tried loading transaction file.")


    def load_budgets(self):
        """
        Load saved budget data from a CSV file into a dictionary.

        If the file exists, it reads category-budget pairs into `self.budgets`.

        Args:
            self: Instance of the class.

        Returns:
            None

        Side Effects:
            - Updates self.budgets.
            - Shows error dialog if file cannot be read.
        """

        if os.path.exists(BUDGET_FILE):
            try:
                df = pd.read_csv(BUDGET_FILE)
                self.budgets = dict(zip(df["Category"], df["Budget"]))
            except Exception as e:
                messagebox.showerror("Error", f"Could not load budgets:\n{e}")

    def save_budgets(self):
        """
        Save the current budget dictionary to a CSV file.

        Converts `self.budgets` into a DataFrame and writes it to disk.

        Args:
            self: Instance of the class.

        Returns:
            None

        Side Effects:
            - Writes to BUDGET_FILE.
        """

        df = pd.DataFrame(list(self.budgets.items()), columns=["Category", "Budget"])
        df.to_csv(BUDGET_FILE, index=False)


    def display_transactions(self):
        """
        Display the transaction table and input form in the UI.

        Clears the current frame and shows a table of transactions,
        followed by a form for adding new transactions.

        Args:
            self: Instance of the class.

        Returns:
            None

        Side Effects:
            - Clears the UI and repopulates it with transaction-related widgets.
        """

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
            """
            Save a new transaction to the CSV file and update the display.

            Gathers form data, validates the amount, appends the transaction
            to the CSV file and updates the internal DataFrame.

            Args:
                None (uses closure variables from the parent method).

            Returns:
                None

            Side Effects:
                - Appends new row to TRANSACTION_FILE.
                - Updates self.transactions_df.
                - Shows success or error message.
                - Refreshes the transaction display.
            """    

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
        """
        Display budgets and amounts spent per category.

        Clears the frame and lists each category's budget alongside total spent.
        Includes a button to return to the main menu.

        Args:
            self: Instance of the class.

        Returns:
            None

        Side Effects:
            - Updates the UI with budget and spending information.
        """

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
        """
        Display a form to set or update the budget for a category.

        Loads existing categories from transactions (if available).
        Allows user to select or enter a category and specify a budget amount.
        Saves the budget on successful input and returns to the main menu.

        Args:
            self: Instance of the class.

        Returns:
            None

        Side Effects:
            - Updates self.budgets and saves to file.
            - Displays success or error dialogs.
            - Updates the UI with form elements.
        """

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
            """
            Save the budget for a selected category after validating input.

            Retrieves the category and amount from the form, updates the budget
            dictionary, saves it to file, and returns to the main menu. Shows an
            error message if the amount is invalid.

            Args:
                None (uses closure variables from the parent method).

            Returns:
                None

            Side Effects:
                - Updates self.budgets and writes to disk.
                - Displays success or error messages.
                - Navigates back to the main menu UI.
            """

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