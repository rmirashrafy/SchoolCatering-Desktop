
import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox

class SchoolExpensesView(ctk.CTkFrame):
    def __init__(self, master, school_name, expenses_list, back_to_dashboard_callback):
        super().__init__(master, fg_color="transparent")
        self.school_name = school_name
        self.expenses_list = expenses_list  # متصل به لیست مرجع هزینه‌های مدرسه
        self.back_callback = back_to_dashboard_callback

        self.upload_dir = "saved_receipt_images"
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

        self.selected_image_path = None
        self.setup_ui()

    def setup_ui(self):
        # ---- ۱. هدر بالای صفحه (دکمه بک و عنوان) ----
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=10)

        back_btn = ctk.CTkButton(header_frame, text="← Back to Dashboard", width=140, command=self.back_callback)
        back_btn.pack(side="left")

        title = ctk.CTkLabel(header_frame, text=f"Expenses / Receipts - {self.school_name}", font=("Arial", 16, "bold"))
        title.pack(side="right", padx=10)

        # ---- ۲. بدنه اصلی (گرید دو ستونه) ----
        body_frame = ctk.CTkFrame(self, fg_color="transparent")
        body_frame.pack(fill="both", expand=True, padx=10, pady=5)

        body_frame.grid_columnconfigure(0, weight=1, uniform="col")
        body_frame.grid_columnconfigure(1, weight=1, uniform="col")
        body_frame.grid_rowconfigure(0, weight=1)

        # --- بخش اول: فرم ثبت هزینه جدید ---
        self.form_frame = ctk.CTkFrame(body_frame)
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.form_title = ctk.CTkLabel(self.form_frame, text="Create New Receipt", font=("Arial", 18, "bold"))
        self.form_title.pack(pady=15)

        # انتخاب نوع هزینه
        self.type_label = ctk.CTkLabel(self.form_frame, text="Receipt Type:")
        self.type_label.pack(anchor="w", padx=20, pady=2)
        
        # دسته‌بندی هزینه‌های اختصاصی مدرسه
        expense_options = ["Water", "Electricity", "Gas", "Rent", "Worker Salary", "Maintenance", "Supplies", "Other"]
        self.type_select = ctk.CTkOptionMenu(self.form_frame, values=expense_options, command=self.toggle_worker_field)
        self.type_select.pack(fill="x", padx=20, pady=5)

        # فیلد نام کارمند (مخفی به صورت پیش‌فرض)
        self.worker_label = ctk.CTkLabel(self.form_frame, text="Worker Name:")
        self.worker_entry = ctk.CTkEntry(self.form_frame, placeholder_text="e.g. John Doe")

        # فیلد مبلغ
        self.amount_label = ctk.CTkLabel(self.form_frame, text="Amount:")
        self.amount_label.pack(anchor="w", padx=20, pady=2)
        self.amount_entry = ctk.CTkEntry(self.form_frame, placeholder_text="e.g. 500000")
        self.amount_entry.pack(fill="x", padx=20, pady=5)

        # فیلد تاریخ
        self.date_label = ctk.CTkLabel(self.form_frame, text="Date:")
        self.date_label.pack(anchor="w", padx=20, pady=2)
        self.date_entry = ctk.CTkEntry(self.form_frame, placeholder_text="YYYY/MM/DD")
        self.date_entry.pack(fill="x", padx=20, pady=5)

        # آپلود تصویر رسید
        self.image_label = ctk.CTkLabel(self.form_frame, text="Receipt Image:")
        self.image_label.pack(anchor="w", padx=20, pady=2)
        
        self.upload_btn = ctk.CTkButton(self.form_frame, text="Choose & Upload Receipt Image", command=self.upload_image)
        self.upload_btn.pack(fill="x", padx=20, pady=5)
        
        self.file_path_label = ctk.CTkLabel(self.form_frame, text="No image selected", text_color="gray", font=("Arial", 10))
        self.file_path_label.pack(anchor="w", padx=20, pady=2)

        # دکمه ثبت
        self.submit_btn = ctk.CTkButton(self.form_frame, text="Save Receipt", fg_color="#c0392b", hover_color="#e74c3c", command=self.save_receipt)
        self.submit_btn.pack(fill="x", padx=20, pady=25)

        # --- بخش دوم: لیست تاریخچه هزینه‌های ثبت شده ---
        self.list_frame = ctk.CTkFrame(body_frame)
        self.list_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.list_title = ctk.CTkLabel(self.list_frame, text="Saved Receipts History", font=("Arial", 18, "bold"))
        self.list_title.pack(pady=15)

        self.scrollable_list = ctk.CTkScrollableFrame(self.list_frame, width=380, height=450)
        self.scrollable_list.pack(padx=10, pady=10, fill="both", expand=True)

        self.update_receipts_list()

    def toggle_worker_field(self, choice):
        """نمایش یا مخفی کردن فیلد نام کارمند"""
        if choice == "Worker Salary":
            self.worker_label.pack(anchor="w", padx=20, pady=2)
            self.worker_entry.pack(fill="x", padx=20, pady=5)
            
            # چیدمان مجدد المان‌ها برای حفظ ترتیب عمودی
            self.amount_label.pack_forget()
            self.amount_entry.pack_forget()
            self.date_label.pack_forget()
            self.date_entry.pack_forget()
            self.image_label.pack_forget()
            self.upload_btn.pack_forget()
            self.file_path_label.pack_forget()
            self.submit_btn.pack_forget()

            self.amount_label.pack(anchor="w", padx=20, pady=2)
            self.amount_entry.pack(fill="x", padx=20, pady=5)
            self.date_label.pack(anchor="w", padx=20, pady=2)
            self.date_entry.pack(fill="x", padx=20, pady=5)
            self.image_label.pack(anchor="w", padx=20, pady=2)
            self.upload_btn.pack(fill="x", padx=20, pady=5)
            self.file_path_label.pack(anchor="w", padx=20, pady=2)
            self.submit_btn.pack(fill="x", padx=20, pady=25)
        else:
            self.worker_label.pack_forget()
            self.worker_entry.pack_forget()

    def upload_image(self):
        file_types = [('Image Files', '*.png *.jpg *.jpeg *.bmp')]
        file_path = filedialog.askopenfilename(title="Select Receipt Image", filetypes=file_types)
        
        if file_path:
            self.selected_image_path = file_path
            filename = os.path.basename(file_path)
            self.file_path_label.configure(text=f"Selected: {filename}", text_color="white")

    def save_receipt(self):
        receipt_type = self.type_select.get()
        amount = self.amount_entry.get().strip()
        date = self.date_entry.get().strip()
        worker_name = self.worker_entry.get().strip() if receipt_type == "Worker Salary" else None

        if not amount or not date:
            messagebox.showerror("Error", "Please fill in all required fields.")
            return
        
        if receipt_type == "Worker Salary" and not worker_name:
            messagebox.showerror("Error", "Please enter the worker's name.")
            return

        saved_img_name = "No Image"
        if self.selected_image_path:
            extension = os.path.splitext(self.selected_image_path)[1]
            safe_date = date.replace("/", "-")
            saved_img_name = f"{self.school_name}_{receipt_type}_{safe_date}{extension}"
            destination = os.path.join(self.upload_dir, saved_img_name)
            try:
                shutil.copy(self.selected_image_path, destination)
            except Exception as e:
                messagebox.showerror("Image Save Error", str(e))
                return

        receipt_data = {
            "type": receipt_type,
            "worker_name": worker_name,
            "amount": amount,
            "date": date,
            "image": saved_img_name
        }
        self.expenses_list.append(receipt_data)

        # ریست کردن فرم
        self.amount_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.worker_entry.delete(0, 'end')
        self.file_path_label.configure(text="No image selected", text_color="gray")
        self.selected_image_path = None
        
        self.type_select.set("Water")
        self.toggle_worker_field("Water")

        self.update_receipts_list()
        messagebox.showinfo("Success", "Expense receipt saved successfully.")

    def update_receipts_list(self):
        for widget in self.scrollable_list.winfo_children():
            widget.destroy()

        for receipt in reversed(self.expenses_list):
            item_frame = ctk.CTkFrame(self.scrollable_list, fg_color="#2b2b2b", corner_radius=8)
            item_frame.pack(fill="x", padx=5, pady=5)

            if receipt['type'] == "Worker Salary":
                info_text = f"Type: {receipt['type']} (Worker: {receipt['worker_name']})\nAmount: {receipt['amount']} | Date: {receipt['date']}\nImage: {receipt['image']}"
            else:
                info_text = f"Type: {receipt['type']}\nAmount: {receipt['amount']} | Date: {receipt['date']}\nImage: {receipt['image']}"
                
            info_label = ctk.CTkLabel(item_frame, text=info_text, justify="left", anchor="w")
            info_label.pack(side="left", padx=10, pady=10)
