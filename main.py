import tkinter as tk
import customtkinter as ctk
from login_page import LoginApp
from transactions import TransactionApp
from budgeting import BudgetingApp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image

# icons
growth_path = Image.open("icons/growth.png")
budget_path = Image.open("icons/asset-management.png")

class MainApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        #ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.withdraw()  # Hide the root window initially
        self.show_login()

    def show_login(self):
        login_window = ctk.CTkToplevel()
        LoginApp(login_window, self.login_success)

    def login_success(self, username):
        self.username = username
        self.show_main_menu()

    def show_main_menu(self):
        main_window = ctk.CTkToplevel()
        main_window.title("Main Menu")
        main_window.configure(fg_color='#0A2647')
        # Set window size and center it manually
        window_width = 500
        window_height = 400
        screen_width = main_window.winfo_screenwidth()
        screen_height = main_window.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # icon placement
        icon_frame = ctk.CTkFrame(main_window, fg_color="transparent")
        icon_frame.pack(pady=10)

        growth_icon = ctk.CTkImage(light_image=growth_path, size=(100, 100))
        budget_icon = ctk.CTkImage(light_image=budget_path, size=(100, 100))

        growth_label = ctk.CTkLabel(icon_frame, text="", image=growth_icon)
        growth_label.pack(side="left", padx=20)

        budget_label = ctk.CTkLabel(icon_frame, text="", image=budget_icon)
        budget_label.pack(side="left", padx=20)

        # Main Dashboard
        ctk.CTkLabel(
            main_window,
            text="Your PocketBook Dashboard",
            font=("Helvetica", 20, "bold")
        ).pack(pady=20)

        ctk.CTkButton(
            main_window,
            text="Manage Transactions",
            command=lambda: TransactionApp(ctk.CTkToplevel(), self.username),
            fg_color='#205295',
            hover_color='#144272',
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        ctk.CTkButton(
            main_window,
            text="Manage Budget",
            command=lambda: BudgetingApp(ctk.CTkToplevel(), self.username),
            fg_color='#205295',
            hover_color='#144272',
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)

        ctk.CTkButton(
            main_window,
            text="Exit",
            command=self.root.destroy,
            fg_color='red',
            hover_color='darkred',
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)

if __name__ == "__main__":
    MainApp().root.mainloop()
