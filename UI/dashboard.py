import customtkinter as ctk

class Dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        # app title and set size
        self.title("My PocketBook: Dashboard")
        self.geometry("500x600")

        # get screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # calculate center using set size
        center_x = int(screen_width/2 - 500/2)
        center_y = int(screen_height/2 - 600/2)

        # center items in center of screen
        self.geometry(f"500x600+{center_x}+{center_y}")
        self.grid_columnconfigure(0, weight=1)

        # total balance label + placement
        self.total_bal_label = ctk.CTkLabel(self, text="Total Balance: ", font=("Lora", 20, "bold"))
        self.total_bal_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        # income label + placement
        self.income_label = ctk.CTkLabel(self, text="Income: ", font=("Lora", 20, "bold"))
        self.income_label.grid(row=0, column=1, padx=20, pady=20, sticky="w")

        # transactions label + placement
        self.transactions_label = ctk.CTkLabel(self, text="Recent Transactions:", font=("Lora", 16, "bold"))
        self.transactions_label.grid(row=2, column=0, padx=20, pady=(20, 5), sticky="w")

        # transactions list + placement
        self.transactions_list = ctk.CTkLabel(self, font=("Lora", 14))
        self.transactions_list.grid(row=3, column=0, padx=20, pady=5, sticky="w")

        # expenses label + placement 
        self.expenses_label = ctk.CTkLabel(self, text="Expenses:", font=("Lora", 16, "bold"))
        self.expenses_label.grid(row=4, column=1, padx=20, pady=(20, 5), sticky="w")

        # expenses list + placement
        self.expenses_list = ctk.CTkLabel(self, font=("Lora", 14))
        self.expenses_list.grid(row=5, column=0, padx=20, pady=5, sticky="w")

        # TODO: fix navbar frame, try to make it anchored to the bottom
        # navbar frame + placement
        self.navbar_frame = ctk.CTkFrame(self, border_width=2, border_color="black", height=60)
        self.navbar_frame.grid(row=10, column=0, pady=(20,0), sticky="s", padx=20)

        # TODO: replace buttons with images 
        self.button1 = ctk.CTkButton(self.navbar_frame, text="button1")
        self.button1.grid(row=0, column=0, padx=10)

        


