# ✅ charts_page.py
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from utils.file_manager import load_json_data

class ChartsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.products = load_json_data("data/product_data.json")

        ctk.CTkLabel(self, text="📈 Product Stock & Price Charts", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        self.btn_bar = ctk.CTkButton(self, text="Bar Chart: Stock", command=self.show_bar_chart)
        self.btn_bar.pack(pady=5)

        self.btn_pie = ctk.CTkButton(self, text="Pie Chart: Stock Distribution", command=self.show_pie_chart)
        self.btn_pie.pack(pady=5)

        self.btn_price = ctk.CTkButton(self, text="Bar Chart: Price", command=self.show_price_chart)
        self.btn_price.pack(pady=5)

        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.pack(pady=10, fill="both", expand=True)

    def show_bar_chart(self):
        names = [p['name'] for p in self.products]
        stocks = [p['stock'] for p in self.products]
        fig, ax = plt.subplots()
        ax.bar(names, stocks, color='skyblue')
        ax.set_ylabel('Stock')
        ax.set_title('Product Stock Levels')
        self.render_chart(fig)

    def show_pie_chart(self):
        names = [p['name'] for p in self.products]
        stocks = [p['stock'] for p in self.products]
        fig, ax = plt.subplots()
        ax.pie(stocks, labels=names, autopct='%1.1f%%')
        ax.set_title('Stock Distribution by Product')
        self.render_chart(fig)

    def show_price_chart(self):
        names = [p['name'] for p in self.products]
        prices = [p['price'] for p in self.products]
        fig, ax = plt.subplots()
        ax.bar(names, prices, color='lightgreen')
        ax.set_ylabel('Price')
        ax.set_title('Product Prices')
        self.render_chart(fig)

    def render_chart(self, fig):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
