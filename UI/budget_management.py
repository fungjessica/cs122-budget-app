import customtkinter as ctk

class Budget_Management(ctk.CTk):
    def __init__(self):
        
        # app title and set size
        self.title("My PocketBook: Charts")
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

        # dashboard label + placement
        self.label = ctk.CTkLabel(self, text="Budget Management", font=("Lora", 24, "bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)