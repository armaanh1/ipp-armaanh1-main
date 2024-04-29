"""
Name: Armaan Hirani
UTEID: ah62954

On my honor, Armaan Hirani, this programming assignment is my own work
and I have not provided this code to any other student.

Complete the following:

0. What is your email in case I have issues while trying to install, run, and
use your program.

   email: hiraniarmaan@gmail.com

1. What is the purpose of your program?
 
2. List the major features of your program:

3. What 3rd party modules must be installed for the program to work?
   (Must be clear and explicit here or we won't be able to test your program.)
   
   If it is required to install 3rd party modules include the EXACT pip command.

4. List the things your learned while doing this program. Python features,
   techniques, third party modules, etc.

5. What was the most difficult thing you had to overcome or learn
   to get this program to work?
   
6. What features would you add next?

"""""

import tkinter as tk
from tkinter import messagebox
import hashlib
import re
import pickle
import time

class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        self.expenses = []
        self.income = []

        print('New User Creted: ', self.username + ' ' + self.password_hash)

# Dictionary to hold users
users = {}

class Expense:
    # Predefined categories
    CATEGORIES = ("Housing", "Transportation", "Food", "Utilities", "Clothing",
                  "Medical", "Insurance", "Household Items", "Personal", "Debt",
                  "Retirement", "Education", "Savings", "Gifts/Donations", "Entertainment")

    def __init__(self, title, amount, category, repeating=False, frequency=False):
        if category not in self.CATEGORIES:
            raise ValueError(f"Invalid category. Choose from: {', '.join(self.CATEGORIES)}")
        self.title = title
        self.amount = amount
        self.category = category
        self.repeating = repeating
        self.frequency = frequency

    def __repr__(self):
        return f"{self.title} - ${self.amount} - {self.category}"

class Income:
    def __init__(self, title, amount, repeating=False, frequency=False):
        self.title = title
        self.amount = amount
        self.repeating = repeating
        self.frequency = frequency

    def __repr__(self):
        return f"{self.title} - ${self.amount}"


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_password_secure(password):
    if not (8 <= len(password) <= 20):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!*\?^@#&]', password):
        return False
    return True

def save_data():
    with open('user_data.pkl', 'wb') as output:
        pickle.dump(users, output, pickle.HIGHEST_PROTOCOL)

    print('Saved Data: ', users)

def load_data():
    global users
    try:
        with open('user_data.pkl', 'rb') as input:
            users = pickle.load(input)
    except (FileNotFoundError, EOFError):
        users = {}

    print('Loaded Data: ', users)

class BudgetTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title('Simple Budget Tracker')
        master.geometry('800x300')
        self.center_window(800, 300)
        self.master.protocol("WM_DELETE_WINDOW", self.on_app_close)

        # Prevent resizing
        self.master.resizable(False, False)

        # Setup left and right frames
        self.left_frame = tk.Frame(master, width=400, height=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.left_frame.pack_propagate(False)  # Prevents frame shrinking

        self.right_frame = tk.Frame(master, width=400, height=300)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.right_frame.pack_propagate(False)

        # Text on the left frame
        self.initial_left_frame()

        # Initial buttons on the right frame
        self.initial_right_frame()

    def initial_left_frame(self):
        self.clear_left_frame()
        text_frame = tk.Frame(self.left_frame)
        text_frame.place(relx=0.5, rely=0.5, anchor='center')

        welcome_label = tk.Label(text_frame, text="Welcome to the Simple Budget Tracker!", font=('Montserrat', 14))
        welcome_label.grid(row=0, column=0, padx=20, pady=(20, 0))

        info_label = tk.Label(text_frame, text="This program helps you manage your finances by allowing you to log expenses and income. Register or log in to get started!",
                              font=('Montserrat', 14), wraplength=350, justify='center')
        info_label.grid(row=1, column=0, padx=20, pady=(0, 20))

        bottom_text = tk.Label(self.left_frame, font=('Montserrat', 12), text="<\\> with ❤️ in 📍 Austin, TX by Armaan Hirani")
        bottom_text.pack(side=tk.BOTTOM, pady=10)  # Positioning at the bottom with padding

    def initial_right_frame(self):
        self.clear_right_frame()
        button_frame = tk.Frame(self.right_frame)
        button_frame.pack(expand=True)
        
        register_button = tk.Button(button_frame, font=('Montserrat', 14), text='Register', command=self.register_form, height=2, width=20)
        register_button.pack(pady=10)
        login_button = tk.Button(button_frame, font=('Montserrat', 14), text='Login', command=self.login_form, height=2, width=20)
        login_button.pack(pady=10)
        quit_button = tk.Button(button_frame, font=('Montserrat', 14), text='Quit', command=self.master.quit, height=2, width=20)
        quit_button.pack(pady=10)

    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def clear_left_frame(self):
        for widget in self.left_frame.winfo_children():
            widget.destroy()

    def register_form(self):
        self.clear_right_frame()
        form_frame = tk.Frame(self.right_frame)
        form_frame.pack(expand=True)
        
        username_label = tk.Label(form_frame, font=('Montserrat', 14), text='Username:')
        username_label.pack()
        username_entry = tk.Entry(form_frame)
        username_entry.pack()
        password_label = tk.Label(form_frame, font=('Montserrat', 14), text='Password:')
        password_label.pack()
        password_entry = tk.Entry(form_frame, show='*')
        password_entry.pack()
        register_button = tk.Button(form_frame, font=('Montserrat', 14), text='Register', command=lambda: self.register_user(username_entry.get(), password_entry.get()))
        register_button.pack(pady=10)
        back_button = tk.Button(form_frame, font=('Montserrat', 14), text='Back', command=self.initial_right_frame)
        back_button.pack()

    def login_form(self):
        self.clear_right_frame()
        form_frame = tk.Frame(self.right_frame)
        form_frame.pack(expand=True)
        
        username_label = tk.Label(form_frame, font=('Montserrat', 14), text='Username:')
        username_label.pack()
        username_entry = tk.Entry(form_frame)
        username_entry.pack()
        password_label = tk.Label(form_frame, font=('Montserrat', 14), text='Password:')
        password_label.pack()
        password_entry = tk.Entry(form_frame, show='*')
        password_entry.pack()
        login_button = tk.Button(form_frame, font=('Montserrat', 14), text='Login', command=lambda: self.login_user(username_entry.get(), password_entry.get()))
        login_button.pack(pady=10)
        back_button = tk.Button(form_frame, font=('Montserrat', 14), text='Back', command=self.initial_right_frame)
        back_button.pack()

    def register_user(self, username, password):
        if username in users:
            messagebox.showerror("Error", "Username already exists")
            return
        if not is_password_secure(password):
            messagebox.showerror("Error", "Password is not secure")
            return
        password_hash = hash_password(password)
        users[username] = User(username, password_hash)

        self.setup_main_interface()

    def login_user(self, username, password):
        if username not in users:
            messagebox.showerror("Error", "Username does not exist")
            return
        password_hash = hash_password(password)
        if password_hash != users[username].password_hash:
            messagebox.showerror("Error", "Invalid password")
            return
        
        self.setup_main_interface()


    def center_window(self, width, height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')

    def setup_main_interface(self):
        self.clear_right_frame()
        self.clear_left_frame()  # Assuming you have a method to clear frames
        self.setup_pie_chart_frame()
        self.setup_right_interface()

    def setup_pie_chart_frame(self):
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        # Sample data
        labels = 'Rent', 'Groceries', 'Entertainment', 'Utilities'
        sizes = [215, 130, 245, 210]
        colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']

        # Pie chart setup
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        # Embedding in Tkinter
        chart = FigureCanvasTkAgg(fig, self.left_frame)
        chart.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def setup_right_interface(self):
        top_frame = tk.Frame(self.right_frame, height=75)  # Reduced height if needed
        top_frame.pack(side=tk.BOTTOM, fill=tk.X)  # Pack at the bottom of the right frame
        bottom_frame = tk.Frame(self.right_frame)
        bottom_frame.pack(fill=tk.BOTH, expand=True)  # Fill the remaining space

        # Setup buttons and transaction lists
        self.setup_top_buttons(top_frame)
        self.setup_transaction_lists(bottom_frame)

    def setup_top_buttons(self, frame):
        # This frame holds the buttons, positioned at the bottom of 'top_frame'
        button_frame = tk.Frame(frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)  # Use 'pady' for consistent padding from the frame edges

        edit_expenses_button = tk.Button(button_frame, text='Edit Expenses', command=self.add_edit_expense)
        edit_expenses_button.pack(side=tk.LEFT, padx=20, expand=True)  # Use 'expand' to evenly distribute

        edit_income_button = tk.Button(button_frame, text='Edit Income', command=self.add_edit_income)
        edit_income_button.pack(side=tk.RIGHT, padx=20, expand=True)

    def setup_transaction_lists(self, frame):
        left_list_frame = tk.Frame(frame)
        left_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_list_frame = tk.Frame(frame)
        right_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Center labels horizontally, keep default vertical alignment (top)
        expense_label = tk.Label(left_list_frame, text="Logged Expenses")
        expense_label.pack(pady=10, anchor='center')  # Horizontal center alignment, vertical padding for aesthetics

        income_label = tk.Label(right_list_frame, text="Logged Income")
        income_label.pack(pady=10, anchor='center')  # Horizontal center alignment, vertical padding for aesthetics

    def add_edit_expense(self):
        self.clear_right_frame()  # Clears existing widgets in the right frame
        form_frame = tk.Frame(self.right_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Category dropdown
        tk.Label(form_frame, text="Category:", font=('Montserrat', 12)).pack()
        category_var = tk.StringVar(form_frame)
        category_dropdown = tk.OptionMenu(form_frame, category_var, *Expense.CATEGORIES)
        category_dropdown.pack()

        # Title entry
        tk.Label(form_frame, text="Title:", font=('Montserrat', 12)).pack()
        title_entry = tk.Entry(form_frame)
        title_entry.pack()

        # Amount entry
        tk.Label(form_frame, text="Amount ($):", font=('Montserrat', 12)).pack()
        amount_entry = tk.Entry(form_frame)
        amount_entry.pack()

        # Repeating transaction setup
        repeat_var = tk.IntVar()
        repeat_check = tk.Checkbutton(form_frame, text="Mark as repeating", variable=repeat_var, command=lambda: self.toggle_repeating(form_frame, repeat_var))
        repeat_check.pack()

        # Submit button
        submit_button = tk.Button(form_frame, text="Save Expense", command=lambda: self.save_expense(title_entry.get(), amount_entry.get(), category_var.get(), repeat_var.get()))
        submit_button.pack(pady=10)


    def add_edit_income(self):
        self.clear_right_frame()
        form_frame = tk.Frame(self.right_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title entry
        tk.Label(form_frame, text="Title:", font=('Montserrat', 12)).pack()
        title_entry = tk.Entry(form_frame)
        title_entry.pack()

        # Amount entry
        tk.Label(form_frame, text="Amount ($):", font=('Montserrat', 12)).pack()
        amount_entry = tk.Entry(form_frame)
        amount_entry.pack()

        # Repeating transaction setup
        repeat_var = tk.IntVar()
        repeat_check = tk.Checkbutton(form_frame, text="Mark as repeating", variable=repeat_var, command=lambda: self.toggle_repeating(form_frame, repeat_var))
        repeat_check.pack()

        # Submit button
        submit_button = tk.Button(form_frame, text="Save Income", command=lambda: self.save_income(title_entry.get(), amount_entry.get(), repeat_var.get()))
        submit_button.pack(pady=10)

    def toggle_repeating(self, parent_frame, repeat_var):
        if repeat_var.get() == 1:
            self.repeating_frame = tk.Frame(parent_frame)
            self.repeating_frame.pack(pady=10)
            tk.Label(self.repeating_frame, text="Repeats every ").pack(side=tk.LEFT)
            self.repeat_days_entry = tk.Entry(self.repeating_frame, width=5)
            self.repeat_days_entry.pack(side=tk.LEFT)
            tk.Label(self.repeating_frame, text=" days").pack(side=tk.LEFT)

        else:
            self.repeating_frame.destroy()

    def save_expense(self, title='Expense', amount=0.0, category=None, repeat=None):
        # Implement logic to save the expense
        print(f"Saved Expense: {title}, Amount: {amount}, Category: {category}, Repeat: {repeat}")

        self.setup_main_interface()


    def save_income(self, title='Income', amount=0.0, repeat=None):
        # Implement logic to save the income
        print(f"Saved Income: {title}, Amount: {amount}, Repeat: {repeat}")

        self.setup_main_interface()

    def on_app_close(self):
        save_data()  # Call the function to save your data
        self.master.destroy()  # Ensures the application window is closed properly
        time.sleep(1)
        exit(0)

def main():
    load_data()
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
