import customtkinter as ctk
from tkinter import simpledialog, messagebox
from modules.school_dashboard import SchoolDashboard

class SalesTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # دیتابیس فرضی برای ذخیره مدارس و اطلاعات آن‌ها
        self.schools_data = {
            "Alborz School": {"expenses": [], "returns": [], "sales": []},
            "Sadaf School": {"expenses": [], "returns": [], "sales": []}
        }
        
        # نگهدارنده فریم فعلی برای سوئیچ کردن بین صفحات
        self.current_view = None
        self.show_schools_grid()

    def clear_view(self):
        """حذف فریم فعلی برای بارگذاری صفحه جدید"""
        if self.current_view:
            self.current_view.destroy()

        for widget in self.winfo_children():
            widget.destroy()

    def show_schools_grid(self):
        """نمایش صفحه اول: مربع‌های مدارس"""
        self.clear_view()
        
        # فریم اصلی اسکرول‌باور برای کارت‌ها
        self.current_view = ctk.CTkScrollableFrame(self)
        self.current_view.pack(fill="both", expand=True, padx=10, pady=10)
        
        # تنظیم ستون‌های گرید (مثلاً ۴ ستون)
        for i in range(4):
            self.current_view.grid_columnconfigure(i, weight=1, minsize=150)

        row, col = 0, 0

        # ساخت کارت برای هر مدرسه
        for school_name in self.schools_data.keys():
            card = ctk.CTkButton(
                self.current_view, 
                text=school_name, 
                font=("Arial", 14, "bold"),
                fg_color="#3a3a3a",
                hover_color="#4a4a4a",
                height=120,
                corner_radius=10,
                command=lambda name=school_name: self.open_school_dashboard(name)
            )
            card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            col += 1
            if col > 3:
                col = 0
                row += 1

        # دکمه مثبت (+) برای اضافه کردن مدرسه جدید
        add_card = ctk.CTkButton(
            self.current_view, 
            text="+", 
            font=("Arial", 30, "bold"),
            fg_color="#2b2b2b",
            hover_color="#3a3a3a",
            border_width=2,
            border_color="#555555",
            height=120,
            corner_radius=10,
            command=self.add_new_school
        )
        add_card.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

    
    def add_new_school(self):
        """باز کردن یک دیالوگ برای گرفتن نام مدرسه جدید"""
        school_name = simpledialog.askstring("New School", "Enter school name:")
        if school_name:
            school_name = school_name.strip()
            if school_name in self.schools_data:
                messagebox.showerror("Error", "This school already exists.")
            elif school_name:
                self.schools_data[school_name] = {"expenses": [], "returns": [], "sales": []}
                self.show_schools_grid()
    

    def open_school_dashboard(self, school_name):
        """باز کردن داشبورد اختصاصی مدرسه انتخاب شده"""
        self.clear_view()
        self.current_view = SchoolDashboard(self, school_name, self.schools_data[school_name], self.show_schools_grid)
        self.current_view.pack(fill="both", expand=True)
