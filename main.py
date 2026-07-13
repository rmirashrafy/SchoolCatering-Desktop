
import customtkinter as ctk

# Initial theme and appearance settings
ctk.set_appearance_mode("System")  # Match system theme (Dark/Light)
ctk.set_default_color_theme("blue")  # Blue color theme


class CateringApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("School Catering Accounting System")
        self.geometry("900x650")

        # Main tab view
        self.tab_view = ctk.CTkTabview(self, width=860, height=600)
        self.tab_view.pack(padx=20, pady=20, fill="both", expand=True)

        # Tabs
        self.tab1 = self.tab_view.add("Sales & Schools")
        self.tab2 = self.tab_view.add("Expense Invoices")

        # Initialize tabs
        self.setup_tab1()
        self.setup_tab2()

    def setup_tab1(self):
        """Sales and school information"""

        title_label = ctk.CTkLabel(
            self.tab1,
            text="School Orders & Sales Registration",
            font=("Tahoma", 18, "bold")
        )
        title_label.pack(pady=10)

        form_frame = ctk.CTkFrame(self.tab1)
        form_frame.pack(padx=20, pady=10, fill="x")

        self.school_name = ctk.CTkEntry(
            form_frame,
            placeholder_text="School Name"
        )
        self.school_name.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.order_date = ctk.CTkEntry(
            form_frame,
            placeholder_text="Delivery Date (YYYY/MM/DD)"
        )
        self.order_date.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.food_type = ctk.CTkComboBox(
            form_frame,
            values=[
                "Kebab with Rice",
                "Grilled Chicken",
                "Ghormeh Sabzi",
                "Gheymeh"
            ]
        )
        self.food_type.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.quantity = ctk.CTkEntry(
            form_frame,
            placeholder_text="Number of Meals"
        )
        self.quantity.grid(row=1, column=2, padx=10, pady=10, sticky="ew")

        self.price_per_unit = ctk.CTkEntry(
            form_frame,
            placeholder_text="Price per Meal (IRR)"
        )
        self.price_per_unit.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        btn_submit = ctk.CTkButton(
            form_frame,
            text="Save Order",
            fg_color="green",
            hover_color="darkgreen"
        )
        btn_submit.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        form_frame.grid_columnconfigure((0, 1, 2), weight=1)

        table_frame = ctk.CTkScrollableFrame(
            self.tab1,
            label_text="Today's Orders"
        )
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        sample_txt = ctk.CTkLabel(
            table_frame,
            text=(
                "Alborz School - Tomorrow - 50 Grilled Chicken Meals\n"
                "Farzanegan School - Tomorrow - 120 Kebab with Rice Meals"
            ),
            font=("Tahoma", 12)
        )
        sample_txt.pack(pady=20)

    def setup_tab2(self):
        """Expense invoices"""

        title_label = ctk.CTkLabel(
            self.tab2,
            text="Expense Invoice Management",
            font=("Tahoma", 18, "bold")
        )
        title_label.pack(pady=10)

        # Fixed Expenses
        frame_fixed = ctk.CTkFrame(self.tab2)
        frame_fixed.pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(
            frame_fixed,
            text="1. Fixed Expenses",
            font=("Tahoma", 12, "bold")
        ).pack(side="right", padx=10, pady=10)

        fixed_type = ctk.CTkComboBox(
            frame_fixed,
            values=[
                "Rent",
                "Water",
                "Electricity",
                "Gas",
                "Employee Salary"
            ]
        )
        fixed_type.pack(side="right", padx=10, pady=10)

        fixed_amount = ctk.CTkEntry(
            frame_fixed,
            placeholder_text="Amount (IRR)"
        )
        fixed_amount.pack(side="right", padx=10, pady=10)

        btn_fixed = ctk.CTkButton(
            frame_fixed,
            text="+ Add Fixed Expense"
        )
        btn_fixed.pack(side="left", padx=10, pady=10)

        # Materials & Support
        frame_material = ctk.CTkFrame(self.tab2)
        frame_material.pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(
            frame_material,
            text="2. Raw Materials & Support",
            font=("Tahoma", 12, "bold")
        ).pack(side="right", padx=10, pady=10)

        material_type = ctk.CTkComboBox(
            frame_material,
            values=[
                "Raw Materials",
                "Maintenance",
                "Transportation",
                "Fuel",
                "Kitchen Supplies"
            ]
        )
        material_type.pack(side="right", padx=10, pady=10)

        material_amount = ctk.CTkEntry(
            frame_material,
            placeholder_text="Amount (IRR)"
        )
        material_amount.pack(side="right", padx=10, pady=10)

        btn_material = ctk.CTkButton(
            frame_material,
            text="+ Add Support Expense"
        )
        btn_material.pack(side="left", padx=10, pady=10)

        # School Buffet Expenses
        frame_buffet = ctk.CTkFrame(self.tab2)
        frame_buffet.pack(padx=20, pady=5, fill="x")

        ctk.CTkLabel(
            frame_buffet,
            text="3. School Buffet Expenses",
            font=("Tahoma", 12, "bold")
        ).pack(side="right", padx=10, pady=10)

        buffet_type = ctk.CTkComboBox(
            frame_buffet,
            values=[
                "Buffet Rent",
                "Buffet Staff Salary"
            ]
        )
        buffet_type.pack(side="right", padx=10, pady=10)

        buffet_amount = ctk.CTkEntry(
            frame_buffet,
            placeholder_text="Amount (IRR)"
        )
        buffet_amount.pack(side="right", padx=10, pady=10)

        btn_buffet = ctk.CTkButton(
            frame_buffet,
            text="+ Add Buffet Expense"
        )
        btn_buffet.pack(side="left", padx=10, pady=10)


if __name__ == "__main__":
    app = CateringApp()
    app.mainloop()
