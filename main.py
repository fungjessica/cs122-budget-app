import tkinter as tk
from login_page import LoginApp
from transactions import TransactionApp
from budgeting import BudgetingApp

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window initially
        self.show_login()

    def show_login(self):
        login_window = tk.Toplevel()
        LoginApp(login_window, self.login_success)

    def login_success(self, username):
        self.username = username
        self.show_main_menu()

    def show_main_menu(self):
        main_window = tk.Toplevel()
        main_window.title("Main Menu")
        
        # Set window size and center it manually
        window_width = 300
        window_height = 200
        screen_width = main_window.winfo_screenwidth()
        screen_height = main_window.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Buttons
        tk.Button(main_window, text="Manage Transactions",
                 command=lambda: TransactionApp(tk.Toplevel(), self.username)).pack(pady=10)
        tk.Button(main_window, text="Manage Budget",
                 command=lambda: BudgetingApp(tk.Toplevel(), self.username)).pack(pady=10)
        tk.Button(main_window, text="Exit",
                 command=self.root.destroy).pack(pady=10)

if __name__ == "__main__":
    MainApp().root.mainloop()
