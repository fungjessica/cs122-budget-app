import tkinter as tk
import customtkinter as ctk
from login_page import LoginApp
from transactions import TransactionApp
from budgeting import BudgetingApp

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
        window_width = 300
        window_height = 200
        screen_width = main_window.winfo_screenwidth()
        screen_height = main_window.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Main Dashboard
        ctk.CTkButton(main_window, text="Manage Transactions",
                 command=lambda: TransactionApp(ctk.CTkToplevel(), self.username), fg_color='#205295', hover_color='#144272').pack(pady=10)
        ctk.CTkButton(main_window, text="Manage Budget",
                 command=lambda: BudgetingApp(ctk.CTkToplevel(), self.username), fg_color='#205295', hover_color='#144272').pack(pady=10)
        ctk.CTkButton(main_window, text="Exit",
                 command=self.root.destroy, fg_color=('red'), hover_color='darkred').pack(pady=10)

if __name__ == "__main__":
    MainApp().root.mainloop()
