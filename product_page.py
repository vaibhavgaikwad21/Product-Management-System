import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
import json
import os

PRODUCTS_FILE = "products.json"

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

        self.configure(fg_color="#f4f6f8")  # soft light background

        self.create_widgets()
        self.refresh_tree()

    def create_widgets(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self)
        self.scrollable_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Title
        title = ctk.CTkLabel(self.scrollable_frame, text="📦 Product Management", font=("Segoe UI", 24, "bold"), text_color="#1f2937")
        title.grid(row=0, column=0, columnspan=4, pady=(10, 20))

        # Entry fields
        self.fields = {
            "name": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Product Name"),
            "category": ctk.CTkComboBox(self.scrollable_frame, values=[
                "Grocery", "Clothes", "Accessories", "Home Appliances", "Electronics", "Stationery"]),
            "brand": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Brand"),
            "price": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Price"),
            "stock": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Stock"),
            "unit": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Unit"),
            "supplier": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Supplier Name"),
            "date": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Purchase Date (YYYY-MM-DD)"),
            "sku": ctk.CTkEntry(self.scrollable_frame, placeholder_text="SKU / Barcode (Optional)"),
            "expiry": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Expiry Date (Optional)"),
            "discount": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Discount % (Optional)"),
            "notes": ctk.CTkEntry(self.scrollable_frame, placeholder_text="Notes (Optional)")
        }

        # Arrange entries
        row, col = 1, 0
        for key, widget in self.fields.items():
            widget.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            col += 1
            if col >= 2:
                row += 1
                col = 0

        # Buttons
        ctk.CTkButton(self.scrollable_frame, text="➕ Add Product", command=self.add_product, fg_color="#2563eb", hover_color="#1d4ed8").grid(row=row+1, column=0, pady=15)
        ctk.CTkButton(self.scrollable_frame, text="🧹 Clear", command=self.clear_fields, fg_color="#9ca3af", hover_color="#6b7280").grid(row=row+1, column=1, pady=15)
        ctk.CTkButton(self.scrollable_frame, text="📝 Update", command=self.update_product, fg_color="#10b981", hover_color="#059669").grid(row=row+1, column=2, pady=15)
        ctk.CTkButton(self.scrollable_frame, text="❌ Delete", command=self.delete_product, fg_color="#ef4444", hover_color="#dc2626").grid(row=row+1, column=3, pady=15)

        # Treeview for product list
        self.tree = ttk.Treeview(self.scrollable_frame, columns=tuple(self.fields.keys()), show="headings", height=12)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, anchor="center", width=110)

        self.tree.grid(row=row+2, column=0, columnspan=4, pady=10, sticky="nsew")
        self.tree.bind("<ButtonRelease-1>", self.on_row_selected)

    def clear_fields(self):
        for key, widget in self.fields.items():
            if isinstance(widget, ctk.CTkComboBox):
                widget.set("")
            else:
                widget.delete(0, "end")
        self.selected_index = None

    def add_product(self):
        new_product = {key: widget.get() for key, widget in self.fields.items()}
        if not new_product["name"] or not new_product["price"]:
            messagebox.showerror("Error", "Product Name and Price are required.")
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
