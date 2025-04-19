import tkinter as tk
from login_page import LoginApp
from transactions import TransactionApp  # Import TransactionApp from transaction.py
from budgeting import BudgetingApp      # Import BudgetingApp from budgeting.py

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window initially
        self.show_login()

    def center_window(self, window, width, height):
        """Centers a given window on the screen."""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int((screen_width / 2) - (width / 2))
        y = int((screen_height / 2) - (height / 2))
        window.geometry(f"{width}x{height}+{x}+{y}")

    def show_login(self):
        login_window = tk.Toplevel()
        self.center_window(login_window, 300, 250)  # Center the login window
        LoginApp(login_window, self.login_success)

    def login_success(self, username):
        self.username = username
        self.show_main_menu()

    def show_main_menu(self):
        main_window = tk.Toplevel()
        main_window.title("Main Menu")
        self.center_window(main_window, 300, 200)  # Center the main menu window
        
        tk.Button(main_window, text="Manage Transactions", 
                  command=lambda: TransactionApp(tk.Toplevel(), self.username)).pack(pady=10)
        tk.Button(main_window, text="Manage Budget", 
                  command=lambda: BudgetingApp(tk.Toplevel(), self.username)).pack(pady=10)
        tk.Button(main_window, text="Exit", 
                  command=self.root.destroy).pack(pady=10)

if __name__ == "__main__":
    MainApp().root.mainloop()
