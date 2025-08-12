import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from tkinter import ttk
import json
import os

PRODUCTS_FILE = "data/products.json"

def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_products(products):
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=4)

class ProductTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.products = load_products()
        self.selected_index = None
        self.configure(fg_color="#f4f6f8")  # light professional background
        self.create_widgets()
        self.refresh_tree()

    def create_widgets(self):
        # --- Wrapper Frame ---
        wrapper = ctk.CTkFrame(self, fg_color="#F3F4F6")
        wrapper.pack(expand=True, fill="both")

        # --- Logo ---
        try:
            logo = ctk.CTkImage(light_image=Image.open("assets/logo.png"), size=(60, 60))
            ctk.CTkLabel(wrapper, image=logo, text="").pack(pady=(20, 5))
        except Exception as e:
            print("Logo not found:", e)

        # --- Header ---
        ctk.CTkLabel(
            wrapper,
            text="📦 Product Management",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1E3A8A"
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            wrapper,
            text="Add, edit, delete, and manage your inventory effortlessly.",
            font=ctk.CTkFont(size=15),
            text_color="#374151"
        ).pack(pady=(0, 15))

        # --- Card Frame ---
        card = ctk.CTkFrame(wrapper, corner_radius=16, fg_color="#FFFFFF")
        card.pack(expand=True, fill="both", padx=40, pady=20)

        self.scrollable_frame = ctk.CTkScrollableFrame(card, fg_color="#FFFFFF")
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Title ---
        title = ctk.CTkLabel(
            self.scrollable_frame,
            text="📝 Product Entry Panel",
            font=("Segoe UI", 20, "bold"),
            text_color="#1f2937"
        )
        title.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="nsew")

        # --- Entry Fields ---
        self.fields = {
            "name": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Product Name"),
            "category": ctk.CTkComboBox(self.scrollable_frame, values=[
                "Grocery", "Clothes", "Accessories", "Home Appliances", "Electronics", "Stationery"]),
            "brand": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Brand"),
            "unit": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Unit"),
            "price": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Price"),
            "stock": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Stock"),
            "customer": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Customer Name"),
            "date": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Purchase Date (YYYY-MM-DD)"),
            "sku": ctk.CTkEntry(self.scrollable_frame, placeholder_text="SKU / Barcode (Optional)"),
            "expiry": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Expiry Date (Optional)"),
            "discount": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Discount % (Optional)"),
            "notes": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Notes (Optional)")
        }
        self.fields["category"].set("Grocery")

        field_order = [
            ("name", "category"),
            ("brand", "unit"),
            ("price", "stock"),
            ("customer", "date"),
            ("sku", "expiry"),
            ("discount", "notes")
        ]

        for row, (left, right) in enumerate(field_order, start=1):
            self.fields[left].grid(row=row, column=0, padx=20, pady=6, sticky="ew")
            self.fields[right].grid(row=row, column=1, padx=20, pady=6, sticky="ew")

        # --- Buttons (Styled) ---
        button_row = len(field_order) + 1

        button_style = {
            "text_color": "white",
            "font": ctk.CTkFont(size=14, weight="bold"),
            "corner_radius": 8
        }

        ctk.CTkButton(
            self.scrollable_frame,
            text="➕ Add Product",
            command=self.add_product,
            fg_color="#60a5fa",
            hover_color="#93c5fd",
            **button_style
        ).grid(row=button_row, column=0, pady=15, padx=10)

        ctk.CTkButton(
            self.scrollable_frame,
            text="🧹 Clear",
            command=self.clear_fields,
            fg_color="#fcd34d",
            hover_color="#fde68a",
            **button_style
        ).grid(row=button_row, column=1, pady=15, padx=10)

        ctk.CTkButton(
            self.scrollable_frame,
            text="📝 Update",
            command=self.update_product,
            fg_color="#25D366",
            hover_color="#6ee7b7",
            **button_style
        ).grid(row=button_row + 1, column=0, pady=5, padx=10)

        ctk.CTkButton(
            self.scrollable_frame,
            text="❌ Delete",
            command=self.delete_product,
            fg_color="#a78bfa",
            hover_color="#c4b5fd",
            **button_style
        ).grid(row=button_row + 1, column=1, pady=5, padx=10)

        # --- Treeview ---
        self.tree = ttk.Treeview(self.scrollable_frame, columns=tuple(self.fields.keys()), show="headings", height=12)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, anchor="center", width=120)
        self.tree.grid(row=button_row + 2, column=0, columnspan=2, pady=15, sticky="nsew")
        self.scrollable_frame.grid_rowconfigure(button_row + 2, weight=1)
        self.scrollable_frame.grid_columnconfigure((0, 1), weight=1)

        self.tree.bind("<ButtonRelease-1>", self.on_row_selected)

        # --- Footer ---
        ctk.CTkLabel(
            wrapper,
            text="© 2025 Shop Management System | Developed by Vaibhav Gaikwad",
            font=ctk.CTkFont(size=12),
            text_color="#9CA3AF"
        ).pack(pady=(0, 10))

    def clear_fields(self):
        for key, widget in self.fields.items():
            if isinstance(widget, ctk.CTkComboBox):
                widget.set("Grocery")
            else:
                widget.delete(0, "end")
        self.selected_index = None

    def add_product(self):
        new_product = {key: widget.get() for key, widget in self.fields.items()}
        if not new_product["name"] or not new_product["price"]:
            messagebox.showerror("Error", "Product Name and Price are required.")
            return
        try:
            new_product["price"] = float(new_product["price"])
            new_product["stock"] = int(new_product["stock"])
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a number and Stock must be an integer.")
            return
        self.products.append(new_product)
        save_products(self.products)
        self.refresh_tree()
        self.clear_fields()
        messagebox.showinfo("Success", "Product added successfully!")

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for index, p in enumerate(self.products):
            values = tuple(p.get(k, "") for k in self.fields.keys())
            self.tree.insert("", "end", iid=index, values=values)

    def on_row_selected(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            self.selected_index = int(selected_item)
            selected_data = self.tree.item(selected_item)["values"]
            for i, key in enumerate(self.fields):
                widget = self.fields[key]
                if isinstance(widget, ctk.CTkComboBox):
                    widget.set(selected_data[i])
                else:
                    widget.delete(0, "end")
                    widget.insert(0, selected_data[i])

    def update_product(self):
        if self.selected_index is None:
            messagebox.showwarning("Warning", "Select a product to update.")
            return
        updated_product = {key: widget.get() for key, widget in self.fields.items()}
        if not updated_product["name"] or not updated_product["price"]:
            messagebox.showerror("Error", "Product Name and Price are required.")
            return
        try:
            updated_product["price"] = float(updated_product["price"])
            updated_product["stock"] = int(updated_product["stock"])
        except ValueError:
            messagebox.showerror("Invalid Input", "Price must be a number and Stock must be an integer.")
            return
        self.products[self.selected_index] = updated_product
        save_products(self.products)
        self.refresh_tree()
        self.clear_fields()
        messagebox.showinfo("Success", "Product updated successfully!")

    def delete_product(self):
        if self.selected_index is None:
            messagebox.showwarning("Warning", "Select a product to delete.")
            return
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this product?")
        if confirm:
            self.products.pop(self.selected_index)
            save_products(self.products)
            self.refresh_tree()
            self.clear_fields()
            messagebox.showinfo("Deleted", "Product deleted successfully!")