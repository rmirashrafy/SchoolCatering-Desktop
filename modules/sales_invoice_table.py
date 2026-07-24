import customtkinter as ctk
from tkinter import messagebox
import config
import os

class SalesInvoiceTable(ctk.CTkFrame):
    def __init__(self, master, school_name, items_list, back_to_dashboard_callback, invoice_type="Sales"):
        super().__init__(master, fg_color="transparent")
        self.school_name = school_name
        self.sales_list = items_list  # لیست مرجع داده‌ها (فروش یا برگشتی)
        self.back_callback = back_to_dashboard_callback
        self.invoice_type = invoice_type  # نوع فاکتور: "Sales" یا "Returns"
        
        self.edit_mode = False
        self.checkbox_vars = {}
        self.qty_entries = {} 

        self.setup_ui()

    def setup_ui(self):
        # ---- هدر فاکتور ----
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=10)

        back_btn = ctk.CTkButton(header_frame, text="← Back to Dashboard", width=140, command=self.back_callback)
        back_btn.pack(side="left")

        # عنوان تغییرپذیر بر اساس نوع فاکتور
        title_text = f"{self.invoice_type} Invoice - {self.school_name}"
        title = ctk.CTkLabel(header_frame, text=title_text, font=("Arial", 16, "bold"))
        title.pack(side="right", padx=10)

        # دکمه ویرایش ساختاری
        self.edit_btn = ctk.CTkButton(header_frame, text="Edit", width=80, fg_color="#2980b9", hover_color="#3498db", command=self.toggle_edit_mode)
        self.edit_btn.pack(side="right", padx=10)

        # ---- فرم افزودن ردیف به فاکتور ----
        self.form_frame = ctk.CTkFrame(self)

        categories = list(config.MENU_OPTIONS.keys())
        self.category_combo = ctk.CTkComboBox(self.form_frame, values=categories, command=self.update_food_options, width=130)
        self.category_combo.pack(side="left", padx=5, pady=10)
        self.category_combo.set("Select Category")

        self.food_combo = ctk.CTkComboBox(self.form_frame, values=[], width=130)
        self.food_combo.pack(side="left", padx=5, pady=10)
        self.food_combo.set("Select Food")

        self.qty_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Qty", width=60)
        self.qty_entry.pack(side="left", padx=5, pady=10)

        self.price_entry = ctk.CTkEntry(self.form_frame, placeholder_text="Price", width=100)
        self.price_entry.pack(side="left", padx=5, pady=10)

        self.add_btn = ctk.CTkButton(self.form_frame, text="Add Item", width=80, fg_color="green", hover_color="darkgreen", command=self.add_item)
        self.add_btn.pack(side="left", padx=5, pady=10)

        self.delete_btn = ctk.CTkButton(self.form_frame, text="Delete Selected", width=110, fg_color="#c0392b", hover_color="#e74c3c", command=self.delete_selected_items)
        self.delete_btn.pack(side="left", padx=5, pady=10)

        # ---- جدول فاکتور ----
        self.table_frame = ctk.CTkScrollableFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # ---- بخش پایین صفحه ----
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=10, pady=10)

        self.save_print_btn = ctk.CTkButton(
            self.footer_frame, 
            text=f"Save & Print {self.invoice_type} Invoice (PDF)", 
            font=("Arial", 14, "bold"),
            fg_color="#16a085" if self.invoice_type == "Sales" else "#d35400", 
            hover_color="#1abc9c" if self.invoice_type == "Sales" else "#e67e22", 
            height=40,
            command=self.save_all_and_print
        )
        self.save_print_btn.pack(fill="x", padx=20)

        self.render_table()

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            self.edit_btn.configure(text="Done", fg_color="#27ae60", hover_color="#2ecc71")
            self.table_frame.pack_forget()
            self.footer_frame.pack_forget()
            self.form_frame.pack(fill="x", padx=10, pady=5)
            self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)
            self.footer_frame.pack(fill="x", padx=10, pady=10)
        else:
            self.edit_btn.configure(text="Edit", fg_color="#2980b9", hover_color="#3498db")
            self.form_frame.pack_forget()
        
        self.render_table()

    def update_food_options(self, selected_category):
        foods = config.MENU_OPTIONS.get(selected_category, [])
        self.food_combo.configure(values=foods)
        if foods:
            self.food_combo.set(foods[0])
        else:
            self.food_combo.set("No items")

    def render_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        self.checkbox_vars.clear()
        self.qty_entries.clear()

        headers = ["Category", "Food Item", "Quantity (Editable)", "Unit Price", "Total Price"]
        start_col = 0
        
        if self.edit_mode:
            headers.insert(0, "Select")
            start_col = 1

        for col_idx, header_text in enumerate(headers):
            self.table_frame.grid_columnconfigure(col_idx, weight=1, uniform="table_col")
            lbl = ctk.CTkLabel(self.table_frame, text=header_text, font=("Arial", 12, "bold"), fg_color="#1f1f1f", height=30)
            lbl.grid(row=0, column=col_idx, sticky="nsew", padx=1, pady=1)

        for row_idx, item in enumerate(self.sales_list, start=1):
            if self.edit_mode:
                var = ctk.BooleanVar()
                self.checkbox_vars[row_idx - 1] = var
                chk = ctk.CTkCheckBox(self.table_frame, text="", variable=var, width=20)
                chk.grid(row=row_idx, column=0, pady=2)

            ctk.CTkLabel(self.table_frame, text=item.get("category", "-"), anchor="w", padx=5).grid(row=row_idx, column=start_col, sticky="nsew", pady=2)
            ctk.CTkLabel(self.table_frame, text=item["food"], anchor="w", padx=5).grid(row=row_idx, column=start_col+1, sticky="nsew", pady=2)
            
            qty_ent = ctk.CTkEntry(self.table_frame, width=70, justify="center")
            qty_ent.insert(0, str(item["qty"]))
            qty_ent.grid(row=row_idx, column=start_col+2, pady=2)
            self.qty_entries[row_idx - 1] = qty_ent

            ctk.CTkLabel(self.table_frame, text=f"{float(item['price']):,.3f}").grid(row=row_idx, column=start_col+3, sticky="nsew", pady=2)
            ctk.CTkLabel(self.table_frame, text=f"{item['total']:,.3f}").grid(row=row_idx, column=start_col+4, sticky="nsew", pady=2)

    def save_all_and_print(self):
        if not self.sales_list:
            messagebox.showwarning("Empty Invoice", "There are no items in the invoice to save or print.")
            return

        for idx, qty_widget in self.qty_entries.items():
            qty_str = qty_widget.get().strip()
            try:
                new_qty = int(qty_str)
                if new_qty <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", f"Invalid quantity in row {idx+1}. Must be a positive integer.")
                return
            
            item = self.sales_list[idx]
            item["qty"] = new_qty
            item["total"] = new_qty * float(item["price"])

        self.render_table()

        try:
            from weasyprint import HTML
            
            grand_total = sum(item["total"] for item in self.sales_list)
            
            html_rows = ""
            for idx, item in enumerate(self.sales_list, start=1):
                html_rows += f"""
                <tr>
                    <td>{idx}</td>
                    <td>{item.get('category', '-')}</td>
                    <td>{item['food']}</td>
                    <td>{item['qty']}</td>
                    <td>{float(item['price']):,.0f} IRR</td>
                    <td>{item['total']:,.0f} IRR</td>
                </tr>
                """

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    @page {{ size: A4; margin: 20mm 15mm; background-color: #ffffff; }}
                    body {{ font-family: 'Arial', sans-serif; color: #333333; direction: ltr; }}
                    .header {{ border-bottom: 2px solid #2c3e50; padding-bottom: 10px; margin-bottom: 30px; }}
                    .title {{ font-size: 24pt; font-weight: bold; color: #2c3e50; margin: 0; }}
                    .meta-info {{ margin-top: 10px; font-size: 11pt; color: #7f8c8d; }}
                    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                    th {{ background-color: #2c3e50; color: #ffffff; font-weight: bold; padding: 10px; font-size: 11pt; text-align: left; }}
                    td {{ padding: 10px; border-bottom: 1px solid #bdc3c7; font-size: 11pt; }}
                    .total-row {{ font-weight: bold; background-color: #ecf0f1; }}
                    .footer {{ margin-top: 50px; text-align: center; font-size: 10pt; color: #95a5a6; border-top: 1px solid #bdc3c7; padding-top: 10px; }}
                </style>
            </head>
            <body>
                <div class="header">
                    <div class="title">{self.invoice_type.upper()} INVOICE</div>
                    <div class="meta-info">
                        <strong>School Name:</strong> {self.school_name}<br>
                        <strong>Status:</strong> Final & Saved
                    </div>
                </div>

                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Category</th>
                            <th>Food Item</th>
                            <th>Quantity</th>
                            <th>Unit Price</th>
                            <th>Total Price</th>
                        </tr>
                    </thead>
                    <tbody>
                        {html_rows}
                        <tr class="total-row">
                            <td colspan="5" style="text-align: right;">GRAND TOTAL :</td>
                            <td>{grand_total:,.0f} IRR</td>
                        </tr>
                    </tbody>
                </table>

                <div class="footer">
                    Generated Automatically by School Management System
                </div>
            </body>
            </html>
            """
            
            # نام فایل خروجی PDF بر اساس فروش یا برگشتی بودن
            pdf_filename = f"{self.invoice_type}_Invoice_{self.school_name.replace(' ', '_')}.pdf"
            HTML(string=html_content).write_pdf(pdf_filename)
            
            messagebox.showinfo("Success", f"All changes saved successfully!\nInvoice printed to: {os.path.abspath(pdf_filename)}")
            
        except ImportError:
            messagebox.showinfo("Saved", "All quantities updated and saved successfully in memory!\n(Note: Install 'weasyprint' to enable PDF printing feature.)")
        except Exception as e:
            messagebox.showerror("Error", f"Saved successfully, but failed to print PDF: {str(e)}")

    def add_item(self):
        category = self.category_combo.get()
        food = self.food_combo.get()
        qty = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()

        if category == "Select Category" or food in ["Select Food", "No items"] or not qty or not price:
            messagebox.showerror("Error", "Please fill all fields correctly.")
            return

        try:
            total_price = int(qty) * float(price)
        except ValueError:
            messagebox.showerror("Error", "Quantity and Price must be numbers.")
            return

        self.sales_list.append({
            "category": category,
            "food": food,
            "qty": int(qty),
            "price": price,
            "total": total_price
        })

        self.qty_entry.delete(0, 'end')
        self.price_entry.delete(0, 'end')
        self.render_table()

    def delete_selected_items(self):
        indices_to_delete = [idx for idx, var in self.checkbox_vars.items() if var.get()]
        
        if not indices_to_delete:
            messagebox.showwarning("Selection", "No items selected for deletion.")
            return

        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {len(indices_to_delete)} selected item(s)?"):
            for idx in sorted(indices_to_delete, reverse=True):
                self.sales_list.pop(idx)
            self.render_table()
