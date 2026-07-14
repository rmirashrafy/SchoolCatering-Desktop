# main.py
import customtkinter as ctk
import config
from modules.sales_tab import SalesTab
from modules.expenses_tab import ExpensesTab

class CateringApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("School Catering Accounting System")
        self.geometry("900x650")

        # Main tab view
        self.tab_view = ctk.CTkTabview(self, width=860, height=600)
        self.tab_view.pack(padx=20, pady=20, fill="both", expand=True)

        # Add tabs
        tab1_container = self.tab_view.add("Sales & Schools")
        tab2_container = self.tab_view.add("Expense Invoices")

        # Load modular frames into tabs
        self.sales_tab = SalesTab(tab1_container)
        self.sales_tab.pack(fill="both", expand=True)

        self.expenses_tab = ExpensesTab(tab2_container)
        self.expenses_tab.pack(fill="both", expand=True)

if __name__ == "__main__":
    config.init_theme()
    app = CateringApp()
    app.mainloop()
