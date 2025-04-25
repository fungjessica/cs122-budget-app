import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import hashlib
from models import User, Session, create_tables
from PIL import Image

user_path = Image.open("icons/user(1).png")
password_path = Image.open("icons/padlock.png")

class LoginApp:

    def __init__(self, root, success_callback):
        create_tables()  # ORM DB setup
        self.root = root
        self.root.configure(fg_color='#0A2647')
        self.root.title("Budget App Login")
        self.center_window(self.root, 500, 450)
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
        ctk.CTkLabel(self.root, text="My PocketBook", font=("Helvetica", 20, "bold")).pack(pady=5)
        ctk.CTkLabel(self.root, text="Your BFF for all your budgeting needs!", font=("Helvetica", 18)).pack(pady=5)

        user_image = ctk.CTkImage(light_image=user_path, size=(30, 30))

        user_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        user_frame.pack(pady=10)

        userLabel = ctk.CTkLabel(user_frame, text="", image=user_image)
        userLabel.pack(side="left", padx=5)

        #ctk.CTkLabel(user_frame, text="Username:", font=("Helvetica", 16)).pack(side="left", padx=5)
        self.username_entry = ctk.CTkEntry(user_frame, placeholder_text="Username", fg_color='white', text_color='black', border_color='white')
        self.username_entry.pack(side="left", padx=5)

        password_image = ctk.CTkImage(light_image=password_path, size=(33,33))

        password_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        password_frame.pack(pady=10)

        passwordLabel = ctk.CTkLabel(password_frame, text="", image=password_image)
        passwordLabel.pack(side="left", padx=5)

        #ctk.CTkLabel(password_frame, text="Password:", font=("Helvetica", 16)).pack(side="left", padx=5)
        self.password_entry = ctk.CTkEntry(password_frame, show="*", placeholder_text="Password", fg_color='white', text_color='black', border_color='white')
        self.password_entry.pack(side="left", padx=5)

        ctk.CTkButton(self.root, text="Login", command=self.login, fg_color='#205295', hover_color='#144272', font=("Helvetica", 16, "bold")).pack(pady=10)
        ctk.CTkLabel(self.root, text="Don't have an account? Create one today!", font=("Helvetica", 16, "bold")).pack(pady=5)
        ctk.CTkButton(self.root, text="Register", command=self.register, fg_color=('green'), hover_color='darkgreen', font=("Helvetica", 16, "bold")).pack(pady=10)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
