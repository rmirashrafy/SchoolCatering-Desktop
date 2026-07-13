# modules/sales_tab.py
import customtkinter as ctk
import config

class SalesTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.setup_ui()

    def setup_ui(self):
        title_label = ctk.CTkLabel(self, text="School Orders & Sales Registration", font=config.FONT_TITLE)
        title_label.pack(pady=10)

        form_frame = ctk.CTkFrame(self)
        form_frame.pack(padx=20, pady=10, fill="x")

        # ردیف 0: اطلاعات مدرسه و انتخاب دسته‌بندی/غذا
        self.school_name = ctk.CTkEntry(form_frame, placeholder_text="School Name")
        self.school_name.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # کامبوباکس اول: انتخاب دسته‌بندی
        categories = list(config.MENU_OPTIONS.keys())
        self.category_type = ctk.CTkComboBox(
            form_frame, 
            values=categories,
            command=self.update_food_options
        )
        self.category_type.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.category_type.set("Select Category")

        # کامبوباکس دوم: انتخاب غذا (ابتدا خالی است)
        self.food_type = ctk.CTkComboBox(form_frame, values=[])
        self.food_type.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.food_type.set("Select Food")

        # ردیف 1: جزئیات سفارش (تعداد، قیمت، تاریخ)
        self.quantity = ctk.CTkEntry(form_frame, placeholder_text="Number of Meals")
        self.quantity.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        self.price_per_unit = ctk.CTkEntry(form_frame, placeholder_text="Price per Meal (IRR)")
        self.price_per_unit.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.order_date = ctk.CTkEntry(form_frame, placeholder_text="Delivery Date (YYYY/MM/DD)")
        self.order_date.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # ردیف 2: دکمه ثبت سفارش
        btn_submit = ctk.CTkButton(form_frame, text="Save Order", fg_color="green", hover_color="darkgreen")
        btn_submit.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        form_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # بخش نمایش سفارش‌ها
        table_frame = ctk.CTkScrollableFrame(self, label_text="Today's Orders")
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        sample_txt = ctk.CTkLabel(
            table_frame,
            text="Alborz School - Tomorrow - 50 Grilled Chicken Meals\nFarzanegan School - Tomorrow - 120 Kebab with Rice Meals",
            font=config.FONT_TEXT
        )
        sample_txt.pack(pady=20)

    def update_food_options(self, selected_category):
        """با تغییر دسته‌بندی، لیست غذاها را به‌روز می‌کند"""
        foods = config.MENU_OPTIONS.get(selected_category, [])
        self.food_type.configure(values=foods)
        
        if foods:
            self.food_type.set(foods[0])
        else:
            self.food_type.set("No items")
