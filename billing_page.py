import customtkinter as ctk
from tkinter import messagebox
import json
import os
from datetime import datetime
from PIL import Image
import webbrowser
from urllib.parse import quote
from utils.pdf_generator import generate_pdf

PRODUCTS_FILE = "data/products.json"  # Changed to match your Product page

def load_products():
    """Load product data from JSON file."""
    if os.path.exists(PRODUCTS_FILE):
        try:
            with open(PRODUCTS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            messagebox.showerror("Error", "products.json contains invalid JSON.")
    return []

class BillingPage(ctk.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.configure(fg_color="#f4f6f8")

        self.products = load_products()

        self.customer_name_var = ctk.StringVar()
        self.customer_contact_var = ctk.StringVar()
        self.product_var = ctk.StringVar()
        self.quantity_var = ctk.StringVar(value="1")
        self.gst_var = ctk.StringVar(value="18")
        self.discount_var = ctk.StringVar(value="5")

        self.bill_items = []
        self.pdf_path = None

        self.create_widgets()

    def create_widgets(self):
        wrapper = ctk.CTkFrame(self, fg_color="#F3F4F6")
        wrapper.pack(expand=True, fill="both")

        try:
            logo = ctk.CTkImage(light_image=Image.open("assets/logo.png"), size=(60, 60))
            ctk.CTkLabel(wrapper, image=logo, text="").pack(pady=(20, 5))
        except FileNotFoundError:
            messagebox.showwarning("Missing Logo", "Logo not found. PDF may be unbranded.")

        ctk.CTkLabel(
            wrapper,
            text="💸 Billing Page",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1E3A8A"
        ).pack(pady=(0, 5))

        ctk.CTkLabel(
            wrapper,
            text="Generate GST bills, apply discounts, export to PDF, and send via WhatsApp.",
            font=ctk.CTkFont(size=15),
            text_color="#374151"
        ).pack(pady=(0, 15))

        card = ctk.CTkFrame(wrapper, corner_radius=16, fg_color="#FFFFFF")
        card.pack(expand=True, fill="both", padx=40, pady=20)

        form_frame = ctk.CTkScrollableFrame(card, fg_color="#FFFFFF")
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        entry_style = {"fg_color": "white", "border_width": 1, "corner_radius": 6}

        # Customer Info
        ctk.CTkLabel(form_frame, text="🧍 Customer Information", font=("Segoe UI", 18, "bold"), text_color="#1f2937")\
            .grid(row=0, column=0, columnspan=2, pady=(5, 10), sticky="w")

        ctk.CTkLabel(form_frame, text="Customer Name:", font=("Segoe UI", 12, "bold"), text_color="#374151")\
            .grid(row=1, column=0, padx=20, sticky="w")
        self.customer_name_entry = ctk.CTkEntry(form_frame, textvariable=self.customer_name_var, placeholder_text="Customer Name", **entry_style)
        self.customer_name_entry.grid(row=2, column=0, padx=20, pady=6, sticky="ew")

        ctk.CTkLabel(form_frame, text="Contact No:", font=("Segoe UI", 12, "bold"), text_color="#374151")\
            .grid(row=1, column=1, padx=20, sticky="w")
        self.customer_contact_entry = ctk.CTkEntry(form_frame, textvariable=self.customer_contact_var, placeholder_text="Contact No", **entry_style)
        self.customer_contact_entry.grid(row=2, column=1, padx=20, pady=6, sticky="ew")

        # Product Selection
        ctk.CTkLabel(form_frame, text="📦 Product Selection", font=("Segoe UI", 18, "bold"), text_color="#1f2937")\
            .grid(row=3, column=0, columnspan=2, pady=(15, 10), sticky="w")

        ctk.CTkLabel(form_frame, text="Product:", font=("Segoe UI", 12, "bold"), text_color="#374151")\
            .grid(row=4, column=0, padx=20, sticky="w")
        product_names = [prod.get("name", "Unnamed") for prod in self.products] or ["No Products Available"]
        self.product_dropdown = ctk.CTkComboBox(form_frame, values=product_names, variable=self.product_var, **entry_style)
        self.product_dropdown.grid(row=5, column=0, padx=20, pady=6, sticky="ew")
        self.product_dropdown.set(product_names[0])

        ctk.CTkLabel(form_frame, text="Quantity:", font=("Segoe UI", 12, "bold"), text_color="#374151")\
            .grid(row=4, column=1, padx=20, sticky="w")
        self.quantity_entry = ctk.CTkEntry(form_frame, textvariable=self.quantity_var, placeholder_text="Quantity", **entry_style)
        self.quantity_entry.grid(row=5, column=1, padx=20, pady=6, sticky="ew")

        # Tax & Discount
        ctk.CTkLabel(form_frame, text="💰 Tax & Discounts", font=("Segoe UI", 18, "bold"), text_color="#1f2937")\
            .grid(row=6, column=0, columnspan=2, pady=(15, 10), sticky="w")

        ctk.CTkLabel(form_frame, text="GST (%):", font=("Segoe UI", 12, "bold"), text_color="#374151")\
            .grid(row=7, column=0, padx=20, sticky="w")
        self.gst_entry = ctk.CTkEntry(form_frame, textvariable=self.gst_var, placeholder_text="GST (%)", **entry_style)
        self.gst_entry.grid(row=8, column=0, padx=20, pady=6, sticky="ew")

        ctk.CTkLabel(form_frame, text="Discount (%):", font=("Segoe UI", 12, "bold"), text_color="#374151")\
            .grid(row=7, column=1, padx=20, sticky="w")
        self.discount_entry = ctk.CTkEntry(form_frame, textvariable=self.discount_var, placeholder_text="Discount (%)", **entry_style)
        self.discount_entry.grid(row=8, column=1, padx=20, pady=6, sticky="ew")

        # Buttons
        button_style = {
            "text_color": "white",
            "font": ctk.CTkFont(size=14, weight="bold"),
            "corner_radius": 8,
            "height": 40
        }

        self.add_to_bill_btn = ctk.CTkButton(form_frame, text="➕ Add to Bill", fg_color="#4ade80", hover_color="#86efac",
                              command=self.add_to_bill, **button_style)
        self.add_to_bill_btn.grid(row=9, column=0, pady=15, padx=10, sticky="ew")

        self.generate_bill_btn = ctk.CTkButton(form_frame, text="🧾 Generate Bill", fg_color="#60a5fa", hover_color="#93c5fd",
                              command=self.generate_bill, **button_style)
        self.generate_bill_btn.grid(row=9, column=1, pady=15, padx=10, sticky="ew")

        ctk.CTkButton(form_frame, text="💾 Export PDF", fg_color="#fcd34d", hover_color="#fde68a",
                      command=self.export_pdf, **button_style).grid(row=10, column=0, pady=5, padx=10, sticky="ew")
        ctk.CTkButton(form_frame, text="📲 Send WhatsApp", fg_color="#25D366", hover_color="#6ee7b7",
                      command=self.send_whatsapp, **button_style).grid(row=10, column=1, pady=5, padx=10, sticky="ew")

        ctk.CTkButton(form_frame, text="🧹 Clear", fg_color="#a78bfa", hover_color="#c4b5fd",
                      command=self.clear_bill, **button_style).grid(row=11, column=0, pady=5, padx=10, sticky="ew")
        ctk.CTkButton(form_frame, text="🔄 Refresh Products", fg_color="#fca5a5", hover_color="#fecaca",
                      command=self.refresh_products, **button_style).grid(row=11, column=1, pady=5, padx=10, sticky="ew")

        # Bill Display
        bill_frame = ctk.CTkFrame(form_frame, fg_color="#FFFFFF", corner_radius=8)
        bill_frame.grid(row=12, column=0, columnspan=2, pady=20, padx=20, sticky="nsew")

        self.bill_display = ctk.CTkTextbox(bill_frame, font=("Courier New", 12), fg_color="white", border_width=1)
        self.bill_display.pack(fill="both", expand=True, padx=5, pady=5)

        # Configure grid expansion
        form_frame.grid_columnconfigure((0, 1), weight=1)
        form_frame.grid_rowconfigure(12, weight=1)

    # ------------------ BILL LOGIC ------------------

    def add_to_bill(self):
        product_name = self.product_var.get()
        try:
            quantity = int(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid quantity.")
            return
        if not product_name or product_name == "No Products Available":
            messagebox.showwarning("Warning", "Please select a product.")
            return
        product = next((p for p in self.products if p.get("name") == product_name), None)
        if product:
            try:
                price = float(product.get("price", 0))
                total_price = round(price * quantity, 2)
                self.bill_items.append((product_name, quantity, price, total_price))
                self.update_bill_display()
            except (ValueError, TypeError):
                messagebox.showerror("Error", f"Invalid price for product: {product_name}")

    def update_bill_display(self):
        self.bill_display.delete("1.0", "end")
        self.bill_display.insert("end", f"{'Product':<20}{'Qty':<10}{'Price':<10}{'Total'}\n")
        self.bill_display.insert("end", "-" * 60 + "\n")
        for item in self.bill_items:
            name, qty, price, total = item
            self.bill_display.insert("end", f"{name:<20}{qty:<10}{price:<10.2f}{total:.2f}\n")
        self.bill_display.insert("end", "-" * 60 + "\n")

        subtotal = sum(item[3] for item in self.bill_items)
        gst_percent = float(self.gst_var.get() or 0)
        discount_percent = float(self.discount_var.get() or 0)
        gst_amount = subtotal * gst_percent / 100
        discount_amount = subtotal * discount_percent / 100
        final_amount = subtotal + gst_amount - discount_amount

        self.bill_display.insert("end", f"{'Subtotal:':>45} ₹{subtotal:.2f}\n")
        self.bill_display.insert("end", f"{'GST:':>45} ₹{gst_amount:.2f}\n")
        self.bill_display.insert("end", f"{'Discount:':>45} -₹{discount_amount:.2f}\n")
        self.bill_display.insert("end", f"{'Final Total:':>45} ₹{final_amount:.2f}")

    def generate_bill(self):
        name = self.customer_name_var.get()
        contact = self.customer_contact_var.get()
        if not name:
            messagebox.showwarning("Info Missing", "Enter customer name.")
            return
        if not self.bill_items:
            messagebox.showinfo("Empty", "No items in bill.")
            return

        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        subtotal = sum(item[3] for item in self.bill_items)
        gst_percent = float(self.gst_var.get() or 0)
        discount_percent = float(self.discount_var.get() or 0)
        gst_amount = subtotal * gst_percent / 100
        discount_amount = subtotal * discount_percent / 100
        final_amount = subtotal + gst_amount - discount_amount

        self.bill_display.delete("1.0", "end")
        self.bill_display.insert("end", f"Customer: {name}\nContact: {contact}\nDate: {now}\n\n")
        self.bill_display.insert("end", f"{'Product':<20}{'Qty':<10}{'Price':<10}{'Total'}\n")
        self.bill_display.insert("end", "-" * 60 + "\n")
        for pname, qty, price, total in self.bill_items:
            self.bill_display.insert("end", f"{pname:<20}{qty:<10}{price:<10.2f}{total:.2f}\n")
        self.bill_display.insert("end", "-" * 60 + "\n")
        self.bill_display.insert("end", f"{'Subtotal:':>45} ₹{subtotal:.2f}\n")
        self.bill_display.insert("end", f"{'GST:':>45} ₹{gst_amount:.2f}\n")
        self.bill_display.insert("end", f"{'Discount:':>45} -₹{discount_amount:.2f}\n")
        self.bill_display.insert("end", f"{'Final Total:':>45} ₹{final_amount:.2f}")
        messagebox.showinfo("Done", f"Bill generated for {name}.")

    def export_pdf(self):
        if not self.bill_items:
            messagebox.showwarning("Empty", "No items in the bill.")
            return
        name = self.customer_name_var.get()
        contact = self.customer_contact_var.get()
        if not name:
            messagebox.showwarning("Missing", "Enter customer name.")
            return
        try:
            gst = float(self.gst_var.get())
            discount = float(self.discount_var.get())
            pdf_path = generate_pdf(
                customer_name=name,
                customer_contact=contact,
                bill_items=self.bill_items,
                gst_percent=gst,
                discount_percent=discount,
                logo_path="assets/logo.png",
                shop_name="My Shop"
            )
            if pdf_path and os.path.exists(pdf_path):
                self.pdf_path = pdf_path
                messagebox.showinfo("Saved", f"PDF saved to:\n{pdf_path}")
            else:
                raise Exception("PDF not created.")
        except Exception as e:
            messagebox.showerror("Error", f"PDF generation failed:\n{str(e)}")

    def send_whatsapp(self):
        if not self.pdf_path or not os.path.exists(self.pdf_path):
            messagebox.showwarning("Missing", "Generate PDF first.")
            return
        contact = self.customer_contact_var.get()
        if not contact:
            messagebox.showwarning("Missing", "Enter customer contact.")
            return
        try:
            customer_name = self.customer_name_var.get()
            gst = float(self.gst_var.get())
            discount = float(self.discount_var.get())
            total_amt = round(sum(item[3] for item in self.bill_items), 2)

            product_lines = "\n".join([
                f"• {name} x{qty} = ₹{total:.2f}"
                for name, qty, price, total in self.bill_items
            ])

            marketing_note = (
                "🛍️ *Welcome to Prodexa !* 🛍️\n"
                "📦 From stock to billing, from summaries to sales charts — manage everything like a pro!\n"
                "🧾 Generate stunning GST bills, auto-apply discounts, and send them via WhatsApp in 1 click!\n"
                "💡 Smart analytics, sleek UI, and lightning-fast performance in one powerful package!\n"
                "🔔 Get low-stock alerts before you run out & keep your inventory game strong!\n"
                "👨‍💼 Perfect for shopkeepers, store owners, and anyone who loves control and clarity!\n"
                "✨ Try it once — and you'll wonder how you ever managed without it!"
            )

            thanks_note = (
                "\n🙏 *Thank you for buying from us!* 🙏\n"
                "We truly appreciate your support and look forward to serving you again. ❤️"
            )

            message = (
                f"{marketing_note}\n\n"
                f"🧾 *Invoice Details*\n"
                f"👤 Customer: {customer_name}\n"
                f"📦 Items:\n{product_lines}\n"
                f"➕ GST: {gst}%\n"
                f"➖ Discount: {discount}%\n"
                f"💰 Total Amount: ₹{total_amt:.2f}\n"
                f"📞 Contact: {contact}\n"
                f"⏰ Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n"
                f"{thanks_note}"
            )

            url = f"https://web.whatsapp.com/send?phone=+91{contact}&text={quote(message)}"
            webbrowser.open(url)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send WhatsApp message:\n{e}")

    def clear_bill(self):
        self.customer_name_var.set("")
        self.customer_contact_var.set("")
        self.product_var.set("")
        self.quantity_var.set("1")
        self.gst_var.set("18")
        self.discount_var.set("5")
        self.bill_items.clear()
        self.pdf_path = None
        self.bill_display.delete("1.0", "end")
        self.refresh_products()

    def refresh_products(self):
        self.products = load_products()
        product_names = [prod.get("name", "Unnamed") for prod in self.products] or ["No Products Available"]
        self.product_dropdown.configure(values=product_names)
        self.product_dropdown.set(product_names[0])
