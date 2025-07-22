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

        Raises:

        Edge Cases:

        Extend & Modify:

        Integration Notes: 

        """
        self.root = root
        self.root.title("Budget Tracker")
        self.transactions_df = pd.DataFrame()
        self.budgets = {}

        # Makes sure both transactions and budgets will be properly parsed
        self.load_transactions()
        self.load_budgets()

        self.create_main_menu()

        # Center the window on screen without changing its size
        self.center_window(self.root)


    def center_window(self, window):
        """
        Centers a Tkinter window on the screen without changing its size.

        Args:
            window: The Tkinter window (Tk or Toplevel) to center.
        """
        window.update_idletasks()  # Ensure size info is updated
        width = window.winfo_width()
        height = window.winfo_height()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"+{x}+{y}")


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

    def sort_column(self, col):
        """
        Sort the Treeview column when header is clicked.
        Automatically switches between ascending/descending.

        Args:
            col (str): Column name to sort by.

        Returns:
            None
        """
        reverse = self.sort_direction.get(col, False)

        def try_parse(val):
            try:
                return pd.to_datetime(val)
            except:
                pass
            # Try to parse number
            try:
                return float(val)
            except:
                pass
            return str(val).lower()  # Fallback to string

        # Use custom sort key to handle dates, numbers, and strings
        sorted_df = self.transactions_df.copy()
        sorted_df["_sort_key"] = sorted_df[col].map(try_parse)
        sorted_df = sorted_df.sort_values("_sort_key", ascending=not reverse).drop(columns=["_sort_key"])

        self.sort_direction[col] = not reverse
        self.transactions_df = sorted_df

        # Clear the tree and re-insert sorted rows
        for row in self.tree.get_children():
            self.tree.delete(row)
        for _, row_data in sorted_df.iterrows():
            self.tree.insert("", "end", values=list(row_data))

    def handle_delete_click(self, event):
        """
        Handle click on Treeview rows. Deletes the row if ❌ is clicked.
        """
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)

        col_index = int(col.replace("#", "")) - 1

        if self.tree["columns"][col_index] == "Delete":
            confirm = messagebox.askyesno("Delete", "Delete this transaction?")
            if confirm:
                try:
                    # Drop the row by index
                    self.transactions_df.drop(index=int(row_id), inplace=True)
                    self.transactions_df.reset_index(drop=True, inplace=True)

                    # Save updated CSV
                    self.transactions_df.to_csv(TRANSACTION_FILE, index=False)

                    # Refresh UI
                    self.display_transactions()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete row:\n{e}")


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
                    # If the csv file of transactions is not found in file_path directory, it will generate a new csv file in that location with the necesary column headers.
                    empty_df = pd.DataFrame(columns=[
                        "Date", "Description", "Amount", "Income/Expense", "Personal/Business", "Category"
                    ])
                    empty_df.to_csv(file_path, index=False) #C

                self.transactions_df = pd.read_csv(file_path, on_bad_lines='skip') # Using Pandas we can read the csv file in the data frame and any improperly formatted columns will be will be skipped using on_bad_lines='skip'.
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

        columns = list(self.transactions_df.columns) + ["Delete"]
        tree["columns"] = columns

        tree["show"] = "headings"

         # Store tree so it's accessible in sort_column
        self.tree = tree
        self.sort_direction = {}  # Tracks sort direction per column

        for col in self.transactions_df.columns:
            tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))


        for index, row in self.transactions_df.iterrows():
            tree.insert(parent="", index="end", iid=str(index), values=list(row) + ["✖️"])


        tree.pack()

        tree.bind("<Button-1>", self.handle_delete_click)

        self.tree = tree  # Store tree reference


        # ----- Add Transaction Form -----
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        # Section title (centered above the full row)
        tk.Label(form_frame, text="Add New Transaction", font=('Helvetica', 12)).grid(row=0, column=0, columnspan=6, pady=5)

        # Row of labels (side by side)
        tk.Label(form_frame, text="Date").grid(row=1, column=0, padx=5, pady=5)
        tk.Label(form_frame, text="Description").grid(row=1, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Amount").grid(row=1, column=2, padx=5, pady=5)
        tk.Label(form_frame, text="Income/Expense").grid(row=1, column=3, padx=5, pady=5)
        tk.Label(form_frame, text="Personal/Business").grid(row=1, column=4, padx=5, pady=5)
        tk.Label(form_frame, text="Category").grid(row=1, column=5, padx=5, pady=5)

        # Row of entry fields (aligned under each label)
        date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        tk.Entry(form_frame, textvariable=date_var, width=12).grid(row=2, column=0, padx=5)

        desc_entry = tk.Entry(form_frame, width=15)
        desc_entry.grid(row=2, column=1, padx=5)

        amount_entry = tk.Entry(form_frame, width=10)
        amount_entry.grid(row=2, column=2, padx=5)

        type_var = tk.StringVar(value="Expense")
        type_menu = ttk.Combobox(form_frame, textvariable=type_var, values=["Income", "Expense"], state="readonly", width=12)
        type_menu.grid(row=2, column=3, padx=5)

        account_var = tk.StringVar(value="Personal")
        account_menu = ttk.Combobox(form_frame, textvariable=account_var, values=["Personal", "Business"], state="readonly", width=12)
        account_menu.grid(row=2, column=4, padx=5)

        category_var = tk.StringVar()
        category_entry = ttk.Combobox(form_frame, textvariable=category_var, values=DEFAULT_CATEGORIES, state="normal", width=12)
        category_entry.grid(row=2, column=5, padx=5)

        # Center the window on screen without changing its size
        self.center_window(self.root)

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
        Display budgets and amounts spent per category with the ability to delete them.

        Clears the frame and lists each category's budget alongside total spent.
        Includes delete buttons for each budget and a button to return to the main menu.
        """

        self.clear_frame()
        tk.Label(self.root, text="Category Budgets", font=('Helvetica', 14)).pack(pady=10)

        for category, amount in self.budgets.items():
            spent = self.transactions_df[
                self.transactions_df["Category"] == category
            ]["Amount"].sum()

            msg = f"{category}: Budget = {amount}, Spent = {spent}"

            row_frame = tk.Frame(self.root)
            row_frame.pack(pady=2)

            tk.Label(row_frame, text=msg).pack(side="left", padx=5)

            # Inline delete function for this specific category
            def delete(c=category):
                confirm = messagebox.askyesno("Confirm Delete", f"Delete budget for '{c}'?")
                if confirm:
                    del self.budgets[c]
                    if hasattr(self, "save_budgets"):
                        self.save_budgets()  # Optional if persistence is implemented
                    self.view_budgets()  # Refresh view

            tk.Button(row_frame, text="Delete", fg="red", command=delete).pack(side="right")

        tk.Button(self.root, text="Back to Main Menu", command=self.create_main_menu).pack(pady=10)
        self.center_window(self.root)

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

        # Center the window on screen without changing its size
        self.center_window(self.root)

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