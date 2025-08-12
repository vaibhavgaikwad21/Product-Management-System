import customtkinter as ctk
from home_page import HomeTab
from product_page import ProductTab
from billing_page import BillingPage
from summary_page import SummaryPage
from charts_page import ChartsPage

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class ShopApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Prodexa Inventory Management System")
        self.geometry("1200x700")
        self.configure(fg_color="#F3F4F6")

        self.pages = {}
        self.active_tab_btn = None

        # --- Navigation Bar ---
        nav_bar_container = ctk.CTkFrame(self, fg_color="transparent")
        nav_bar_container.pack(side="top", pady=10)

        nav_bar = ctk.CTkFrame(nav_bar_container, fg_color="#FFFFFF", height=60, corner_radius=12)
        nav_bar.pack(padx=40)

        self.tab_names = {
            "Home": "🏠",
            "Products": "📦",
            "Billing": "💳",
            "Summary": "📊",
            "Charts": "📈"
        }

        btn_frame = ctk.CTkFrame(nav_bar, fg_color="transparent")
        btn_frame.pack(padx=10, pady=8)

        self.tab_buttons = {}
        total_tabs = len(self.tab_names)

        for col, (name, icon) in enumerate(self.tab_names.items()):
            btn = ctk.CTkButton(
                btn_frame,
                text=f"{icon}  {name}",
                font=ctk.CTkFont(size=15, weight="bold", family="Segoe UI Emoji"),
                fg_color="transparent",
                text_color="#374151",
                hover=False,  # We'll make our own hover
                corner_radius=6,
                height=40,
                command=lambda n=name: self.show_page(n)
            )
            btn.grid(row=0, column=col, sticky="nsew", padx=6, pady=2)

            # Hover effect for inactive tabs
            btn.bind("<Enter>", lambda e, b=btn, n=name: self.hover_tab(b, n, enter=True))
            btn.bind("<Leave>", lambda e, b=btn, n=name: self.hover_tab(b, n, enter=False))

            self.tab_buttons[name] = btn

        for col in range(total_tabs):
            btn_frame.grid_columnconfigure(col, weight=1, uniform="equal")

        # --- Content Frame ---
        self.content_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=12)
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Pages
        self.pages["Home"] = HomeTab(self.content_frame, tab_view=None)
        self.pages["Products"] = ProductTab(self.content_frame)
        self.pages["Billing"] = BillingPage(self.content_frame)
        self.pages["Summary"] = SummaryPage(self.content_frame)
        self.pages["Charts"] = ChartsPage(self.content_frame)

        # Default tab
        self.show_page("Home")
        self.set_active_tab("Home")

    def show_page(self, page_name):
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()
        self.pages[page_name].pack(fill="both", expand=True)
        self.set_active_tab(page_name)

    def set_active_tab(self, name):
        # Reset previous active tab
        if self.active_tab_btn:
            prev_name = self.get_tab_name_by_button(self.active_tab_btn)
            self.active_tab_btn.configure(
                fg_color="transparent",
                text_color="#374151",
                text=f"{self.tab_names[prev_name]}  {prev_name}"
            )

        # Set new active tab
        active_btn = self.tab_buttons[name]
        active_btn.configure(
            fg_color="#2563EB",  # Blue background
            text_color="white",
            text=f"{self.tab_names[name]}  {name}"
        )
        self.active_tab_btn = active_btn

    def hover_tab(self, button, tab_name, enter):
        """ Show hover background only for inactive tabs """
        if button != self.active_tab_btn:
            if enter:
                button.configure(fg_color="#E5E7EB")  # Light grey on hover
            else:
                button.configure(fg_color="transparent")

            # Keep text intact
            button.configure(text=f"{self.tab_names[tab_name]}  {tab_name}")

    def get_tab_name_by_button(self, button):
        for name, btn in self.tab_buttons.items():
            if btn == button:
                return name
        return None


if __name__ == "__main__":
    app = ShopApp()
    app.mainloop()
