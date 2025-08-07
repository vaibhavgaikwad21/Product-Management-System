import customtkinter as ctk
import itertools
from PIL import Image

class HomeTab(ctk.CTkFrame):
    def __init__(self, master, tab_view=None):
        super().__init__(master)
        self.pack(expand=True, fill="both")
        self.tab_view = tab_view  # optional tab view reference for navigation
        self.configure(fg_color="#F3F4F6")  # Light neutral background

        # ---------- Load and Place Logo ----------
        try:
            logo_image = ctk.CTkImage(
                light_image=Image.open("assets/logo.png"),
                size=(80, 80)
            )
            ctk.CTkLabel(self, image=logo_image, text="").pack(pady=(20, 10))
        except Exception as e:
            print(f"Logo not loaded: {e}")

        # ---------- Header ----------
        ctk.CTkLabel(
            self,
            text="Shop Product Management System",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#1E3A8A"  # Indigo-900
        ).pack(pady=(0, 8))

        ctk.CTkLabel(
            self,
            text="Manage inventory, billing, analytics and reporting — all in one place.",
            font=ctk.CTkFont(size=15),
            text_color="#374151"  # Gray-700
        ).pack(pady=(0, 25))

        # ---------- Animated Welcome Text ----------
        self.welcome_texts = itertools.cycle([
            "Built for small businesses, wholesalers, and retailers.",
            "Secure and efficient product tracking.",
            "Generate professional GST invoices in one click.",
            "Understand performance through visual analytics."
        ])
        self.animated_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=13, slant="italic"),
            text_color="#6B7280"  # Gray-600
        )
        self.animated_label.pack()
        self.animate_text()

        # ---------- Feature Panel Container ----------
        self.card_frame = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=16)
        self.card_frame.pack(padx=40, pady=30, fill="both", expand=True)

        # ---------- Individual Feature Panels ----------
        self.create_feature_panel(
            "📦 Product Management",
            "Add, update, search, and delete inventory items.",
            color="#DBEAFE"  # Light blue
        )
        self.create_feature_panel(
            "🧾 Billing System",
            "Create PDF invoices with tax and discount calculations.",
            color="#FEF3C7"  # Light amber
        )
        self.create_feature_panel(
            "📊 Data Analytics",
            "Track sales, trends, and generate visual reports.",
            color="#DCFCE7"  # Light green
        )
        self.create_feature_panel(
            "📋 Summary Reports",
            "Export data to Excel for audits and reports.",
            color="#FDE2E4"  # Light red-pink
        )

        # ---------- Footer ----------
        ctk.CTkLabel(
            self,
            text="© 2025 Shop Management System | Developed by Vaibhav Gaikwad",
            font=ctk.CTkFont(size=12),
            text_color="#9CA3AF"
        ).pack(pady=(10, 12), side="bottom")

    def animate_text(self):
        next_text = next(self.welcome_texts)
        self.animated_label.configure(text=next_text)
        self.after(3500, self.animate_text)

    def create_feature_panel(self, title, description, color="#F9FAFB"):
        panel = ctk.CTkFrame(
            self.card_frame,
            corner_radius=12,
            fg_color=color,
            border_color="#E5E7EB",
            border_width=1
        )
        panel.pack(padx=20, pady=12, fill="x", expand=False)

        ctk.CTkLabel(
            panel,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#111827"  # Gray-900
        ).pack(anchor="w", padx=20, pady=(15, 4))

        ctk.CTkLabel(
            panel,
            text=description,
            font=ctk.CTkFont(size=13),
            text_color="#374151"  # Gray-700
        ).pack(anchor="w", padx=20, pady=(0, 15))
