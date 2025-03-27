import customtkinter as ctk
from dashboard import Dashboard

class Login_Page(ctk.CTk):
    def __init__(self):
        super().__init__()

        # app title and set size
        self.title("My PocketBook")
        self.geometry("500x400")

        # get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate center using set size
        center_x = int(screen_width/2 - 500/2)
        center_y = int(screen_height/2 - 400/2)

        # center items in center of screen
        self.geometry(f"500x400+{center_x}+{center_y}")
        self.grid_columnconfigure(0, weight=1)

        # app label + placement
        self.label = ctk.CTkLabel(self, text="My PocketBook", font=("Lora", 24, "bold"))
        self.label.grid(row=0, column=0, pady=(20,5))

        # email label + entry box 
        self.email_label = ctk.CTkLabel(self, text="Email:", font=("Lora", 16, "bold"))
        self.email_label.grid(row=1, column=0, pady=(20,5))
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.grid(row=2, column=0, padx=20, pady=5)

        # password label + entry box
        self.password_label = ctk.CTkLabel(self, text="Password:", font=("Lora", 16, "bold"))
        self.password_label.grid(row=3, column=0, pady=(20,5))
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.grid(row=4, column=0, padx=20, pady=5)

        # login button 
        self.login_button = ctk.CTkButton(self, text="Login", command=self.open_dashboard)
        self.login_button.grid(row=5, column=0, pady=20)

    # TODO: make sure both email and pwd are filled in order for login to work. 
    # maybe grey out the button until they fill out the boxes? also link user authentication here
    # function to open dashboard UI
    def open_dashboard(self):
        self.destroy()
        dashboard = Dashboard()
        dashboard.mainloop()

if __name__ == "__main__":
    app = Login_Page()
    app.mainloop()

