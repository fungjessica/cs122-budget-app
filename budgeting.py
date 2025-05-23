from models import Budget, Session, User
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


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
        self.center_window(self.root, 1000, 700)

        self.create_widgets()
        self.load_user_salary()
        self.load_budget_data()
        self.update_summary()


    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):
        title_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        title_frame.pack(pady=(10, 5))
        ctk.CTkLabel(title_frame, text="Budget Manager", font=("Helvetica", 22, "bold")).pack()
        ctk.CTkLabel(title_frame, text="Plan your expenses and track your budget", font=("Helvetica", 14)).pack()

        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.top_area_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.top_area_frame.pack(pady=10, fill="both", expand=True)

        self.salary_frame = ctk.CTkFrame(self.top_area_frame, fg_color="#102C57", corner_radius=10)
        self.salary_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.category_frame = ctk.CTkFrame(self.top_area_frame, fg_color="#102C57", corner_radius=10)
        self.category_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.top_area_frame.grid_columnconfigure(0, weight=1)
        self.top_area_frame.grid_columnconfigure(1, weight=1)
        self.top_area_frame.grid_rowconfigure(0, weight=1)

        self.summary_area_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        self.summary_area_frame.pack(pady=10, fill="both", expand=True)

        self.summary_frame = ctk.CTkFrame(self.summary_area_frame, fg_color="#102C57", corner_radius=10)
        self.summary_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.summary_area_frame.grid_columnconfigure(0, weight=1)
        self.summary_area_frame.grid_rowconfigure(0, weight=1)
        self.summary_area_frame.grid_columnconfigure(1, weight=1)


        ctk.CTkLabel(self.salary_frame, text="Enter your estimated monthly salary:", font=("Helvetica", 14)).pack(pady=(10, 5))
        self.salary_entry = ctk.CTkEntry(self.salary_frame, fg_color='white', text_color='black', placeholder_text="Salary")
        self.salary_entry.pack(pady=5, padx=20)
        ctk.CTkButton(self.salary_frame, text="Set Salary", command=self.set_salary, fg_color="#1D4ED8", font=("Helvetica", 14, "bold"), corner_radius=10).pack(pady=(10, 10))

        ctk.CTkLabel(self.category_frame, text="Select a category:", font=("Helvetica", 14)).pack(pady=(10, 5))
        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.category_frame, textvariable=self.category_var, values=self.categories, font=("Helvetica", 12))
        self.category_dropdown.pack(pady=5, padx=20)

        ctk.CTkLabel(self.category_frame, text="Enter amount spent:", font=("Helvetica", 14)).pack(pady=(10, 5))
        self.amount_entry = ctk.CTkEntry(self.category_frame, fg_color='white', text_color='black', placeholder_text="Amount")
        self.amount_entry.pack(pady=5, padx=20)
        ctk.CTkButton(self.category_frame, text="Add Spending", command=self.add_spending, fg_color="#1D4ED8", font=("Helvetica", 14, "bold"), corner_radius=10).pack(pady=(10, 10))
        
        ctk.CTkButton(
            self.category_frame,
            text="Reset Spending",
            command=self.reset_all_spending,
            fg_color="#DC2626",  # Red reset button
            font=("Helvetica", 14, "bold"),
            corner_radius=10
        ).pack(pady=(10, 10))


        ctk.CTkLabel(self.summary_frame, text="Summary", font=("Helvetica", 16, "bold")).pack(pady=(10, 0))
        self.summary_text = ctk.CTkTextbox(self.summary_frame, font=("Helvetica", 12))
        self.summary_text.pack(pady=10, padx=20, fill="both", expand=True)

    def set_salary(self):
        try:
            self.salary = float(self.salary_entry.get())
            # Save salary to DB
            session = Session()
            user = session.query(User).filter_by(username=self.username).first()
            user.salary = self.salary
            session.commit()
            
            self.calculate_recommended_budget()

            session = Session()
            user = session.query(User).filter_by(username=self.username).first()

            for cat, amount in self.recommended_budget.items():
                budget_entry = session.query(Budget).filter_by(user_id=user.id, category=cat, period="Monthly").first()
                if not budget_entry:
                    budget_entry = Budget(user_id=user.id, category=cat, period="Monthly", budget=amount, used=0)
                    session.add(budget_entry)
                else:
                    budget_entry.budget = amount  # update recommended amount

            session.commit()
            session.close()

            messagebox.showinfo("Success", "Salary set and budget saved!")
            self.load_budget_data()
            self.update_summary()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for salary.")
            
    def load_user_salary(self):
        session = Session()
        user = session.query(User).filter_by(username=self.username).first()
        self.salary = user.salary or 0.0
        session.close()

        # Show salary in entry box
        self.salary_entry.delete(0, tk.END)
        self.salary_entry.insert(0, str(self.salary))

    def calculate_recommended_budget(self):
        self.recommended_budget = {
            "Housing": self.salary * 0.30,
            "Utilities": self.salary * 0.10,
            "Food": self.salary * 0.15,
            "Transportation": self.salary * 0.10,
            "Insurance": self.salary * 0.10,
            "Entertainment": self.salary * 0.10,
            "Savings": self.salary * 0.15,
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

        session = Session()
        user = session.query(User).filter_by(username=self.username).first()
        budget_entry = session.query(Budget).filter_by(user_id=user.id, category=category, period="Monthly").first()

        if budget_entry:
            budget_entry.used += amount
        else:
            # If no budget set yet, create a new one
            budget_entry = Budget(user_id=user.id, category=category, period="Monthly", budget=0, used=amount)
            session.add(budget_entry)

        session.commit()
        session.close()

        self.load_budget_data()
        self.update_summary()
        
    def reset_all_spending(self):  
        session = Session()
        user = session.query(User).filter_by(username=self.username).first()
        budgets = session.query(Budget).filter_by(user_id=user.id, period="Monthly").all()

        confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all spending to $0?")
        if not confirm:
            session.close()
            return

        for b in budgets:
            b.used = 0

        session.commit()
        session.close()

        messagebox.showinfo("Reset Complete", "All spending has been reset to $0.")
        self.load_budget_data()
        self.update_summary()

        
    def load_budget_data(self):
        session = Session()
        user = session.query(User).filter_by(username=self.username).first()
        budgets = session.query(Budget).filter_by(user_id=user.id, period="Monthly").all()

        self.recommended_budget = {b.category: b.budget for b in budgets}
        self.actual_spending = {b.category: b.used for b in budgets}
        session.close()

    def update_summary(self):
        self.summary_text.delete("0.0", tk.END)

        self.summary_text.insert(tk.END, "--- Budget Summary ---\n\n")
        self.summary_text.insert(tk.END, f"Monthly Salary: ${self.salary:.2f}\n\n")
        self.summary_text.insert(tk.END, "Category Breakdown:\n\n")

        for cat in self.categories:
            recommended = self.recommended_budget.get(cat, 0)
            line = f"{cat:<15}     |     Recommended: ${recommended:>7.2f}\n"
            self.summary_text.insert(tk.END, line)

        self.summary_text.insert(tk.END, "\n" + "-"*60 + "\n")
        
        # Draw the pie chart after updating the summary
        self.draw_pie_chart()
        
    def draw_pie_chart(self):
        for widget in self.summary_area_frame.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.get_tk_widget().destroy()

        remaining_budget = []
        labels = []
        colors = [
            "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0",
            "#9966FF", "#FF9F40", "#66FF66", "#FF6666"
        ]

        for cat in self.categories:
            recommended = self.recommended_budget.get(cat, 0)
            actual = self.actual_spending.get(cat, 0)
            remaining = max(recommended - actual, 0)
            
            # Always show all categories
            remaining_budget.append(remaining)
            labels.append(cat)

        fig = Figure(figsize=(4, 4))
        ax = fig.add_subplot(111)
        wedges, texts, autotexts = ax.pie(
            remaining_budget,
            labels=labels,
            autopct="%1.1f%%",
            startangle=140,
            colors=colors
        )
        ax.set_title("Remaining Budget by Category", fontsize=14)

        chart = FigureCanvasTkAgg(fig, self.summary_area_frame)
        chart.get_tk_widget().grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
