import customtkinter as ctk
import itertools
from PIL import Image
from login_page import LoginPage
import threading
import pyttsx3

class HomeTab(ctk.CTkFrame):
    def __init__(self, master, tab_view=None, login_callback=None):
        super().__init__(master)
        self.pack(expand=True, fill="both")
        self.tab_view = tab_view
        self.login_callback = login_callback
        self.configure(fg_color="#F3F4F6")

        # ---------- Top bar frame for login button ----------
        top_bar = ctk.CTkFrame(self, fg_color="#F3F4F6", height=40)
        top_bar.pack(fill="x", side="top")

        # Spacer to push login button to right
        top_bar.grid_columnconfigure(0, weight=1)

        # Load login icon (optional)
        try:
            login_icon_img = Image.open("assets/login_icon.png").resize((18, 18), Image.ANTIALIAS)
            self.login_icon = ctk.CTkImage(light_image=login_icon_img, size=(18, 18))
        except Exception:
            self.login_icon = None

        # Updated Login Button with emoji, bigger size, and matching navbar color
        self.login_btn = ctk.CTkButton(
            top_bar,
            text="🔑 Login",  # Added emoji
            width=180,        # Increased width
            height=45,        # Increased height
            fg_color="#2869F6",   # Matching professional navbar color (deep blue)
            hover_color="#3B82F6", # Slightly lighter blue on hover
            text_color="#FFFFFF",
            corner_radius=15,
            command=self.on_login_click,  # Click handler
            font=ctk.CTkFont(size=16, weight="bold"),  # Larger font
            border_width=0,
            image=self.login_icon,
            compound="left"
        )
        self.login_btn.grid(row=0, column=1, padx=20, pady=5, sticky="e")

        # Tooltip for login button
        self.login_btn.bind("<Enter>", lambda e: self.show_tooltip("Click here to login"))
        self.login_btn.bind("<Leave>", lambda e: self.hide_tooltip())

        self.tooltip = ctk.CTkLabel(
            top_bar,
            text="",
            font=ctk.CTkFont(size=10),
            fg_color="#111827",
            text_color="white",
            corner_radius=6
        )

        # ---------- Start welcome speech in a separate thread ----------
        threading.Thread(target=self.speak_welcome, daemon=True).start()

        # ---------- Main Scrollable Container ----------
        scroll_frame = ctk.CTkScrollableFrame(self, fg_color="#F3F4F6")
        scroll_frame.pack(fill="both", expand=True)

        # ---------- Load and Place Logo ----------
        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open("assets/logo.png"),
                size=(80, 80)
            )
            ctk.CTkLabel(scroll_frame, image=logo_image, text="").pack(pady=(20, 10))
        except Exception as e:
            print(f"Logo not loaded: {e}")

        # ---------- Header ----------
        ctk.CTkLabel(
            scroll_frame,
            text=" Prodexa Inventory Management System",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1E3A8A"
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            scroll_frame,
            text="Manage inventory, billing, analytics and reporting — all in one place.",
            font=ctk.CTkFont(size=15),
            text_color="#374151"
        ).pack(pady=(0, 25))

        # ---------- Animated Welcome Text ----------
        self.welcome_texts = itertools.cycle([
            "Built for small businesses, wholesalers, and retailers.",
            "Secure and efficient product tracking.",
            "Generate professional GST invoices in one click.",
            "Understand performance through visual analytics."
        ])
        self.animated_label = ctk.CTkLabel(
            scroll_frame,
            text="",
            font=ctk.CTkFont(size=13, slant="italic"),
            text_color="#6B7280"
        )
        self.animated_label.pack()
        self.animate_text()

        # ---------- Feature Panel Container ----------
        self.card_frame = ctk.CTkFrame(scroll_frame, fg_color="#FFFFFF", corner_radius=16)
        self.card_frame.pack(padx=40, pady=30, fill="both", expand=True)

        # ---------- Feature Panels ----------
        self.create_feature_panel(
            "📦 Product Management",
            "Add, update, search, and delete inventory items.",
            "#DBEAFE", "#BFDBFE", "Products"
        )
        self.create_feature_panel(
            "🧾 Billing System",
            "Create PDF invoices with tax and discount calculations.",
            "#FEF3C7", "#FDE68A", "Billing"
        )
        self.create_feature_panel(
            "📊 Data Analytics",
            "Track sales, trends, and generate visual reports.",
            "#DCFCE7", "#BBF7D0", "Charts"
        )
        self.create_feature_panel(
            "📋 Summary Reports",
            "Export data to Excel for audits and reports.",
            "#FDE2E4", "#FBCFE8", "Summary"
        )

        # ---------- Footer ----------
        ctk.CTkLabel(
            scroll_frame,
            text="© 2025 Shop Management System | Developed by Vaibhav Gaikwad",
            font=ctk.CTkFont(size=12),
            text_color="#9CA3AF"
        ).pack(pady=(10, 12))

        # Create LoginPage but don't show it yet
        self.login_page = LoginPage(master=self.master, on_login_success=self.on_login_success)

    def on_login_click(self):
        self.pack_forget()  # Hide HomeTab
        self.login_page.pack(fill="both", expand=True)  # Show LoginPage

    def on_login_success(self):
        self.login_page.pack_forget()  # Hide LoginPage
        self.pack(fill="both", expand=True)  # Show HomeTab again
        if self.login_callback:
            self.login_callback()

    def default_login_success(self):
        print("Login success callback not provided.")

    def show_tooltip(self, text):
        self.tooltip.configure(text=text)
        self.tooltip.place(x=self.login_btn.winfo_x(), y=self.login_btn.winfo_y() - 24)
        self.tooltip.lift()

    def hide_tooltip(self):
        self.tooltip.place_forget()

    def speak_welcome(self):
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.say("Welcome to the Prodexa Inventory Management System")
        engine.runAndWait()

    def animate_text(self):
        next_text = next(self.welcome_texts)
        self.animated_label.configure(text=next_text)
        self.after(3500, self.animate_text)

    def create_feature_panel(self, title, description, normal_color, hover_color, tab_name):
        panel = ctk.CTkFrame(
            self.card_frame,
            corner_radius=12,
            fg_color=normal_color,
            border_color="#E5E7EB",
            border_width=1
        )
        panel.pack(padx=20, pady=12, fill="x", expand=False)

        def fade_color(start, end, steps=10):
            start_rgb = self.hex_to_rgb(start)
            end_rgb = self.hex_to_rgb(end)
            diff = [(e - s) / steps for s, e in zip(start_rgb, end_rgb)]
            colors = [
                self.rgb_to_hex(
                    int(start_rgb[0] + diff[0] * i),
                    int(start_rgb[1] + diff[1] * i),
                    int(start_rgb[2] + diff[2] * i)
                )
                for i in range(steps + 1)
            ]
            return colors

        fade_in_colors = fade_color(normal_color, hover_color)
        fade_out_colors = fade_color(hover_color, normal_color)

        def on_enter(e):
            self.animate_panel_color(panel, fade_in_colors)

        def on_leave(e):
            self.animate_panel_color(panel, fade_out_colors)

        panel.bind("<Enter>", on_enter)
        panel.bind("<Leave>", on_leave)

        if self.tab_view:
            panel.bind("<Button-1>", lambda e: self.switch_tab(tab_name))

        lbl_title = ctk.CTkLabel(
            panel,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#111827"
        )
        lbl_title.pack(anchor="w", padx=20, pady=(15, 4))

        lbl_desc = ctk.CTkLabel(
            panel,
            text=description,
            font=ctk.CTkFont(size=13),
            text_color="#374151"
        )
        lbl_desc.pack(anchor="w", padx=20, pady=(0, 15))

        for widget in (lbl_title, lbl_desc):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)
            widget.bind("<Button-1>", lambda e: self.switch_tab(tab_name))

    def animate_panel_color(self, panel, color_steps, delay=15):
        def step(i=0):
            if i < len(color_steps):
                panel.configure(fg_color=color_steps[i])
                panel.after(delay, lambda: step(i + 1))
        step()

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def rgb_to_hex(self, r, g, b):
        return f"#{r:02X}{g:02X}{b:02X}"

    def switch_tab(self, tab_name):
        try:
            self.tab_view.set(tab_name)
        except Exception as e:
            print(f"Error switching tab: {e}")
