# transactions.py (updated)
from models import Transaction, Session, User
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import messagebox, ttk

class TransactionApp:
    def __init__(self, root, username):
        self.session = Session()
        self.user = self.session.query(User).filter_by(username=username).first()
        self.root = root
        self.root.title("Transactions")
        self.center_window(self.root, 400, 400)
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

        # Display results
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Monthly Summary")
        text = tk.Text(summary_window)
        text.pack()
        
        for month in sorted(summary.keys()):
            income = summary[month]['Income']
            expense = summary[month]['Expense']
            savings = income - expense
            text.insert(tk.END, 
                f"Month {month}:\n"
                f"Income: ${income:.2f}\n"
                f"Expense: ${expense:.2f}\n"
                f"Savings: ${savings:.2f}\n\n"
            )

        # Keep original center_window method
        def center_window(self, window, width, height):
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = int((screen_width / 2) - (width / 2))
            y = int((screen_height / 2) - (height / 2))
            window.geometry(f"{width}x{height}+{x}+{y}")

    # Keep original widget creation
    def create_widgets(self):
        fields = [
            ("Date (YY-MM-DD):", 'date'),
            ("Description:", 'description'),
            ("Amount:", 'amount'),
            ("Type (Income/Expense):", 'type')
        ]
        
        self.entries = {}
        for i, (label_text, field) in enumerate(fields):
            tk.Label(self.root, text=label_text).grid(row=i, column=0, padx=5, pady=5)
            entry = tk.Entry(self.root)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[field] = entry

        tk.Button(self.root, text="Add Entry", command=self.add_entry).grid(row=4, columnspan=2, pady=10)
        tk.Button(self.root, text="View Entries", command=self.view_entries).grid(row=5, columnspan=2, pady=5)
        tk.Button(self.root, text="Search Entries", command=self.search_entries).grid(row=6, columnspan=2, pady=5)
        tk.Button(self.root, text="Monthly Summary", command=self.monthly_summary).grid(row=7, columnspan=2, pady=5)

    # Keep original view_entries UI
    def view_entries(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Entries")
        text = tk.Text(view_window)
        text.pack()
        
        transactions = self.session.query(Transaction).filter_by(user=self.user).all()
        for transaction in transactions:
            text.insert(tk.END,
                f"Date: {transaction.date} | Description: {transaction.description} | "
                f"Amount: {transaction.amount} | Type: {transaction.type}\n"
            )

    # Keep original search_entries UI
    def search_entries(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Entries")
        tk.Label(search_window, text="Search term:").pack(padx=5, pady=5)
        search_entry = tk.Entry(search_window)
        search_entry.pack(padx=5, pady=5)
        
        def perform_search():
            term = search_entry.get().lower()
            results = self.session.query(Transaction).filter(
                (Transaction.description.ilike(f"%{term}%")) |
                (Transaction.date.ilike(f"%{term}%")) |
                (Transaction.type.ilike(f"%{term}%"))
            ).all()
                
            result_window = tk.Toplevel(search_window)
            result_window.title("Search Results")
            text = tk.Text(result_window)
            text.pack()
                
            for transaction in results:
                text.insert(tk.END,
                    f"Date: {transaction.date} | Description: {transaction.description} | "
                    f"Amount: {transaction.amount} | Type: {transaction.type}\n"
                )
            
        tk.Button(search_window, text="Search", command=perform_search).pack(pady=5)
