import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime

try:
    df = pd.read_csv('./records.csv')
except Exception as e:
    data = {
        "Date": [],
        "Description": [],
        "Amount": [],
        "Type": []
    }
    
    df = pd.DataFrame(data)
    
class TransactionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Tracker")
        
        #Labels and Entries for input
        self.label_date = tk.Label(root, text="Date (YY-MM-DD):")
        self.label_date.grid(row=0, column=0)
        self.entry_date = tk.Entry(root)
        self.entry_date.grid(row=0, column=1)
        
        self.label_description = tk.Label(root, text="Description:")
        self.label_description.grid(row=1, column=0)
        self.entry_description = tk.Entry(root)
        self.entry_description.grid(row=1, column=1)
        
        self.label_amount = tk.Label(root, text="Amount:")
        self.label_amount.grid(row=2, column=0)
        self.entry_amount = tk.Entry(root)
        self.entry_amount.grid(row=2, column=1)
    
        self.label_type = tk.Label(root, text="Type (Income/Expense):")
        self.label_type.grid(row=3, column=0)
        self.entry_type = tk.Entry(root)
        self.entry_type.grid(row=3, column=1)
        
        #Buttons
        self.button_add = tk.Button(root, text="Add Entry", command=self.add_entry)
        self.button_add.grid(row=4, column=0, columnspan=2)
        
        self.button_view = tk.Button(root, text="View Entries", command=self.view_entries)
        self.button_view.grid(row=5, column=0, columnspan=2)
        
        self.button_search = tk.Button(root, text="Search Entries", command=self.search_entries)
        self.button_search.grid(row=6, column=0, columnspan=2)
        
        self.button_summary = tk.Button(root, text="Monthly Summary", command=self.monthly_summary)
        self.button_summary.grid(row=7, column=0, columnspan=2)
        
    def monthly_summary(self):
        global df
        summary_top = tk.Toplevel(self.root)
        summary_top.title("Monthly Summary")
        
        text = tk.Text(summary_top)
        text.pack()
        
        report_df = df.copy()
        report_df['Month'] = report_df['Date'].str.split('-').str[1].str.strip()
        
        monthly_income = report_df.query("Type == 'Income'").groupby("Month")['Amount'].sum()
        monthly_expense = report_df.query("Type == 'Expense'").groupby("Month")['Amount'].sum()

        
        summary_df  = pd.DataFrame({
            "Income":monthly_income,
            "Expense": monthly_expense
        }).fillna(0)
        
        #Convert columns to numeric ones
        summary_df['Income'] = pd.to_numeric(summary_df['Income'], errors='coerce')
        summary_df['Expense'] = pd.to_numeric(summary_df['Expense'], errors='coerce')
        
        summary_df['Savings'] = summary_df['Income'] - summary_df['Expense']
        
        text.insert(tk.END, summary_df.to_string())
        
    def search_entries(self):
        global df
        search_top = tk.Toplevel(self.root)
        search_top.title("Search Entries")
        
        search_label = tk.Label(search_top, text="Enter search criteria:")
        search_label.pack()
        
        self.search_entry = tk.Entry(search_top)
        self.search_entry.pack() 
        
        search_button = tk.Button(search_top, text="Search", command=self.perform_search)
        search_button.pack()
        
    def perform_search(self):
        global df
        search_term = self.search_entry.get().lower()
        filtered_df = df.query(f"Date.str.lower().str.contains('{search_term}') or Description.str.lower().str.contains('{search_term}')")
        
        results_top = tk.Toplevel(self.root)
        results_top.title("Search Results")
        
        text = tk.Text(results_top)
        text.pack()
        
        for index, row in filtered_df.iterrows():
            text.insert(tk.END, f"Date: {row['Date']}  |  Description: {row['Description']}  |  Amount: {row['Amount']}  |  Type: {row['Amount']} \n\n")
        
    def add_entry(self):
        #Retrieving data from the entries
        date = self.entry_date.get()
        description = self.entry_description.get()
        amount = self.entry_amount.get()
        entry_type = self.entry_type.get()
        
        #Validate and reformat date
        try:
            amount = float(self.entry_amount.get())
            date = self.entry_date.get()
            formatted_date = datetime.strptime(date, "%y-%m-%d").strftime("%y-%-m-%-d")
        except ValueError:
            if "could not convert string to float" in str(e):
                messagebox.showerror("Error", "Amount must be a valid number.")
            else:
                messagebox.showerror("Error", "Invalid date format. Use YY-MM-DD.")
            return
        
        # insert new data into db if not missing 
        if formatted_date and description and amount and entry_type:
            new_entry = pd.DataFrame({
                "Date": [formatted_date],
                "Description": [description],
                "Amount": [amount],
                "Type": [entry_type]
            })
            
            global df
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv('./records.csv', index=False)
            messagebox.showinfo("Success", "Entry saved sucessfully!" )
            
            self.entry_date.delete(0, tk.END)
            self.entry_description.delete(0, tk.END)
            self.entry_amount.delete(0, tk.END)
            self.entry_type.delete(0, tk.END)
            
        else:
            messagebox.showerror("Error", "All fields are required.")
        
        
    def view_entries(self):
        global df   #Global so you have access to dataframe
        self.top = tk.Toplevel(self.root)
        self.top.title("View Entries")
        
        text = tk.Text(self.top)
        text.pack()
        
        for index, row in df.iterrows():
            text.insert(tk.END, "Date: " + row['Date'] + "  |  Description: " + row['Description'] + "  |  Amount:" + str(row['Amount']) + "  |  Type: " + row['Type'] + "\n")
        
            edit_button = tk.Button(self.top, text="Edit", command = lambda i=index: self.edit_entry(i))
            delete_button = tk.Button(self.top, text="Delete", command = lambda i=index: self.delete_entry(i))
            text.window_create(tk.END, window=edit_button)
            text.window_create(tk.END, window=delete_button)
            text.insert(tk.END, "\n\n")
            
            
    def edit_entry(self, index):
        global df
        self.edit_top = tk.Toplevel(self.root)
        self.edit_top.title("Edit Entry")
        
        self.edit_date = tk.Entry(self.edit_top)
        self.edit_date.insert(0, df.at[index, 'Date']) #Getting data from a specific row
        self.edit_date.pack()
        
        self.edit_description = tk.Entry(self.edit_top)
        self.edit_description.insert(0, df.at[index, 'Description'])
        self.edit_description.pack()
        
        self.edit_amount = tk.Entry(self.edit_top)
        self.edit_amount.insert(0, df.at[index, 'Amount'])
        self.edit_amount.pack()
        
        self.edit_type = tk.Entry(self.edit_top)
        self.edit_type.insert(0, df.at[index, 'Type'])
        self.edit_type.pack()
        
        save_button = tk.Button(self.edit_top, text="Save", command= lambda i=index: self.save_edit(i))
        save_button.pack()
        
    def save_edit(self, index):
        global df
        
        # Get updated values from input fields
        date = self.edit_date.get()
        description = self.edit_description.get()
        amount = self.edit_amount.get()
        entry_type = self.edit_type.get()
        
        # Validate and reformat the date
        try:
            formatted_date = datetime.strptime(date, "%y-%m-%d").strftime("%y-%-m-%-d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format, YY-MM-DD.")
            return
        
        #Update DataFrame with new values
        df.at[index, 'Date'] = formatted_date
        df.at[index, 'Description'] = description
        df.at[index, 'Amount'] = amount
        df.at[index, 'Type'] = entry_type
        
        df.to_csv('./records.csv', index=False)
        messagebox.showinfo("Success", "Entry updated successfully!")
        self.edit_top.destroy()
        self.top.destroy()
        self.view_entries()

        
        
    def delete_entry(self,index):
        global df
        df.drop(index, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.to_csv('./records.csv', index=False)
        messagebox.showinfo("Success", "Entry deleted successfully")
        self.top.destroy()
        self.view_entries()

        
        

    