# login_page.py

import customtkinter as ctk
from tkinter import messagebox
from utils.file_manager import load_json

class LoginPage(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.master = master
        self.on_login_success = on_login_success
        self.pack(padx=40, pady=40, fill="both", expand=True)

        ctk.CTkLabel(self, text="🔐 Login", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(0, 20))

        # Username
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10)

        # Password
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        # Login button
        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=20)

    def login(self):
        user = self.username_entry.get()
        pwd = self.password_entry.get()
        if not user or not pwd:
            messagebox.showwarning("Input Error", "Username and password cannot be empty.")
            return

        data = load_json("login.json")

        if not isinstance(data, dict):
            data = {}

        if user in data and data[user] == pwd:
            self.on_login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
