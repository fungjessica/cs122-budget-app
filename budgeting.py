import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BudgetingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Budget")
        self.root.geometry("400x600")
        
        self.categories = ['Bills & Utilities', 'Dining & Drinks', 'Groceries', 'Others']
        self.spending = [51, 22, 15, 12]    # Percentages
        self.amounts = [984, 687, 450, 300] # Dollar amounts
        
        self.colors = ['#FF5733', '#33FF57', '#3357FF', '#FFC300']   # Pie chart colors
        
        self.create_title()
        self.create_pie_chart()
        #self.create_toggle_switch()
        self.create_budget_summary()
        
        
    def create_title(self):
        # Title at the top of the app
        tk.Label(self.root, text="Manage Budget", font=("Arial", 18, "bold")).pack(pady=10)
        
    def create_pie_chart(self):
        fig = Figure(figsize=(4,4), dpi=100)
        ax = fig.add_subplot(111)
        
        wedges, texts, autotexts = ax.pie(
            self.spending,
            labels=self.categories,
            autopct='%1.1f%%',
            startangle=90,
            colors=self.colors 
        )
        
        ax.set_title("Total spend in August: $3,121")
        
        chart_canvas = FigureCanvasTkAgg(fig, self.root)
        chart_canvas.get_tk_widget().pack()
        
    def toggle_include_bills(self):
        print("Toggle switched")
        
    def create_toggle_switch(self):
        toggle_frame = tk.Frame(self.root)
        toggle_frame.pack(pady=10)
        
        tk.Label(toggle_frame, text="Include bills").pack(side="left")
        
        toggle_button = tk.Checkbutton(toggle_frame, command=self.toggle_include_bills)
        toggle_button.pack(side="right")
        
    def create_budget_summary(self):
        details = [
            ("Bills & Utilities", "$984", "51% of spend"),
            ("Dining & Drinks", "687", "22% of spend"),
            ("Groceries", "$450", "15% of spend"),
            ("Others", "$300", "12% of spend"),
        ]
        
        for category, amount, percentage in details:
            frame = tk.Frame(self.root)
            frame.pack(fill="x", pady=5)
            
            tk.Label(frame, text=category, font=("Arial", 12)).pack(side="left")
            tk.Label(frame, text=f"{percentage}", font=("Arial", 10), fg="gray").pack(side="left", padx=10)
            tk.Label(frame, text=f"{amount}", font=("Arial", 12)).pack(side="right")