# modules/expenses_tab.py
import customtkinter as ctk
import config

class ExpensesTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()

    def setup_ui(self):
        title_label = ctk.CTkLabel(self, text="Expense Invoice Management", font=config.FONT_TITLE)
        title_label.pack(pady=10)

        # 1. Fixed Expenses
        self.create_expense_row("1. Fixed Expenses", config.FIXED_EXPENSES, "+ Add Fixed Expense")
        # 2. Materials
        self.create_expense_row("2. Raw Materials & Support", config.MATERIAL_EXPENSES, "+ Add Support Expense")
        # 3. Buffet
        self.create_expense_row("3. School Buffet Expenses", config.BUFFET_EXPENSES, "+ Add Buffet Expense")

    def create_expense_row(self, label_text, combo_values, btn_text):
        frame = ctk.CTkFrame(self)
        frame.pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(frame, text=label_text, font=config.FONT_LABEL).pack(side="right", padx=10, pady=10)
        
        combo = ctk.CTkComboBox(frame, values=combo_values)
        combo.pack(side="right", padx=10, pady=10)

        amount = ctk.CTkEntry(frame, placeholder_text="Amount (IRR)")
        amount.pack(side="right", padx=10, pady=10)

        btn = ctk.CTkButton(frame, text=btn_text)
        btn.pack(side="left", padx=10, pady=10)
