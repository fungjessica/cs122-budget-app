import customtkinter as ctk

class Transaction_Screen(ctk.CTk):
    def __init__(self):
        
        # app title and set size
        self.title("My PocketBook: Transactions")
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

        # amount label + placement + entry box
        self.amount_label = ctk.CTkLabel(self, text="Amount ($):", font=("Lora", 20, "bold"))
        self.amount_label.grid(row=0, column=0, padx=20, pady=20)
        self.amount_entry = ctk.CTkEntry(self)
        self.amount_entry.grid(row=0, column=1, padx=20, pady=5)

        # date label + placement + entry box
        self.date_label = ctk.CTkLabel(self, text="Date:", font=("Lora", 20, "bold"))
        self.date_label.grid(row=1, column=0, padx=20, pady=20)
        self.date_entry = ctk.CTkEntry(self)
        self.date_entry.grid(row=1, column=1, padx=20, pady=5)

        # category label + placement + entry box
        self.category_label = ctk.CTkLabel(self, text="Category:", font=("Lora", 20, "bold"))
        self.category_label.grid(row=2, column=0, padx=20, pady=20)
        self.category_entry = ctk.CTkEntry(self)
        self.category_entry.grid(row=2, column=1, padx=20, pady=5)

        # description label + placement + entry box
        self.description_label = ctk.CTkLabel(self, text="Description:", font=("Lora", 20, "bold"))
        self.description_label.grid(row=3, column=0, padx=20, pady=20)
        self.description_entry = ctk.CTkEntry(self)
        self.description_entry.grid(row=3, column=1, padx=20, pady=5)

