import customtkinter as ctk
from utils.file_manager import load_json_data
import plotly.graph_objects as go
import plotly.io as pio
from PIL import Image, ImageTk
import io

class ChartsPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.products = load_json_data("data/product_data.json")

        # Title
        ctk.CTkLabel(
            self,
            text="📊 Product Stock & Price Charts",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)

        # Button Section
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame, text="📦 Stock Bar Chart",
            command=self.show_bar_chart,
            corner_radius=20, width=180
        ).grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            btn_frame, text="🍕 Stock Pie Chart",
            command=self.show_pie_chart,
            corner_radius=20, width=180
        ).grid(row=0, column=1, padx=10)

        ctk.CTkButton(
            btn_frame, text="💰 Price Bar Chart",
            command=self.show_price_chart,
            corner_radius=20, width=180
        ).grid(row=0, column=2, padx=10)

        # Chart Display Area
        self.chart_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=12)
        self.chart_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.chart_label = None

    def show_bar_chart(self):
        names = [p['name'] for p in self.products]
        stocks = [p['stock'] for p in self.products]

        fig = go.Figure(go.Bar(
            x=names,
            y=stocks,
            marker=dict(color='skyblue'),
            text=stocks,
            textposition='outside'
        ))
        fig.update_layout(
            title='📦 Product Stock Levels',
            xaxis_title='Products',
            yaxis_title='Stock',
            template='plotly_white',
            height=400
        )

        self.render_chart(fig)

    def show_pie_chart(self):
        names = [p['name'] for p in self.products]
        stocks = [p['stock'] for p in self.products]

        fig = go.Figure(go.Pie(
            labels=names,
            values=stocks,
            hole=0.4
        ))
        fig.update_layout(
            title='🍕 Stock Distribution by Product',
            template='plotly_dark',
            height=400
        )

        self.render_chart(fig)

    def show_price_chart(self):
        names = [p['name'] for p in self.products]
        prices = [p['price'] for p in self.products]

        fig = go.Figure(go.Bar(
            x=names,
            y=prices,
            marker=dict(color='lightgreen'),
            text=prices,
            textposition='outside'
        ))
        fig.update_layout(
            title='💰 Product Prices',
            xaxis_title='Products',
            yaxis_title='Price',
            template='plotly_white',
            height=400
        )

        self.render_chart(fig)

    def render_chart(self, fig):
        # Convert plotly figure to image for Tkinter
        img_bytes = pio.to_image(fig, format='png')
        img = Image.open(io.BytesIO(img_bytes))
        img_tk = ImageTk.PhotoImage(img)

        # Clear previous
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        self.chart_label = ctk.CTkLabel(self.chart_frame, image=img_tk, text="")
        self.chart_label.image = img_tk  # Prevent garbage collection
        self.chart_label.pack(fill="both", expand=True, pady=10)