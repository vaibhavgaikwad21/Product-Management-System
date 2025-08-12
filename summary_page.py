import customtkinter as ctk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta
import pandas as pd
import os
import json
from PIL import Image

PRODUCTS_FILE = "data/products.json"

def load_all_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    return []

class SummaryPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(fg_color="#f4f6f8")
        self.columns = [
            "name", "category", "brand", "unit", "price", "stock",
            "customer", "date", "sku", "expiry", "discount", "notes"
        ]
        self.create_ui()
        self.refresh_data()

    def create_ui(self):
        wrapper = ctk.CTkFrame(self, fg_color="#f4f6f8")
        wrapper.pack(expand=True, fill="both")

        try:
            logo = ctk.CTkImage(light_image=Image.open("assets/logo.png"), size=(60, 60))
            ctk.CTkLabel(wrapper, image=logo, text="").pack(pady=(20, 5))
        except Exception as e:
            print("Logo not found:", e)

        ctk.CTkLabel(wrapper, text="📜 Product Summary Dashboard", font=ctk.CTkFont(size=24, weight="bold"), text_color="#1E3A8A").pack()
        ctk.CTkLabel(wrapper, text="Visualize and export product data efficiently.", font=ctk.CTkFont(size=15), text_color="#374151").pack(pady=(0, 15))

        card = ctk.CTkFrame(wrapper, fg_color="#ffffff", corner_radius=20)
        card.pack(expand=True, fill="both", padx=40, pady=20)

        top_bar = ctk.CTkFrame(card, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=(15, 5))

        self.filter_var = ctk.StringVar()
        self.filter_box = ctk.CTkComboBox(
            top_bar,
            variable=self.filter_var,
            values=["All", "Today", "Yesterday", "Last 7 Days"],
            command=self.apply_filter,
            width=180,
            font=ctk.CTkFont(size=13),
            fg_color="#2563eb",
            border_color="#2563eb",
            button_color="#2563eb",
            text_color="white",
            dropdown_fg_color="white",
            dropdown_text_color="black"
        )
        self.filter_box.set("All")
        self.filter_box.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            top_bar,
            text="🔁 Refresh Summary",
            command=self.refresh_data,
            fg_color="#22c55e",
            hover_color="#16a34a",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=180,
            corner_radius=8
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            top_bar,
            text="💾 Export to Excel",
            command=self.export_to_excel,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=180,
            corner_radius=8
        ).pack(side="right")

        ctk.CTkLabel(card, text="📋 All Product Records", font=ctk.CTkFont(size=16, weight="bold"), text_color="#1f2937").pack(anchor="center", pady=(10, 5))

        table_frame = ctk.CTkFrame(card, fg_color="#f9fafb", corner_radius=12)
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=28)

        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings")

        for col in self.columns:
            heading_text = col.replace("_", " ").title()
            self.tree.heading(col, text=heading_text)
            self.tree.column(col, anchor="center", width=120)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ctk.CTkLabel(wrapper, text="© 2025 Shop Summary | Design by Vaibhav Gaikwad", font=ctk.CTkFont(size=12), text_color="#9ca3af").pack(pady=(0, 10))

    def display_products(self, data):
        self.tree.delete(*self.tree.get_children())
        for item in data:
            values = tuple(str(item.get(k, "")) for k in self.columns)
            self.tree.insert("", "end", values=values)

    def apply_filter(self, *_):
        choice = self.filter_var.get()
        today = datetime.today().date()
        yesterday = today - timedelta(days=1)
        self.filtered_products = []

        if choice == "All":
            self.filtered_products = self.products.copy()
        else:
            for item in self.products:
                date_str = item.get("date", "").strip()
                if not date_str or date_str.lower() == "n/a":
                    continue

                item_date = None
                for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
                    try:
                        item_date = datetime.strptime(date_str, fmt).date()
                        break
                    except ValueError:
                        continue

                if not item_date:
                    continue

                if choice == "Today" and item_date == today:
                    self.filtered_products.append(item)
                elif choice == "Yesterday" and item_date == yesterday:
                    self.filtered_products.append(item)
                elif choice == "Last 7 Days" and today - timedelta(days=7) <= item_date <= today:
                    self.filtered_products.append(item)

        self.display_products(self.filtered_products)

    def refresh_data(self):
        self.products = load_all_products()
        self.filter_var.set("All")
        self.filtered_products = self.products.copy()
        self.display_products(self.filtered_products)

    def export_to_excel(self):
        if not self.filtered_products:
            messagebox.showwarning("Warning", "No data to export.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel Files", "*.xlsx")],
            title="Save Summary Report"
        )
        if file_path:
            try:
                df = pd.DataFrame(self.filtered_products)
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Exported successfully:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed:\n{e}")
