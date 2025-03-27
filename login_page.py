import customtkinter as ctk

class login_page(ctk.CTk):

    def __init__(self):
        super().__init__()

        self = ctk.CTk()
        self.title("My PocketBook")
        self.geometry("500x400")

app = login_page()
app.mainloop()

