import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime

class TransactionApp:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Transactions")
        self.center_window(self.root, 400, 400)
        
        # Initialize data
        self.df = pd.DataFrame(columns=['username', 'date', 'description', 'amount', 'type'])
        self.load_data()
        
        # Create UI
        self.create_widgets()
        
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x}+{y}")

    def load_data(self):
        try:
            self.df = pd.read_csv('./transactions.csv')
        except FileNotFoundError:
            self.df = pd.DataFrame(columns=['username', 'date', 'description', 'amount', 'type'])

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

    def add_entry(self):
        try:
            entry_data = {
                'username': self.username,
                'date': datetime.strptime(self.entries['date'].get(), "%y-%m-%d").strftime("%y-%m-%d"),
                'description': self.entries['description'].get(),
                'amount': float(self.entries['amount'].get()),
                'type': self.entries['type'].get().capitalize()
            }
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
            return

        new_entry = pd.DataFrame([entry_data])
        self.df = pd.concat([self.df, new_entry], ignore_index=True)
        self.df.to_csv('./transactions.csv', index=False)
        
        messagebox.showinfo("Success", "Entry saved successfully!")
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def view_entries(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Entries")
        
        text = tk.Text(view_window)
        text.pack()
        
        user_transactions = self.df[self.df['username'] == self.username]
        for _, row in user_transactions.iterrows():
            text.insert(tk.END, 
                f"Date: {row['date']} | Description: {row['description']} | " 
                f"Amount: {row['amount']} | Type: {row['type']}\n"
            )

    def search_entries(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Entries")
        
        tk.Label(search_window, text="Search term:").pack(padx=5, pady=5)
        search_entry = tk.Entry(search_window)
        search_entry.pack(padx=5, pady=5)
        
        def perform_search():
            term = search_entry.get().lower()
            results = self.df[
                (self.df['description'].str.lower().str.contains(term)) |
                (self.df['date'].str.contains(term)) |
                (self.df['type'].str.lower().str.contains(term))
            ]
            
            result_window = tk.Toplevel(search_window)
            result_window.title("Search Results")
            
            text = tk.Text(result_window)
            text.pack()
            
            for _, row in results.iterrows():
                text.insert(tk.END, 
                    f"Date: {row['date']} | Description: {row['description']} | " 
                    f"Amount: {row['amount']} | Type: {row['type']}\n"
                )
        
        tk.Button(search_window, text="Search", command=perform_search).pack(pady=5)

    def monthly_summary(self):
        summary_window = tk.Toplevel(self.root)
        summary_window.title("Monthly Summary")
        
        user_transactions = self.df[self.df['username'] == self.username]
        user_transactions['month'] = user_transactions['date'].str.slice(0, 2)
        
        summary = user_transactions.groupby(['month', 'type'])['amount'].sum().unstack(fill_value=0)
        summary['Savings'] = summary.get('Income', 0) - summary.get('Expense', 0)
        
        text = tk.Text(summary_window)
        text.pack()
        text.insert(tk.END, summary.to_string())