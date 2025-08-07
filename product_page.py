import customtkinter as ctk
from tkinter import messagebox, filedialog
from tkinter.ttk import Treeview, Scrollbar
import datetime
import csv
from utils.file_manager import load_json, save_json

class ProductTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.products = load_json("data/product_data.json", default=[])

        ctk.CTkLabel(self, text="📦 Manage Products", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        # ----- Form Fields -----
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Product Name")
        self.price_entry = ctk.CTkEntry(self, placeholder_text="Price (₹)")
        self.stock_entry = ctk.CTkEntry(self, placeholder_text="Stock")
        self.category_entry = ctk.CTkEntry(self, placeholder_text="Product Category")
        self.buyer_entry = ctk.CTkEntry(self, placeholder_text="Buyer/Supplier Name")
        self.sku_entry = ctk.CTkEntry(self, placeholder_text="Barcode / SKU (optional)")
        self.date_entry = ctk.CTkEntry(self, placeholder_text="Purchase Date (YYYY-MM-DD)")
        
        for entry in [self.name_entry, self.price_entry, self.stock_entry, self.category_entry, self.buyer_entry, self.sku_entry, self.date_entry]:
            entry.pack(pady=4)

        # ----- Action Buttons -----
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Add Product", command=self.add_product).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Reset Fields", command=self.reset_fields).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Export CSV", command=self.export_csv).pack(side="left", padx=5)

        # ----- Product List (TreeView) -----
        self.tree = Treeview(self, columns=("Name", "Price", "Stock", "Category", "Buyer", "Date"), show="headings", height=10)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(padx=10, pady=10, fill="x")

        scrollbar = Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(in_=self.tree, relx=1.0, rely=0, relheight=1.0, bordermode="outside")

        # ----- Delete Button -----
        ctk.CTkButton(self, text="Delete Selected", fg_color="#ef4444", hover_color="#dc2626", command=self.delete_selected).pack(pady=5)

        # ----- Stats -----
        self.stats_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13))
        self.stats_label.pack(pady=10)

        self.refresh_tree()

    def add_product(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        stock = self.stock_entry.get()
        category = self.category_entry.get()
        buyer = self.buyer_entry.get()
        sku = self.sku_entry.get()
        date = self.date_entry.get() or str(datetime.date.today())

        if not (name and price.isdigit() and stock.isdigit()):
            messagebox.showerror("Error", "Please enter valid product details.")
            return

        product = {
            "name": name,
            "price": int(price),
            "stock": int(stock),
            "category": category,
            "buyer": buyer,
            "sku": sku,
            "date": date
        }

        self.products.append(product)
        save_json("data/product_data.json", self.products)
        self.refresh_tree()
        self.reset_fields()
        messagebox.showinfo("Success", f"{name} added successfully.")

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        low_stock = 0
        total_value = 0

        for p in self.products:
            name = p.get("name", "")
            price = int(p.get("price", 0))
            stock = int(p.get("stock", 0))
            category = p.get("category", "N/A")
            buyer = p.get("buyer", "N/A")
            date = p.get("date", "N/A")

            self.tree.insert("", "end", values=(name, price, stock, category, buyer, date))

            if stock <= 5:
                low_stock += 1
            total_value += price * stock

        self.stats_label.configure(
            text=f"🧮 Total Products: {len(self.products)} | 💰 Inventory Worth: ₹{total_value} | ⚠️ Low Stock: {low_stock}"
        )

    def delete_selected(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        item = self.tree.item(selected_item)["values"]
        name = item[0]
        self.products = [p for p in self.products if p["name"] != name]
        save_json("data/product_data.json", self.products)
        self.refresh_tree()
        messagebox.showinfo("Deleted", f"{name} has been deleted.")

    def reset_fields(self):
        for entry in [self.name_entry, self.price_entry, self.stock_entry,
                      self.category_entry, self.buyer_entry, self.sku_entry, self.date_entry]:
            entry.delete(0, "end")

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Price", "Stock", "Category", "Buyer", "SKU", "Date"])
            for p in self.products:
                writer.writerow([p["name"], p["price"], p["stock"], p["category"], p["buyer"], p["sku"], p["date"]])
        messagebox.showinfo("Exported", f"Products exported to {file_path}")
