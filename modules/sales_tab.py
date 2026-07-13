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

        self.school_name = ctk.CTkEntry(form_frame, placeholder_text="School Name")
        self.school_name.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.order_date = ctk.CTkEntry(form_frame, placeholder_text="Delivery Date (YYYY/MM/DD)")
        self.order_date.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # تمام غذاها را از دسته‌بندی‌های مختلف استخراج کرده و به یک لیست ساده تبدیل می‌کند
        all_foods = [food for category in config.MENU_OPTIONS.values() for food in category]

        self.food_type = ctk.CTkComboBox(form_frame, values=all_foods)
        self.food_type.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.quantity = ctk.CTkEntry(form_frame, placeholder_text="Number of Meals")
        self.quantity.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        self.price_per_unit = ctk.CTkEntry(form_frame, placeholder_text="Price per Meal (IRR)")
        self.price_per_unit.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        btn_submit = ctk.CTkButton(form_frame, text="Save Order", fg_color="green", hover_color="darkgreen")
        btn_submit.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        form_frame.grid_columnconfigure((0, 1, 2), weight=1)

        table_frame = ctk.CTkScrollableFrame(self, label_text="Today's Orders")
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        sample_txt = ctk.CTkLabel(
            table_frame,
            text="Alborz School - Tomorrow - 50 Grilled Chicken Meals\nFarzanegan School - Tomorrow - 120 Kebab with Rice Meals",
            font=config.FONT_TEXT
        )
        sample_txt.pack(pady=20)
