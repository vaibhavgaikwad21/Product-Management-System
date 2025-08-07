import customtkinter as ctk
from login_page import LoginPage
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
        self.title("Shop Product Management System")
        self.geometry("1000x600")

        self.login_page = LoginPage(self, self.on_login_success)
        self.login_page.pack(fill="both", expand=True)

    def on_login_success(self):
        self.login_page.destroy()

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True)

        self.tabs.add("Home")
        self.tabs.add("Products")
        self.tabs.add("Billing")
        self.tabs.add("Summary")
        self.tabs.add("Charts")

        HomeTab(self.tabs.tab("Home")).pack(fill="both", expand=True)
        ProductTab(self.tabs.tab("Products")).pack(fill="both", expand=True)
        BillingPage(self.tabs.tab("Billing")).pack(fill="both", expand=True)
        SummaryPage(self.tabs.tab("Summary")).pack(fill="both", expand=True)
        ChartsPage(self.tabs.tab("Charts")).pack(fill="both", expand=True)


if __name__ == "__main__":
    app = ShopApp()
    app.mainloop()
