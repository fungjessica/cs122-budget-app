from models import Transaction, Session, User
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TransactionApp:
    def __init__(self, root, username):
        self.session = Session()
        self.user = self.session.query(User).filter_by(username=username).first()
        self.root = root
        self.root.title("Transactions")
        self.root.configure(fg_color='#0A2647')
        self.center_window(self.root, 600, 600)
        self.create_widgets()
    
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x}+{y}")
        
    def add_entry(self):
        try:
            new_transaction = Transaction(
                date=datetime.strptime(self.entries['date'].get(), "%y-%m-%d"),
                description=self.entries['description'].get(),
                amount=float(self.entries['amount'].get()),
                type=self.entries['type'].get().capitalize(),
                user=self.user
            )
            self.session.add(new_transaction)
            self.session.commit()
            self.view_entries()
            messagebox.showinfo("Success", "Entry saved successfully!")
        except Exception as e:
            self.session.rollback()
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def monthly_summary(self):
        from sqlalchemy import extract, func
        summary = {}
        
        # Calculate income
        income = self.session.query(
            extract('month', Transaction.date).label('month'),
            func.sum(Transaction.amount)
        ).filter_by(user=self.user, type='Income').group_by('month').all()
        
        # Calculate expenses
        expenses = self.session.query(
            extract('month', Transaction.date).label('month'),
            func.sum(Transaction.amount)
        ).filter_by(user=self.user, type='Expense').group_by('month').all()

        # Combine results
        for month, amount in income:
            summary.setdefault(month, {'Income': 0, 'Expense': 0})['Income'] = amount
        for month, amount in expenses:
            summary.setdefault(month, {'Income': 0, 'Expense': 0})['Expense'] = amount

        # Display results in bar chart 
        summary_window = ctk.CTkToplevel(self.root)
        summary_window.title("Monthly Summary")

        months = sorted(summary.keys())
        income = [summary[m]['Income'] for m in months]
        expenses = [summary[m]['Expense'] for m in months]
        
        fig, ax = plt.subplots(figsize=(6,4))
        width = 0.35
        x = range(len(months))

        ax.bar(x, income, width=width, label='Income', color='green')
        ax.bar([i + width for i in x], expenses, width=width, label='Expense', color='red')

        ax.set_xlabel('Month')
        ax.set_ylabel('Amount')
        ax.set_title('Monthly Summary')
        ax.set_xticks([i + width/2 for i in x])
        ax.set_xticklabels([str(int(m)) for m in months])
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=summary_window)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def create_widgets(self):
        title_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        title_frame.pack(pady=(10, 5))
        ctk.CTkLabel(title_frame, text="Transaction Manager", font=("Helvetica", 20, "bold")).pack()
        ctk.CTkLabel(title_frame, text="Track your expenses and income below", font=("Helvetica", 14)).pack()

        search_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        search_frame.pack(pady=10)

        ctk.CTkLabel(search_frame, text="Search Transactions:", font=("Helvetica", 14)).pack(side="left", padx=10)
        self.search_entry = ctk.CTkEntry(search_frame, fg_color='white', text_color='black', border_color='white', placeholder_text='Search here')
        self.search_entry.bind("<KeyRelease>", self.check_search_input)
        self.search_entry.pack(side="left", padx=10)
        self.search_button = ctk.CTkButton(search_frame, text="Search", command=self.search_entries, fg_color='#205295', hover_color='#144272', font=("Helvetica", 14, "bold"), corner_radius=10, state=tk.DISABLED)
        self.search_button.pack(side="left", padx=10)

        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(pady=10)

        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.grid(row=0, column=0, padx=10, sticky="n")

        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=0, column=1, padx=10, sticky="n")

        self.viewer_frame = ctk.CTkFrame(self.root, fg_color="#102C57", corner_radius=10)
        self.viewer_frame.pack(padx=10)

        ctk.CTkLabel(self.viewer_frame, text="Your Transactions", font=("Helvetica", 16, "bold")).pack(pady=(10, 0))

        self.transaction_text = ctk.CTkTextbox(self.viewer_frame, font=("Helvetica", 12), width=450, height=200)
        self.transaction_text.pack(pady=10, padx=10)

        fields = [
            ("Date:", 'date', 'YY-MM-DD'),
            ("Description:", 'description', 'What is it?'),
            ("Amount:", 'amount', '$'),
            ("Type:", 'type', 'Income/Expense')
        ]

        self.entries = {}
        for i, (label_text, field, placeholder) in enumerate(fields):
            ctk.CTkLabel(form_frame, text=label_text, font=("Helvetica", 14)).grid(row=i, column=0, padx=10, pady=8, sticky="e")
            if field == 'type':
                type_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
                type_frame.grid(row=i, column=1, padx=10, pady=8, sticky="w")

                self.type_var = tk.StringVar()

                income_radio = ctk.CTkRadioButton(type_frame, text="Income", variable=self.type_var, value="Income")
                income_radio.pack(side="left", padx=5)

                expense_radio = ctk.CTkRadioButton(type_frame, text="Expense", variable=self.type_var, value="Expense")
                expense_radio.pack(side="left", padx=5)

                self.entries[field] = self.type_var
            else:
                entry = ctk.CTkEntry(form_frame, fg_color='white',
                    text_color='black', border_color='white', corner_radius=10,
                    placeholder_text=placeholder)
                entry.grid(row=i, column=1, padx=10, pady=8)
                self.entries[field] = entry

        ctk.CTkButton(button_frame, text="Add Entry", command=self.add_entry, fg_color='green', hover_color='darkgreen', font=("Helvetica", 14, "bold"), corner_radius=10).pack(pady=(0, 10))
        ctk.CTkButton(button_frame, text="View Entries", command=self.view_entries, fg_color='#205295', hover_color='#144272', font=("Helvetica", 14, "bold"), corner_radius=10).pack(pady=5)
        ctk.CTkButton(button_frame, text="Monthly Summary", command=self.monthly_summary, fg_color='#205295', hover_color='#144272', font=("Helvetica", 14, "bold"), corner_radius=10).pack(pady=(5, 0))

    def view_entries(self):
        self.transaction_text.delete("0.0", tk.END)
        transactions = self.session.query(Transaction).filter_by(user=self.user).all()
        for transaction in transactions:
            self.transaction_text.insert(tk.END,
                f"Date: {transaction.date}   |   Description: {transaction.description}   |   "
                f"Amount: {transaction.amount}   |   Type: {transaction.type}\n"
            )

    def search_entries(self):
        term = self.search_entry.get().lower()
        results = self.session.query(Transaction).filter(
            (Transaction.description.ilike(f"%{term}%")) |
            (Transaction.date.ilike(f"%{term}%")) |
            (Transaction.type.ilike(f"%{term}%"))
        ).all()

        self.transaction_text.delete("0.0", tk.END)
        
        for transaction in results:
            self.transaction_text.insert(tk.END,
                f"Date: {transaction.date}   |   Description: {transaction.description}   |   "
                f"Amount: {transaction.amount}   |   Type: {transaction.type}\n"
            )

    def check_search_input(self, event=None):
        if self.search_entry.get().strip(): 
            self.search_button.configure(state=tk.NORMAL)  
        else:
            self.search_button.configure(state=tk.DISABLED)  