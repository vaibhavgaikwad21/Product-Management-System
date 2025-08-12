import customtkinter as ctk
from PIL import Image, ImageTk
import plotly.graph_objects as go
import plotly.io as pio
import io
import json
import os
from collections import defaultdict

PRODUCTS_FILE = "data/products.json"
LOGO_PATH = "assets/logo.png"  # Change to your logo path


def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, "r") as f:
            return json.load(f)
    return []


class ChartsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.products = load_products()
        self.configure(fg_color="#F3F4F6")  # Match HomeTab background

        # ---------- Logo ----------
        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open(LOGO_PATH),
                size=(80, 80)
            )
            ctk.CTkLabel(self, image=logo_image, text="").pack(pady=(20, 10))
        except Exception as e:
            print(f"Logo not loaded: {e}")

        # ---------- Header ----------
        ctk.CTkLabel(
            self,
            text="📊Product Analytics Dashboard",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1E3A8A"
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            self,
            text="Visualize inventory trends, prices, and stock performance.",
            font=ctk.CTkFont(size=15),
            text_color="#374151"
        ).pack(pady=(0, 20))

        # ---------- Button Frame ----------
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        btn_style = {
            "corner_radius": 18,
            "width": 200,
            "height": 40,
            "fg_color": "#2563EB",
            "hover_color": "#1E40AF",
            "text_color": "white",
            "font": ctk.CTkFont(size=14, weight="bold")
        }

        buttons = [
            ("📦 Stock by Category", self.show_bar_chart),
            ("📈 Price Distribution", self.show_price_chart),
            ("↔️ Product Count", self.show_count_chart),
            ("📊 Price vs Stock", self.show_price_vs_stock),
            ("🥧 Stock Share (Pie)", self.show_stock_pie_chart),
            ("💰 Stock Value by Category", self.show_stock_value_chart)
        ]

        for i, (text, cmd) in enumerate(buttons):
            row, col = divmod(i, 3)
            ctk.CTkButton(btn_frame, text=text, command=cmd, **btn_style).grid(
                row=row, column=col, padx=15, pady=8
            )

        # ---------- Chart Display Frame ----------
        self.chart_frame = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=16,
            border_color="#E5E7EB",
            border_width=1
        )
        self.chart_frame.pack(padx=40, pady=30, fill="both", expand=True)

        self.chart_label = None

    # ---------------- Chart Functions ----------------
    def show_bar_chart(self):
        stock_by_cat = defaultdict(int)
        for p in self.products:
            try:
                stock_by_cat[p.get("category", "Unknown")] += int(p.get("stock", 0))
            except ValueError:
                pass

        categories = sorted(stock_by_cat.keys())
        stocks = [stock_by_cat[c] for c in categories]

        fig = go.Figure(go.Bar(
            x=categories, y=stocks,
            marker_color='#6366F1',
            text=stocks, textposition='auto'
        ))
        fig.update_layout(
            title='📦 Total Stock by Category',
            template='plotly_white',
            height=400,
            yaxis_title="Total Stock",
            xaxis_title="Category",
            xaxis=dict(tickangle=-30, automargin=True)
        )
        self.render_chart(fig)

    def show_price_chart(self):
        categories = sorted(set(p.get("category", "Unknown") for p in self.products))
        data = []
        for cat in categories:
            prices = [
                float(p.get("price", 0))
                for p in self.products if p.get("category", "Unknown") == cat
                and str(p.get("price", "0")).replace('.', '', 1).isdigit()
            ]
            if prices:
                data.append(go.Box(y=prices, name=cat))

        fig = go.Figure(data=data)
        fig.update_layout(
            title="📈 Price Distribution by Category",
            template='plotly_white',
            height=400,
            yaxis_title="Price (₹)",
            xaxis=dict(automargin=True)
        )
        self.render_chart(fig)

    def show_count_chart(self):
        count_by_cat = defaultdict(int)
        for p in self.products:
            count_by_cat[p.get("category", "Unknown")] += 1

        categories = sorted(count_by_cat.keys())
        counts = [count_by_cat[c] for c in categories]

        fig = go.Figure(go.Bar(
            y=categories, x=counts,
            orientation='h',
            marker_color='#8B5CF6',
            text=counts, textposition='auto'
        ))
        fig.update_layout(
            title='↔️ Product Count by Category',
            template='plotly_white',
            height=400,
            xaxis_title="Number of Products",
            yaxis_title="Category",
            yaxis=dict(automargin=True)
        )
        self.render_chart(fig)

    def show_price_vs_stock(self):
        prices, stocks, names = [], [], []
        for p in self.products:
            try:
                prices.append(float(p.get("price", 0)))
                stocks.append(int(p.get("stock", 0)))
                names.append(p.get("name", ""))
            except ValueError:
                pass

        fig = go.Figure(go.Scatter(
            x=prices, y=stocks,
            mode='markers+text',
            text=names,
            textposition='top center',
            marker=dict(size=10, color='#F59E0B', opacity=0.8)
        ))
        fig.update_layout(
            title="📊 Price vs Stock",
            template='plotly_white',
            height=400,
            xaxis_title="Price (₹)",
            yaxis_title="Stock"
        )
        self.render_chart(fig)

    def show_stock_pie_chart(self):
        stock_by_cat = defaultdict(int)
        for p in self.products:
            try:
                stock_by_cat[p.get("category", "Unknown")] += int(p.get("stock", 0))
            except ValueError:
                pass

        labels = sorted(stock_by_cat.keys())
        values = [stock_by_cat[l] for l in labels]

        fig = go.Figure(go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            textinfo='label+percent',
            insidetextorientation='radial'
        ))
        fig.update_layout(
            title="🥧 Stock Share by Category",
            template='plotly_white',
            height=400
        )
        self.render_chart(fig)

    def show_stock_value_chart(self):
        value_by_cat = defaultdict(float)
        for p in self.products:
            try:
                price = float(p.get("price", 0))
                stock = int(p.get("stock", 0))
                value_by_cat[p.get("category", "Unknown")] += price * stock
            except ValueError:
                pass

        categories = sorted(value_by_cat.keys())
        values = [round(value_by_cat[c], 2) for c in categories]

        fig = go.Figure(go.Bar(
            x=categories,
            y=values,
            marker_color='#10B981',
            text=[f"₹{v:,.2f}" for v in values],
            textposition='auto'
        ))
        fig.update_layout(
            title='💰 Total Stock Value by Category',
            template='plotly_white',
            height=400,
            yaxis_title="Total Value (₹)",
            xaxis_title="Category",
            xaxis=dict(tickangle=-30, automargin=True)
        )
        self.render_chart(fig)

    # ---------------- Render Chart ----------------
    def render_chart(self, fig):
        img_bytes = pio.to_image(fig, format='png', width=900, height=400, scale=1)
        img = Image.open(io.BytesIO(img_bytes))
        img_tk = ImageTk.PhotoImage(img)

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        self.chart_label = ctk.CTkLabel(self.chart_frame, image=img_tk, text="")
        self.chart_label.image = img_tk
        self.chart_label.pack(fill="both", expand=True, pady=10)
