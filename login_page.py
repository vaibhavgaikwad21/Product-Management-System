import customtkinter as ctk
from tkinter import messagebox
import json
import os
import re  # Import regex module for email validation

USERS_FILE = "data/users.json"

def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_json(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


class LoginPage(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.configure(fg_color="#f5f6fa")

        title = ctk.CTkLabel(self, text="🔐 Welcome Back", font=("Arial", 22, "bold"), text_color="#2f3640")
        title.pack(pady=(25, 10))

        subtitle = ctk.CTkLabel(self, text="Login to continue", font=("Arial", 14), text_color="#718093")
        subtitle.pack(pady=(0, 20))

        # Email field
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email", width=300, height=40, corner_radius=12)
        self.email_entry.pack(pady=10)
        self.email_entry.bind("<Return>", lambda event: self.password_entry.focus())  # Enter moves to password

        # Password field
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", width=300, height=40, corner_radius=12)
        self.password_entry.pack(pady=10)
        self.password_entry.bind("<Return>", lambda event: self.login())  # Enter triggers login

        # Login Button
        self.login_btn = ctk.CTkButton(
            self, text="Login", width=300, height=40, corner_radius=12, fg_color="#273c75",
            hover_color="#192a56", command=self.login
        )
        self.login_btn.pack(pady=(15, 10))

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Input Error", "Please enter both email and password.")
            return

        # Simple email format validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return

        users = load_json(USERS_FILE)

        # Check if user exists
        user = next((u for u in users if u["email"] == email), None)

        if user:
            # User exists, check password
            if user["password"] == password:
                messagebox.showinfo("Login Success", "Welcome back!")
                if self.on_login_success:
                    self.on_login_success()
            else:
                messagebox.showerror("Login Failed", "Invalid password.")
        else:
            # New user, save credentials
            users.append({"email": email, "password": password})
            save_json(USERS_FILE, users)
            messagebox.showinfo("Registration Success", "New user registered and logged in!")
            if self.on_login_success:
                self.on_login_success()
