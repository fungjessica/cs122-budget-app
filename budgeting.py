import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BudgetingApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Budget Manager")
        self.center_window(self.root, 800, 600)
        
        self.budgets = pd.DataFrame(columns=['username', 'period', 'category', 'budget', 'used'])
        self.transactions = pd.read_csv('./transactions.csv')
        self.load_budgets()
        
        self.create_widgets()
        self.update_chart()
        
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x}+{y}")

    def load_budgets(self):
        try:
            self.budgets = pd.read_csv('./budgets.csv')
        except FileNotFoundError:
            pass

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        
        # Create Budget Tab
        create_tab = ttk.Frame(self.notebook)
        self.create_budget_ui(create_tab)
        
        # View Budget Tab
        view_tab = ttk.Frame(self.notebook)
        self.create_view_ui(view_tab)
        
        self.notebook.add(create_tab, text="Create Budget")
        self.notebook.add(view_tab, text="View Budget")
        self.notebook.pack(expand=True, fill='both')

    def create_budget_ui(self, parent):
        ttk.Label(parent, text="Budget Period:").grid(row=0, column=0, padx=10, pady=5)
        self.period_var = tk.StringVar()
        ttk.Combobox(parent, textvariable=self.period_var, 
                    values=["Month", "6 Months", "Year"]).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(parent, text="Category:").grid(row=1, column=0, padx=10, pady=5)
        self.category_entry = ttk.Entry(parent)
        self.category_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(parent, text="Budget Amount:").grid(row=2, column=0, padx=10, pady=5)
        self.amount_entry = ttk.Entry(parent)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Button(parent, text="Add Category", command=self.add_category).grid(row=3, columnspan=2, pady=10)
        
        self.category_list = tk.Listbox(parent)
        self.category_list.grid(row=4, columnspan=2, padx=10, pady=5)
        
        ttk.Button(parent, text="Save Budget", command=self.save_budget).grid(row=5, columnspan=2, pady=10)

    def create_view_ui(self, parent):
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, parent)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')

    def add_category(self):
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        if category and amount:
            self.category_list.insert(tk.END, f"{category}: ${amount}")
            self.category_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)

    def save_budget(self):
        period = self.period_var.get()
        categories = []
        
        for item in self.category_list.get(0, tk.END):
            category, amount = item.split(': $')
            categories.append({
                'username': self.username,
                'period': period,
                'category': category.strip(),
                'budget': float(amount),
                'used': 0.0
            })
        
        new_budgets = pd.DataFrame(categories)
        self.budgets = pd.concat([self.budgets, new_budgets])
        self.budgets.to_csv('./budgets.csv', index=False)
        messagebox.showinfo("Success", "Budget saved!")
        self.update_chart()

    def update_chart(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        user_budgets = self.budgets[self.budgets['username'] == self.username]
        user_transactions = self.transactions[self.transactions['username'] == self.username]
        
        # Update used amounts from transactions
        for index, budget in user_budgets.iterrows():
            expenses = user_transactions[
                (user_transactions['description'].str.contains(budget['category'], case=False)) &
                (user_transactions['type'] == 'Expense')
            ]['amount'].sum()
            self.budgets.at[index, 'used'] = expenses
        
        if not user_budgets.empty:
            ax.pie(user_budgets['budget'], labels=user_budgets['category'], autopct='%1.1f%%')
            ax.set_title(f"Budget Overview - {user_budgets.iloc[0]['period']}")
            self.canvas.draw()