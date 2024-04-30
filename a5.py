"""
Name: Armaan Hirani
UTEID: ah62954

On my honor, Armaan Hirani, this programming assignment is my own work
and I have not provided this code to any other student.

Complete the following:

0. What is your email in case I have issues while trying to install, run, and
use your program.

   email: hiraniarmaan@gmail.com
   MIKE: Ahmad faced an issue where programs built on the MacOS version of TKinter
   displayed incorrectly and he had to rerun them on Mac. I beleive this is also
   fixed when you try and resize the program, but my window is not resizable.

1. What is the purpose of your program?

    The purpose of this program is to help users manage their finances by allowing
    them to log expenses and income. Users can see a percentge breakdown of
    their ongoing expenses by category via a pie chart on the left side of the
    program. Users can also add, edit, and delete expenses and income streams.

2. List the major features of your program:

    - Users can register and log in to the program
    - Users can log expenses and income streams
    - Users can see a percentage breakdown of their expenses by category
    - Users can edit or delete expenses and income streams
    - Users can mark expenses and income streams as repeating and set a frequency
    - User data is serialized and saved to a file for persistence
    - Hashcodes are used to store user passwords securely

3. What 3rd party modules must be installed for the program to work?
   (Must be clear and explicit here or we won't be able to test your program.)

    - matplotlib
    - tk
    - autopep8 (not needed to run, but used to check for pep8 compliance)
        (can attribute most formatting issues to autopep8,
         but some were fixed manually)


   If it is required to install 3rd party modules include the EXACT pip command.

    pip install matplotlib
    pip install tk
    pip install autopep8

4. List the things your learned while doing this program. Python features,
   techniques, third party modules, etc.

    - I learned how to use the matplotlib library to create pie charts
    - I learned how to use the tkinter library to create GUIs advanced
      more advanced than those we developed in class
    - I learned how to use the pickle library to serialize data
    - I learned how to use the hashlib library to hash passwords securely
    - I learned how to use the re library to validate password strength
    - I learned more about lambda functions and how to use them in tkinter
    - I learned about how some more quirky parts of python syntax
      can be used to make code more concise and use less lines
    - Lastly, I learned how to use the treeview widget in tkinter to
      display and edit tabular data

5. What was the most difficult thing you had to overcome or learn
   to get this program to work?

    The most difficult thing i had to overcome was actually using/debugging
    TKinter. Even though we've had plenty of experience using the library in
    class, we followed a simialr structure through the assignments, as well as
    the fact that we were given a lot of the code to start with.

    In this project I had to start from scratch, and sadly, I had to do a lot of
    trial and error to get the program to work.

6. What features would you add next?

    The ability to delete users and their data, as well as the ability to
    visualize income streams in the pie chart would be one of the next features.

    Also considering users can track repeating expenses, it would be nice to
    be able to change the view to see the total expenses over a certain period of time.
    This was something listed in my original plan, but I over much trial and error,
    I was not able to implement it correctly, I just needed mroe time.

    Also my stretch goal from the beginning was to add a feature that would allow for
    users to generate pdf reports of their expenses and income streams.

"""""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import hashlib
import re
import pickle
import time


class User:
    """Class to represent a user."""

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        self.expenses = []
        self.income = []

        print('New User Created: ', self.username + ' ' + self.password_hash)


users = {}  # Dictionary to hold users


class Expense:
    """Class to represent an expense."""
    CATEGORIES = (
        "Housing",
        "Transportation",
        "Food",
        "Utilities",
        "Clothing",
        "Medical",
        "Insurance",
        "Household Items",
        "Personal",
        "Debt",
        "Retirement",
        "Education",
        "Savings",
        "Gifts/Donations",
        "Entertainment")

    def __init__(
            self,
            title,
            amount,
            category,
            repeating=False,
            frequency=None):
        if category not in self.CATEGORIES:
            raise ValueError(
                f"Invalid category. Choose from: {
                    ', '.join(
                        self.CATEGORIES)}")
        self.title = title
        self.amount = amount
        self.category = category
        self.repeating = repeating
        self.frequency = frequency

    def __repr__(self):
        return (f"{self.title} - ${self.amount} - {self.category} "
                f"- Repeating: {self.repeating} every {self.frequency} days")


class Income:
    """Class to represent an income stream."""

    def __init__(self, title, amount, repeating=False, frequency=None):
        self.title = title
        self.amount = float(amount)
        self.category = "Income"
        self.repeating = repeating
        self.frequency = frequency

    def __repr__(self):
        return (f"{self.title} - ${self.amount} - {self.category} - "
                f"Repeating: {self.repeating} every {self.frequency} days")


def hash_password(password):
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def is_password_secure(password):
    """Check if a password is secure."""
    if not (8 <= len(password) <= 20):
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!*?^@#&]', password):
        return False
    return True


def save_data():
    """Save user data to a file."""
    with open('user_data.pkl', 'wb') as output:
        pickle.dump(users, output, pickle.HIGHEST_PROTOCOL)
    for user in users.values():
        print(
            f'Saved User: {
                user.username}, Password Hash: {
                user.password_hash}, ' f'Expenses: {
                user.expenses}, Income: {
                    user.income}')


def load_data():
    """Load user data from a file."""
    global users
    try:
        with open('user_data.pkl', 'rb') as new_input:
            users = pickle.load(new_input)
            for user in users.values():
                print(
                    f'Loaded User: {
                        user.username}, Password Hash: {
                        user.password_hash}, Expenses: {
                        user.expenses}, ' f'Income: {
                        user.income}')
    except (FileNotFoundError, EOFError):
        users = {}


class BudgetTrackerApp:
    """Main class for the budget tracker application."""

    def __init__(self, master):
        self.master = master
        master.title('Simple Budget Tracker')
        master.geometry('800x300')
        self.center_window(800, 300)
        self.master.protocol("WM_DELETE_WINDOW", self.on_app_close)
        self.master.resizable(False, False)
        self.current_user = None

        self.left_frame = tk.Frame(master, width=400, height=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH)
        self.left_frame.pack_propagate(False)

        self.right_frame = tk.Frame(master, width=400, height=300)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.right_frame.pack_propagate(False)

        self.initial_left_frame()
        self.initial_right_frame()

    def initial_left_frame(self):
        """Initial setup for the left frame."""
        self.clear_left_frame()
        text_frame = tk.Frame(self.left_frame)
        text_frame.place(relx=0.5, rely=0.5, anchor='center')

        welcome_label = tk.Label(
            text_frame,
            text="Welcome to the Simple Budget Tracker!",
            font=(
                'Montserrat',
                14))
        welcome_label.grid(row=0, column=0, padx=20, pady=(20, 0))

        info_label = tk.Label(
            text_frame,
            text="This program helps you manage your finances by allowing you to log "
            "expenses and income. Register or log in to get started!",
            font=(
                'Montserrat',
                14),
            wraplength=350,
            justify='center')
        info_label.grid(row=1, column=0, padx=20, pady=(0, 20))

        bottom_text = tk.Label(
            self.left_frame,
            font=(
                'Montserrat',
                12),
            text="<\\> with ❤️ in 📍 Austin, TX by Armaan Hirani")
        bottom_text.pack(side=tk.BOTTOM, pady=10)

    def initial_right_frame(self):
        """Initial setup for the right frame."""
        self.clear_right_frame()
        button_frame = tk.Frame(self.right_frame)
        button_frame.pack(expand=True)

        register_button = tk.Button(
            button_frame,
            font=(
                'Montserrat',
                14),
            text='Register',
            command=self.register_form,
            height=2,
            width=20)
        register_button.pack(pady=10)
        login_button = tk.Button(
            button_frame,
            font=(
                'Montserrat',
                14),
            text='Login',
            command=self.login_form,
            height=2,
            width=20)
        login_button.pack(pady=10)
        quit_button = tk.Button(
            button_frame,
            font=(
                'Montserrat',
                14),
            text='Quit',
            command=self.master.quit,
            height=2,
            width=20)
        quit_button.pack(pady=10)

    def clear_right_frame(self):
        """Clear the right frame of all widgets."""
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def clear_left_frame(self):
        """Clear the left frame of all widgets."""
        for widget in self.left_frame.winfo_children():
            widget.destroy()

    def register_form(self):
        """Setup the registration form."""
        self.clear_right_frame()
        form_frame = tk.Frame(self.right_frame)
        form_frame.pack(expand=True)

        username_label = tk.Label(
            form_frame, font=(
                'Montserrat', 14), text='Username:')
        username_label.pack()
        username_entry = tk.Entry(form_frame)
        username_entry.pack()
        password_label = tk.Label(
            form_frame, font=(
                'Montserrat', 14), text='Password:')
        password_label.pack()
        password_entry = tk.Entry(form_frame, show='*')
        password_entry.pack()
        register_button = tk.Button(
            form_frame, font=(
                'Montserrat', 14), text='Register', command=lambda: self.register_user(
                username_entry.get(), password_entry.get()))
        register_button.pack(pady=10)
        back_button = tk.Button(
            form_frame,
            font=(
                'Montserrat',
                14),
            text='Back',
            command=self.initial_right_frame)
        back_button.pack()

    def login_form(self):
        """Setup the login form."""
        self.clear_right_frame()
        form_frame = tk.Frame(self.right_frame)
        form_frame.pack(expand=True)

        username_label = tk.Label(
            form_frame, font=(
                'Montserrat', 14), text='Username:')
        username_label.pack()
        username_entry = tk.Entry(form_frame)
        username_entry.pack()
        password_label = tk.Label(
            form_frame, font=(
                'Montserrat', 14), text='Password:')
        password_label.pack()
        password_entry = tk.Entry(form_frame, show='*')
        password_entry.pack()
        login_button = tk.Button(
            form_frame, font=(
                'Montserrat', 14), text='Login', command=lambda: self.login_user(
                username_entry.get(), password_entry.get()))
        login_button.pack(pady=10)
        back_button = tk.Button(
            form_frame,
            font=(
                'Montserrat',
                14),
            text='Back',
            command=self.initial_right_frame)
        back_button.pack()

    def register_user(self, username, password):
        """Register a new user."""
        if username in users:
            messagebox.showerror("Error", "Username already exists")
            return
        if not is_password_secure(password):
            messagebox.showerror("Error", "Password is not secure")
            return
        password_hash = hash_password(password)
        users[username] = User(username, password_hash)

        self.current_user = users[username]
        self.setup_main_interface()

    def login_user(self, username, password):
        """Log in an existing user."""
        if username not in users:
            messagebox.showerror("Error", "Username does not exist")
            return
        password_hash = hash_password(password)
        if password_hash != users[username].password_hash:
            messagebox.showerror("Error", "Invalid password")
            return

        self.current_user = users[username]

        print(f"Logged in as {username}")
        print(
            f"Current User: {
                self.current_user.username}, Password Hash: {
                self.current_user.password_hash}, \nExpenses: {
                self.current_user.expenses}, \nIncome: {
                    self.current_user.income} \n\n")

        self.setup_main_interface()

    def center_window(self, width, height):
        """Center the window on the screen."""
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')

    def setup_main_interface(self):
        """Setup the main interface after logging in."""
        """A method full of methods lmao, I think this is so funny"""
        self.clear_right_frame()
        self.clear_left_frame()  # Assuming you have a method to clear frames
        self.setup_pie_chart_frame()
        self.setup_right_interface()

    def setup_pie_chart_frame(self):
        """"Setup the pie chart frame on the left side of the window."""
        if not self.current_user:
            print("No current user logged in.")
            return

        user = self.current_user

        # Calculate sums for each category of expenses
        category_totals = {category: 0 for category in Expense.CATEGORIES}
        for expense in user.expenses:
            try:
                amount = float(expense.amount)  # Ensure amount is a float
                category_totals[expense.category] += amount
            except ValueError:
                continue  # Skip invalid data

        # Calculate total income
        total_income = sum(
            float(
                income.amount) for income in user.income if isinstance(
                income.amount, (int, float, str)) and str(
                income.amount).isdigit())

        labels = []
        sizes = []
        colors = []

        # Debugging output to check the values
        print(f"Total Income: {total_income}")
        print(f"Category Totals: {category_totals}")

        # Check if there are any expenses or income
        if total_income == 0 and not any(category_totals.values()):
            # If no expenses or income, display a gray placeholder pie
            labels = ['No Data']
            sizes = [1]
            colors = ['grey']
        else:
            if total_income > 0:
                labels.append('Income')
                sizes.append(total_income)
                colors.append('lightgreen')  # Bright green for income

            for category, total in category_totals.items():
                if total > 0:
                    labels.append(category)
                    sizes.append(total)
                    colors.append(None)  # Will set specific colors later

            expense_colors = [
                'gold',
                'yellowgreen',
                'lightcoral',
                'lightskyblue',
                'orange',
                'purple',
                'brown',
                'pink',
                'grey',
                'cyan',
                'magenta',
                'navy']
            color_index = 0
            for i, label in enumerate(labels):
                if label != 'Income':
                    colors[i] = expense_colors[color_index %
                                               len(expense_colors)]
                    color_index += 1

        fig, ax = plt.subplots()
        ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct=None,
            startangle=140)
        ax.axis('equal')

        chart = FigureCanvasTkAgg(fig, self.left_frame)
        chart.draw()
        chart.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def setup_right_interface(self):
        """Setup the right interface after logging in."""
        top_frame = tk.Frame(
            self.right_frame,
            height=75)  # Reduced height if needed
        # Pack at the bottom of the right frame
        top_frame.pack(side=tk.BOTTOM, fill=tk.X)
        bottom_frame = tk.Frame(self.right_frame)
        # Fill the remaining space
        bottom_frame.pack(fill=tk.BOTH, expand=True)

        # Setup buttons and transaction lists
        self.setup_top_buttons(top_frame)
        self.setup_transaction_lists(bottom_frame)

    def setup_top_buttons(self, frame):
        """Setup the buttons at the top of the 'top_frame'."""
        # This frame holds the buttons, positioned at the bottom of 'top_frame'
        button_frame = tk.Frame(frame)
        # Use 'pady' for consistent padding from the frame edges
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

        edit_expenses_button = tk.Button(
            button_frame,
            text='Edit Expenses',
            command=self.add_edit_expense)
        # Use 'expand' to evenly distribute
        edit_expenses_button.pack(side=tk.LEFT, padx=20, expand=True)

        edit_income_button = tk.Button(
            button_frame,
            text='Edit Income',
            command=self.add_edit_income)
        edit_income_button.pack(side=tk.RIGHT, padx=20, expand=True)

    def setup_transaction_lists(self, frame):
        """Setup the transaction lists in the 'bottom_frame'."""
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Montserrat', 12))

        # Combined transaction list setup
        self.transaction_tree = ttk.Treeview(
            frame,
            columns=(
                "Type",
                "Title",
                "Amount",
                "Category",
                "Timing"),
            show="headings",
            height=8)
        self.transaction_tree.column("Type", width=60, anchor="center")
        self.transaction_tree.column("Title", width=120, anchor="center")
        self.transaction_tree.column("Amount", width=100, anchor="e")
        self.transaction_tree.column("Category", width=120, anchor="center")
        self.transaction_tree.column("Timing", width=80, anchor="center")
        self.transaction_tree.heading("Type", text="Type")
        self.transaction_tree.heading("Title", text="Title")
        self.transaction_tree.heading("Amount", text="Amount ($)")
        self.transaction_tree.heading("Category", text="Category")
        self.transaction_tree.heading("Timing", text="Timing")
        self.transaction_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind double click event to handler
        self.transaction_tree.bind("<Double-1>", self.on_double_click)

        self.refresh_transactions()

    def on_double_click(self, event):
        """Handle double-click events to enable editing of treeview items."""
        """Handle double-click events to enable editing of treeview items."""
        region = self.transaction_tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.transaction_tree.identify_column(event.x)
            row = self.transaction_tree.identify_row(event.y)
            if column in ['#2', '#3', '#4', '#5']:  # Specify editable columns
                self.create_entry_widget(row, column)

    def create_entry_widget(self, item_id, column):
        """Create an entry widget for editing a treeview cell."""

        # Place an entry widget over the treeview cell for editing.
        x, y, width, height = self.transaction_tree.bbox(item_id, column)

        # Create an entry widget and position it to cover the cell
        entry = tk.Entry(self.transaction_tree, font=('Montserrat', 10))
        entry.place(x=x, y=y, width=width, height=height, anchor="nw")

        current_value = self.transaction_tree.set(item_id, column)
        entry.insert(0, current_value)
        entry.select_range(0, tk.END)
        entry.focus()

        def save_edit(_):
            new_value = entry.get()
            self.transaction_tree.set(
                item_id, column=column.replace(
                    '#', ''), value=new_value)
            self.update_data(item_id, column, new_value)
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda _: entry.destroy())

    def add_edit_expense(self):
        """Setup the form to add or edit an expense."""
        self.clear_right_frame()  # Clears existing widgets in the right frame
        form_frame = tk.Frame(self.right_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Category dropdown
        tk.Label(form_frame, text="Category:", font=('Montserrat', 12)).pack()
        category_var = tk.StringVar(form_frame)
        category_dropdown = tk.OptionMenu(
            form_frame, category_var, *Expense.CATEGORIES)
        category_dropdown.pack()

        # Title entry
        tk.Label(form_frame, text="Title:", font=('Montserrat', 12)).pack()
        title_entry = tk.Entry(form_frame)
        title_entry.pack()

        # Amount entry
        tk.Label(
            form_frame,
            text="Amount ($):",
            font=(
                'Montserrat',
                12)).pack()
        amount_entry = tk.Entry(form_frame)
        amount_entry.pack()

        # Repeating transaction setup
        repeat_var = tk.IntVar()
        repeat_check = tk.Checkbutton(
            form_frame,
            text="Mark as repeating",
            variable=repeat_var)
        repeat_check.pack()

        # Frequency entry if repeating
        frequency_label = tk.Label(
            form_frame, text="Frequency (days):", font=(
                'Montserrat', 12))
        frequency_label.pack()
        frequency_entry = tk.Entry(form_frame)
        frequency_entry.pack()

        # Submit button
        submit_button = tk.Button(
            form_frame,
            text="Save Expense",
            command=lambda: self.save_expense(
                title_entry.get(),
                amount_entry.get(),
                category_var.get(),
                repeat_var.get(),
                frequency_entry.get()))
        submit_button.pack(pady=10)

    def add_edit_income(self):
        """Setup the form to add or edit an income stream."""
        self.clear_right_frame()
        form_frame = tk.Frame(self.right_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title entry
        tk.Label(form_frame, text="Title:", font=('Montserrat', 12)).pack()
        title_entry = tk.Entry(form_frame)
        title_entry.pack()

        # Amount entry
        tk.Label(
            form_frame,
            text="Amount ($):",
            font=(
                'Montserrat',
                12)).pack()
        amount_entry = tk.Entry(form_frame)
        amount_entry.pack()

        # Repeating transaction setup
        repeat_var = tk.IntVar()
        repeat_check = tk.Checkbutton(
            form_frame,
            text="Mark as repeating",
            variable=repeat_var)
        repeat_check.pack()

        # Frequency entry if repeating
        frequency_label = tk.Label(
            form_frame, text="Frequency (days):", font=(
                'Montserrat', 12))
        frequency_label.pack()
        frequency_entry = tk.Entry(form_frame)
        frequency_entry.pack()

        # Submit button
        submit_button = tk.Button(
            form_frame,
            text="Save Income",
            command=lambda: self.save_income(
                title_entry.get(),
                amount_entry.get(),
                repeat_var.get(),
                frequency_entry.get()))
        submit_button.pack(pady=10)

    def save_expense(self, title, amount, category, repeat, frequency):
        """Save an expense to the current user."""
        repeat_status = bool(repeat)
        frequency_value = int(frequency) if repeat_status else None
        new_expense = Expense(
            title,
            amount,
            category,
            repeating=repeat_status,
            frequency=frequency_value)
        # Assuming 'current_user' is the logged-in user's username
        self.current_user.expenses.append(new_expense)
        print(f"Saved Expense: {new_expense}")
        print('all expenses: ', self.current_user.expenses)
        self.refresh_transactions()
        self.setup_main_interface()

    def save_income(self, title, amount, repeat, frequency):
        """Save an income stream to the current user."""
        repeat_status = bool(repeat)
        frequency_value = int(frequency) if repeat_status else None
        new_income = Income(
            title,
            amount,
            repeating=repeat_status,
            frequency=frequency_value)
        # Assuming 'current_user' is the logged-in user's username
        self.current_user.income.append(new_income)
        print(f"Saved Income: {new_income}")
        print('all income streams: ', self.current_user.income)
        self.refresh_transactions()
        self.setup_main_interface()

    def refresh_transactions(self):
        """Refresh the transaction treeview with the current user's data."""
        if hasattr(
                self,
                'transaction_tree') and self.transaction_tree.winfo_exists():
            self.transaction_tree.delete(*self.transaction_tree.get_children())
            for expense in self.current_user.expenses:
                timing = f"{
                    expense.frequency} days" if expense.repeating else "OT"
                self.transaction_tree.insert(
                    "",
                    "end",
                    values=(
                        "Expense",
                        expense.title,
                        expense.amount,
                        expense.category,
                        timing))
            for income in self.current_user.income:
                timing = f"{
                    income.frequency} days" if income.repeating else "OT"
                self.transaction_tree.insert(
                    "",
                    "end",
                    values=(
                        "Income",
                        income.title,
                        income.amount,
                        "Income",
                        timing))

    def update_data(self, item_id, column, new_value):
        """Update the underlying data based on edits made in the treeview."""
        item_values = self.transaction_tree.item(item_id, 'values')
        transaction_type = item_values[0]
        index = self.transaction_tree.index(item_id)

        if transaction_type == "Expense":
            transaction = self.current_user.expenses[index]
        else:
            transaction = self.current_user.income[index]

        column_index = int(column.strip('#')) - 1
        if column_index == 2:  # Title
            transaction.title = new_value
        elif column_index == 3:  # Amount
            transaction.amount = float(new_value)
        elif column_index == 4:  # Category
            transaction.category = new_value
        elif column_index == 5:  # Timing
            if new_value.upper() == "OT":
                transaction.repeating = False
                transaction.frequency = None
            else:
                transaction.repeating = True
                transaction.frequency = int(new_value.split()[0])

        save_data()

    def on_app_close(self):
        """Handle the window close event."""
        save_data()
        self.master.destroy()
        time.sleep(.2)
        exit(0)


def main():
    """Main function to run the budget tracker application."""
    load_data()
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()


if __name__ == '__main__':
    """Run the main function."""
    main()
