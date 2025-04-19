import tkinter as tk
from tkinter import messagebox
import hashlib
import pandas as pd
import os

class LoginApp:
    def __init__(self, root, success_callback):
        self.root = root
        self.root.title("Budget App Login")
        self.center_window(self.root, 300, 250)  # Center the root window
        
        self.success_callback = success_callback
        
        self.create_widgets()
        self.initialize_storage()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x}+{y}")


    def initialize_storage(self):
        if not os.path.exists('users.csv'):
            pd.DataFrame(columns=['username', 'password_hash']).to_csv('users.csv', index=False)
        if not os.path.exists('transactions.csv'):
            pd.DataFrame(columns=['username', 'date', 'description', 'amount', 'type']).to_csv('transactions.csv', index=False)
        if not os.path.exists('budgets.csv'):
            pd.DataFrame(columns=['username', 'period', 'category', 'budget', 'used']).to_csv('budgets.csv', index=False)

    def create_widgets(self):
        tk.Label(self.root, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register).pack(pady=10)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def login(self):
        username = self.username_entry.get()
        password = self.hash_password(self.password_entry.get())
        
        users = pd.read_csv('users.csv')
        user = users[users['username'] == username]
        
        if not user.empty and user.iloc[0]['password_hash'] == password:
            self.success_callback(username)
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register(self):
        username = self.username_entry.get()
        password = self.hash_password(self.password_entry.get())
        
        users = pd.read_csv('users.csv')
        if username in users['username'].values:
            messagebox.showerror("Error", "Username already exists")
            return
            
        users = pd.concat([users, pd.DataFrame([{'username': username, 'password_hash': password}])])
        users.to_csv('users.csv', index=False)
        messagebox.showinfo("Success", "Registration successful")
