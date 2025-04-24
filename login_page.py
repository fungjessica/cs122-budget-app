import tkinter as tk
from tkinter import messagebox
import hashlib
from models import User, Session, create_tables

class LoginApp:
    def __init__(self, root, success_callback):
        create_tables()  # ORM DB setup
        self.root = root
        self.root.title("Budget App Login")
        self.center_window(self.root, 300, 250)
        self.success_callback = success_callback
        self.create_widgets()

    def login(self):
        username = self.username_entry.get()
        password = self.hash_password(self.password_entry.get())
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        if user and user.password_hash == password:
            self.success_callback(username)
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Invalid credentials")
        session.close()

    def register(self):
        username = self.username_entry.get()
        password = self.hash_password(self.password_entry.get())
        session = Session()
        if session.query(User).filter_by(username=username).first():
            messagebox.showerror("Error", "Username already exists")
        else:
            new_user = User(username=username, password_hash=password)
            session.add(new_user)
            session.commit()
            messagebox.showinfo("Success", "Registration successful")
        session.close()

    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x}+{y}")

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
