import customtkinter as ctk
from modules.sales_invoice_table import SalesInvoiceTable

class SchoolDashboard(ctk.CTkFrame):
    def __init__(self, master, school_name, school_data, back_callback):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.school_name = school_name
        self.school_data = school_data
        self.back_callback = back_callback  # بازگشت به منوی مدارس

        self.setup_ui()

    def setup_ui(self):
        # پاک کردن المان‌های قدیمی برای رندر مجدد بدون باگ
        for widget in self.winfo_children():
            widget.destroy()

        # هدر صفحه
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=10)

        back_btn = ctk.CTkButton(header_frame, text="← Back to Schools", width=100, command=self.back_callback)
        back_btn.pack(side="left")

        title = ctk.CTkLabel(header_frame, text=f"Dashboard: {self.school_name}", font=("Arial", 18, "bold"))
        title.pack(side="right", padx=10)

        # فریم گرید برای ۳ مربع منو
        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        for i in range(3):
            menu_frame.grid_columnconfigure(i, weight=1, uniform="menu_col")
        menu_frame.grid_rowconfigure(0, weight=1)

        # ۱. مربع مخارج
        btn_expenses = ctk.CTkButton(
            menu_frame, text="Expenses\n(مخارج)", font=("Arial", 16, "bold"),
            fg_color="#c0392b", hover_color="#e74c3c", command=self.open_expenses
        )
        btn_expenses.grid(row=0, column=0, padx=15, pady=20, sticky="nsew")

        # ۲. مربع برگشتی‌ها
        btn_returns = ctk.CTkButton(
            menu_frame, text="Returns\n(برگشتی‌ها)", font=("Arial", 16, "bold"),
            fg_color="#d35400", hover_color="#e67e22", command=self.open_returns
        )
        btn_returns.grid(row=0, column=1, padx=15, pady=20, sticky="nsew")

        # ۳. مربع فروش‌ها
        btn_sales = ctk.CTkButton(
            menu_frame, text="Sales / Invoice\n(فروش‌ها)", font=("Arial", 16, "bold"),
            fg_color="#27ae60", hover_color="#2ecc71", command=self.open_sales
        )
        btn_sales.grid(row=0, column=2, padx=15, pady=20, sticky="nsew")

    def open_expenses(self):
        pass

    def open_returns(self):
        pass

    def open_sales(self):
        """باز کردن جدول فاکتور فروش"""
        for widget in self.winfo_children():
            widget.destroy()
        
        # ارسال متد setup_ui به عنوان بازگشت برای حل مشکل دکمه بک فاکتور
        invoice_view = SalesInvoiceTable(
            self, 
            self.school_name, 
            self.school_data["sales"], 
            back_to_dashboard_callback=self.setup_ui
        )
        invoice_view.pack(fill="both", expand=True)
