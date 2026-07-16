# modules/sales_tab.py
import customtkinter as ctk
from tkinter import messagebox
import config

class SalesTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # In-memory database to store orders
        self.saved_orders = []
        
        self.setup_ui()

    def setup_ui(self):
        # Grid configuration: 2 equal columns (Left: Form, Right: Order List)
        self.grid_columnconfigure(0, weight=1, uniform="col")
        self.grid_columnconfigure(1, weight=1, uniform="col")
        self.grid_rowconfigure(0, weight=1)

        # --- Section 1: Create New Order Form ---
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.form_title = ctk.CTkLabel(self.form_frame, text="Create New School Order", font=("Arial", 18, "bold"))
        self.form_title.pack(pady=15)

        # School Name
        self.school_label = ctk.CTkLabel(self.form_frame, text="School Name:")
        self.school_label.pack(anchor="w", padx=20, pady=2)
        self.school_name = ctk.CTkEntry(self.form_frame, placeholder_text="e.g. Alborz School")
        self.school_name.pack(fill="x", padx=20, pady=5)

        # Select Category
        self.category_label = ctk.CTkLabel(self.form_frame, text="Category:")
        self.category_label.pack(anchor="w", padx=20, pady=2)
        
        categories = list(config.MENU_OPTIONS.keys())
        self.category_type = ctk.CTkComboBox(
            self.form_frame, 
            values=categories,
            command=self.update_food_options
        )
        self.category_type.pack(fill="x", padx=20, pady=5)
        self.category_type.set("Select Category")

        # Select Food
        self.food_label = ctk.CTkLabel(self.form_frame, text="Food / Item:")
        self.food_label.pack(anchor="w", padx=20, pady=2)
        self.food_type = ctk.CTkComboBox(self.form_frame, values=[])
        self.food_type.pack(fill="x", padx=20, pady=5)
        self.food_type.set("Select Food")

        # Quantity
        self.qty_label = ctk.CTkLabel(self.form_frame, text="Quantity (Number of Meals):")
        self.qty_label.pack(anchor="w", padx=20, pady=2)
        self.quantity = ctk.CTkEntry(self.form_frame, placeholder_text="e.g. 50")
        self.quantity.pack(fill="x", padx=20, pady=5)

        # Unit Price
        self.price_label = ctk.CTkLabel(self.form_frame, text="Price per Meal (IRR):")
        self.price_label.pack(anchor="w", padx=20, pady=2)
        self.price_per_unit = ctk.CTkEntry(self.form_frame, placeholder_text="e.g. 150000")
        self.price_per_unit.pack(fill="x", padx=20, pady=5)

        # Delivery Date
        self.date_label = ctk.CTkLabel(self.form_frame, text="Delivery Date:")
        self.date_label.pack(anchor="w", padx=20, pady=2)
        self.order_date = ctk.CTkEntry(self.form_frame, placeholder_text="YYYY/MM/DD")
        self.order_date.pack(fill="x", padx=20, pady=5)

        # Submit Button
        self.submit_btn = ctk.CTkButton(self.form_frame, text="Save Order", fg_color="green", hover_color="darkgreen", command=self.save_order)
        self.submit_btn.pack(fill="x", padx=20, pady=20)


        # --- Section 2: Saved Orders List ---
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.list_title = ctk.CTkLabel(self.list_frame, text="Saved Orders History", font=("Arial", 18, "bold"))
        self.list_title.pack(pady=15)

        # Scrollable container for displaying orders
        self.scrollable_list = ctk.CTkScrollableFrame(self.list_frame, width=380, height=450)
        self.scrollable_list.pack(padx=10, pady=10, fill="both", expand=True)

    def update_food_options(self, selected_category):
        """Updates the food dropdown list when the category changes"""
        foods = config.MENU_OPTIONS.get(selected_category, [])
        self.food_type.configure(values=foods)
        
        if foods:
            self.food_type.set(foods[0])
        else:
            self.food_type.set("No items")

    def save_order(self):
        school = self.school_name.get().strip()
        category = self.category_type.get()
        food = self.food_type.get()
        qty = self.quantity.get().strip()
        price = self.price_per_unit.get().strip()
        date = self.order_date.get().strip()

        # Validation
        if not school or category == "Select Category" or food in ["Select Food", "No items"] or not qty or not price or not date:
            messagebox.showerror("Error", "Please fill in all fields correctly.")
            return

        # Calculate total price for display convenience
        try:
            total_price = int(qty) * float(price)
        except ValueError:
            messagebox.showerror("Error", "Quantity and Price must be numeric values.")
            return

        # Save order info
        order_data = {
            "school": school,
            "category": category,
            "food": food,
            "quantity": qty,
            "price": price,
            "total": f"{total_price:,.0f}",
            "date": date
        }
        self.saved_orders.append(order_data)

        # Reset form fields
        self.school_name.delete(0, 'end')
        self.category_type.set("Select Category")
        self.food_type.configure(values=[])
        self.food_type.set("Select Food")
        self.quantity.delete(0, 'end')
        self.price_per_unit.delete(0, 'end')
        self.order_date.delete(0, 'end')

        # Refresh the history list
        self.update_orders_list()
        messagebox.showinfo("Success", "Order saved successfully.")

    def update_orders_list(self):
        # Clear existing widgets
        for widget in self.scrollable_list.winfo_children():
            widget.destroy()

        # Render each order (newest on top)
        for order in reversed(self.saved_orders):
            item_frame = ctk.CTkFrame(self.scrollable_list, fg_color="#2b2b2b", corner_radius=8)
            item_frame.pack(fill="x", padx=5, pady=5)

            info_text = (
                f"School: {order['school']}\n"
                f"Item: {order['food']} ({order['category']}) x{order['quantity']}\n"
                f"Total Price: {order['total']} IRR | Date: {order['date']}"
            )
            
            info_label = ctk.CTkLabel(item_frame, text=info_text, justify="left", anchor="w")
            info_label.pack(side="left", padx=10, pady=10)
