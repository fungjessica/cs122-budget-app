from models import Budget, Session, User
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BudgetingApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Budgeting")
        self.username = username

        self.categories = [
            "Housing", "Utilities", "Food", "Transportation",
            "Insurance", "Entertainment", "Savings", "Miscellaneous"
        ]

        self.salary = 0
        self.recommended_budget = {}
        self.actual_spending = {}

        # CustomTkinter global appearance settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root.configure(fg_color="#0A2647")
        self.center_window(self.root, 600, 700)

        self.create_widgets()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        title_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        title_frame.pack(pady=(10, 5))
        ctk.CTkLabel(title_frame, text="Budget Manager", font=("Helvetica", 20, "bold")).pack()
        ctk.CTkLabel(title_frame, text="Plan your expenses and track your budget", font=("Helvetica", 14)).pack()

        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(pady=10)

        # Salary Input
        ctk.CTkLabel(main_frame, text="Enter your estimated monthly salary:", font=("Helvetica", 14)).pack(pady=5)
        self.salary_entry = ctk.CTkEntry(main_frame, fg_color='white', text_color='black', placeholder_text="Salary")
        self.salary_entry.pack(pady=5)
        ctk.CTkButton(main_frame, text="Set Salary", command=self.set_salary, fg_color="#1D4ED8", font=("Helvetica", 14, "bold"), corner_radius=10).pack(pady=10)

        # Category Selection
        ctk.CTkLabel(main_frame, text="Select a category:", font=("Helvetica", 14)).pack(pady=5)
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(main_frame, textvariable=self.category_var, values=self.categories, font=("Helvetica", 12))
        self.category_dropdown.pack(pady=5)

        # Amount Entry
        ctk.CTkLabel(main_frame, text="Enter amount spent:", font=("Helvetica", 14)).pack(pady=5)
        self.amount_entry = ctk.CTkEntry(main_frame, fg_color='white', text_color='black', placeholder_text="Amount")
        self.amount_entry.pack(pady=5)
        ctk.CTkButton(main_frame, text="Add Spending", command=self.add_spending, fg_color="#1D4ED8", font=("Helvetica", 14, "bold"), corner_radius=10).pack(pady=10)

        # Summary Section
        ctk.CTkLabel(main_frame, text="Summary:", font=("Helvetica", 16, "bold")).pack(pady=5)
        self.summary_text = tk.Text(main_frame, height=15, width=70, bg="#0A2647", fg="white", font=("Helvetica", 12))
        self.summary_text.pack(pady=10)

    def set_salary(self):
        try:
            self.salary = float(self.salary_entry.get())
            self.calculate_recommended_budget()
            messagebox.showinfo("Success", "Salary set and budget calculated!")
            self.update_summary()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for salary.")

    def calculate_recommended_budget(self):
        self.recommended_budget = {
            "Housing": self.salary * 0.30,
            "Utilities": self.salary * 0.10,
            "Food": self.salary * 0.15,
            "Transportation": self.salary * 0.10,
            "Insurance": self.salary * 0.10,
            "Entertainment": self.salary * 0.10,
            "Savings": self.salary * 0.15,
            "Miscellaneous": self.salary * 0.00
        }

    def add_spending(self):
        category = self.category_var.get()
        if category not in self.categories:
            messagebox.showerror("Error", "Please select a valid category.")
            return

        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for amount.")
            return

        if category in self.actual_spending:
            self.actual_spending[category] += amount
        else:
            self.actual_spending[category] = amount

        self.update_summary()

    def update_summary(self):
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, f"Salary: ${self.salary:.2f}\n\n")
        self.summary_text.insert(tk.END, "Category Summary:\n")

        for cat in self.categories:
            recommended = self.recommended_budget.get(cat, 0)
            actual = self.actual_spending.get(cat, 0)
            status = "✅" if actual <= recommended else "⚠️ Over Budget!"
            self.summary_text.insert(tk.END, f"{cat}: Recommended ${recommended:.2f} | Actual ${actual:.2f} {status}\n")
