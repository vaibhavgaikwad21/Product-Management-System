import customtkinter as ctk
from tkinter import messagebox
from utils.file_manager import load_json_data
from utils.pdf_generator import generate_pdf
from datetime import datetime
import os

class BillingPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.products = load_json_data("data/product_data.json")
        self.cart = []

        self.label = ctk.CTkLabel(self, text="🧾 Billing / Invoice", font=ctk.CTkFont(size=18, weight="bold"))
        self.label.pack(pady=10)

        self.product_dropdown = ctk.CTkComboBox(self, values=[p["name"] for p in self.products])
        self.product_dropdown.pack(pady=5)
        if self.products:
            self.product_dropdown.set(self.products[0]["name"])

        self.quantity_entry = ctk.CTkEntry(self, placeholder_text="Quantity")
        self.quantity_entry.pack(pady=5)

        self.add_button = ctk.CTkButton(self, text="Add to Cart", command=self.add_to_cart)
        self.add_button.pack(pady=5)

        self.cart_box = ctk.CTkTextbox(self, height=200)
        self.cart_box.pack(pady=10, fill="both", expand=True)

        self.total_label = ctk.CTkLabel(self, text="Total: ₹0", font=ctk.CTkFont(size=14))
        self.total_label.pack(pady=5)

        self.generate_button = ctk.CTkButton(self, text="Generate Invoice", command=self.generate_invoice)
        self.generate_button.pack(pady=5)

    def add_to_cart(self):
        name = self.product_dropdown.get()
        qty = self.quantity_entry.get()
        if not qty.isdigit() or int(qty) <= 0:
            messagebox.showerror("Error", "Please enter a valid quantity.")
            return
        qty = int(qty)

        for product in self.products:
            if product["name"] == name:
                total_price = product["price"] * qty
                self.cart.append({"name": name, "qty": qty, "price": product["price"], "total": total_price})
                break
        self.update_cart_view()

    def update_cart_view(self):
        self.cart_box.delete("0.0", "end")
        total = 0
        for item in self.cart:
            self.cart_box.insert("end", f"{item['name']} x {item['qty']} = ₹{item['total']}\n")
            total += item['total']
        self.total_label.configure(text=f"Total: ₹{total}")

    def generate_invoice(self):
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty.")
            return
        buyer = f"Customer_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        filepath = os.path.join("data", f"{buyer}_invoice.pdf")
        total_amount = sum(item['total'] for item in self.cart)
        generate_pdf(filepath, self.cart, total_amount)
        messagebox.showinfo("Success", f"Invoice generated: {filepath}")
