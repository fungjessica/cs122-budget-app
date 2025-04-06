import tkinter as tk
from transactions import TransactionApp  # Import TransactionApp from transaction.py
from budgeting import BudgetingApp      # Import BudgetingApp from budgeting.py

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Manager")
        self.root.geometry("300x200")
        
        # Title Label
        tk.Label(root, text="Welcome to Budget Manager", font=("Arial", 16, "bold")).pack(pady=20)
        
        # Buttons to launch different features
        tk.Button(root, text="Manage Transactions", command=self.open_transactions).pack(pady=10)
        tk.Button(root, text="Manage Budget", command=self.open_budget).pack(pady=10)
    
    def open_transactions(self):
        """Open the Transaction Management interface."""
        transaction_window = tk.Toplevel(self.root)  # Create a new window for transactions
        TransactionApp(transaction_window)           # Instantiate TransactionApp in the new window
    
    def open_budget(self):
        """Open the Budget Management interface."""
        budget_window = tk.Toplevel(self.root)       # Create a new window for budgets
        BudgetingApp(budget_window)                 # Instantiate BudgetingApp in the new window

# Main Application Entry Point
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
