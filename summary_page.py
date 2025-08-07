# ✅ summary_page.py
import customtkinter as ctk
import json
import os
from tkinter import ttk, filedialog
from utils.file_manager import load_json_data

class SummaryPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.product_data = load_json_data("data/product_data.json")

        self.label = ctk.CTkLabel(self, text="📊 Product Summary", font=ctk.CTkFont(size=18, weight="bold"))
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("name", "stock", "price"), show="headings")
        self.tree.heading("name", text="Product")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("price", text="Price")
        self.tree.pack(padx=10, pady=5, fill="both", expand=True)

        self.export_button = ctk.CTkButton(self, text="Export to Excel", command=self.export_to_excel)
        self.export_button.pack(pady=10)

        self.load_products()

    def load_products(self):
        for product in self.product_data:
            self.tree.insert("", "end", values=(product["name"], product["stock"], product["price"]))

    def export_to_excel(self):
        import pandas as pd
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")
        if file_path:
            df = pd.DataFrame(self.product_data)
            df.to_excel(file_path, index=False)
