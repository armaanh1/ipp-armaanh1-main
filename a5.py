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

class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        self.expenses = []
        self.income = []

        print('New User Creted: ', self.username + ' ' + self.password_hash)

# Dictionary to hold users
users = {}

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

class BudgetTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title('Simple Budget Tracker')
        master.geometry('800x300')
        self.center_window(800, 300)

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
        self.setup_left_frame()

        # Initial buttons on the right frame
        self.initial_right_frame()

    def setup_left_frame(self):
        text_frame = tk.Frame(self.left_frame)
        text_frame.place(relx=0.5, rely=0.5, anchor='center')

        welcome_label = tk.Label(text_frame, text="Welcome to the Simple Budget Tracker!", font=('Montserrat', 14))
        welcome_label.grid(row=0, column=0, padx=20, pady=(20, 0))

        info_label = tk.Label(text_frame, text="This program helps you manage your finances by allowing you to log expenses and income. Register or log in to get started!",
                              font=('Montserrat', 14), wraplength=350, justify='center')
        info_label.grid(row=1, column=0, padx=20, pady=(0, 20))

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
        messagebox.showinfo("Success", "Registration successful")
        self.initial_right_frame()

    def login_user(self, username, password):
        if username not in users:
            messagebox.showerror("Error", "Username does not exist")
            return
        password_hash = hash_password(password)
        if password_hash != users[username].password_hash:
            messagebox.showerror("Error", "Invalid password")
            return
        messagebox.showinfo("Success", "Login successful")
        self.initial_right_frame()

    def center_window(self, width, height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')

def main():
    root = tk.Tk()
    app = BudgetTrackerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
