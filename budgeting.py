from models import Budget, Session, User
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BudgetingApp:
    def __init__(self, root, username):
        self.session = Session()
        self.user = self.session.query(User).filter_by(username=username).first()
        self.root = root
        self.root.title("Budget Manager")
        self.center_window(self.root, 800, 600)
        self.create_widgets()
        self.update_chart()
        
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x}+{y}")
        
    def add_category(self):
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        if category and amount:
            self.category_list.insert(tk.END, f"{category}: ${amount}")
            self.category_entry.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)

    def save_budget(self):
        try:
            for item in self.category_list.get(0, tk.END):
                category, amount = item.split(': $')
                new_budget = Budget(
                    period=self.period_var.get(),
                    category=category.strip(),
                    budget=float(amount),
                    used=0.0,
                    user=self.user
                )
                self.session.add(new_budget)
            self.session.commit()
            messagebox.showinfo("Success", "Budget saved!")
            self.update_chart()
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"Error saving budget: {str(e)}")

    def update_chart(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        budgets = self.session.query(Budget).filter_by(user=self.user).all()
        if budgets:
            labels = [b.category for b in budgets]
            amounts = [b.budget for b in budgets]
            ax.pie(amounts, labels=labels, autopct='%1.1f%%')
            ax.set_title(f"Budget Overview - {budgets[0].period}")
            self.canvas.draw()


    # Keep original center_window method
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x}+{y}")

    # Keep original widget creation
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

    # Keep original budget UI components
    def create_budget_ui(self, parent):
        ctk.CTkLabel(parent, text="Budget Period:").grid(row=0, column=0, padx=10, pady=5)
        self.period_var = ctk.StringVar()
        ttk.Combobox(parent, textvariable=self.period_var,
                    values=["Month", "6 Months", "Year"]).grid(row=0, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="Category:").grid(row=1, column=0, padx=10, pady=5)
        self.category_entry = ctk.CTkEntry(parent)
        self.category_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(parent, text="Budget Amount:").grid(row=2, column=0, padx=10, pady=5)
        self.amount_entry = ctk.CTkEntry(parent)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ctk.CTkButton(parent, text="Add Category", command=self.add_category).grid(row=3, columnspan=2, pady=10)
        self.category_list = tk.Listbox(parent)
        self.category_list.grid(row=4, columnspan=2, padx=10, pady=5)
        
        ctk.CTkButton(parent, text="Save Budget", command=self.save_budget).grid(row=5, columnspan=2, pady=10)

    # Keep original chart UI components
    def create_view_ui(self, parent):
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, parent)
        self.canvas.get_tk_widget().pack(expand=True, fill='both')