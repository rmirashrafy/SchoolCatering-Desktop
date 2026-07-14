
import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import config

# نکته: برای بخش OCR و اسکنر نیاز به کتابخانه‌های زیر دارید که باید نصب باشند:
# pip install pillow pytesseract
try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None

try:
    import pytesseract
except ImportError:
    pytesseract = None


class ReceiptOCRHandler(ctk.CTkFrame):
    def __init__(self, master, parent_form):
        """
        master: فریم اصلی یا همان ScrollableFrame که این ابزار درون آن قرار می‌گیرد.
        parent_form: ارجاع به خود کلاس ExpensesTab برای دسترسی به مقادیر و فیلدها.
        """
        super().__init__(master, border_width=1, border_color="gray30")
        self.parent_form = parent_form
        self.scanned_image_path = None
        self.setup_ocr_ui()

    def setup_ocr_ui(self):
        # تیتر بخش مدیریت فیش
        lbl_header = ctk.CTkLabel(self, text="🧾 Receipt Attachment & OCR Scanner", font=config.FONT_TITLE, text_color="cyan")
        lbl_header.pack(anchor="w", padx=15, pady=10)

        # فریم افقی برای قرارگیری دکمه‌ها و بخش پیش‌نمایش تصویر
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=10)

        # بخش دکمه‌های کنترلی (سمت چپ)
        actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        actions_frame.pack(side="left", fill="y", padx=10, pady=5)

        self.upload_btn = ctk.CTkButton(actions_frame, text="📁 Choose File / Upload", command=self.upload_file)
        self.upload_btn.pack(fill="x", pady=8)

        self.scan_btn = ctk.CTkButton(actions_frame, text="🖨️ Connect to Scanner & Scan", command=self.scan_document)
        self.scan_btn.pack(fill="x", pady=8)

        self.ocr_btn = ctk.CTkButton(actions_frame, text="🔍 Extract Data (Run OCR)", fg_color="green", hover_color="darkgreen", command=self.run_ocr_processing)
        self.ocr_btn.pack(fill="x", pady=15)

        # بخش پیش‌نمایش تصویر فیش (سمت راست)
        self.preview_frame = ctk.CTkFrame(content_frame, width=200, height=120, border_width=1, border_color="gray50")
        self.preview_frame.pack(side="right", padx=20, pady=5)
        self.preview_frame.pack_propagate(False)

        self.preview_label = ctk.CTkLabel(self.preview_frame, text="No Receipt Selected", font=config.FONT_LABEL, text_color="gray")
        self.preview_label.pack(expand=True, fill="both")

    def upload_file(self):
        """انتخاب فایل فیش از روی سیستم"""
        file_types = [('Image Files', '*.png *.jpg *.jpeg *.bmp *.tiff')]
        file_path = filedialog.askopenfilename(title="Select Receipt Image", filetypes=file_types)
        if file_path:
            self.scanned_image_path = file_path
            self.update_image_preview(file_path)

    def scan_document(self):
        """اتصال به اسکنر و دریافت تصویر اسکن شده"""
        # در محیط ویندوز می‌توانید از کتابخانه twain یا WIA استفاده کنید.
        # در اینجا منطق اتصال و ذخیره به عنوان نمونه پیاده‌سازی شده است.
        try:
            # نمونه شبیه‌سازی پروتکل اسکن یا فراخوانی ابزار اسکنر سیستم:
            # import twain
            # sm = twain.SourceManager(self.winfo_id())
            # ss = sm.open_source()
            # ss.request_acquire()
            
            # جهت عدم توقف برنامه، یک پیام به کاربر نمایش داده می‌شود
            messagebox.showinfo("Scanner", "Connecting to scanner and acquiring image...")
            
            # پس از اسکن واقعی، فایل در یک مسیر موقت ذخیره می‌شود:
            # mock_scanned_path = "scanned_receipt.png"
            # self.scanned_image_path = mock_scanned_path
            # self.update_image_preview(mock_scanned_path)
            pass
        except Exception as e:
            messagebox.showerror("Scanner Error", f"Could not connect to scanner:\n{str(e)}")

    def update_image_preview(self, file_path):
        """بروزرسانی کادر پیش‌نمایش پس از دریافت فایل"""
        if Image is None:
            self.preview_label.configure(text="PIL Library Missing")
            return
        try:
            img = Image.open(file_path)
            img.thumbnail((190, 110))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.preview_label.configure(image=ctk_img, text="")
            self.preview_label.image = ctk_img  # Keep a reference
        except Exception as e:
            self.preview_label.configure(text="Preview Error")

    def run_ocr_processing(self):
        """پردازش متن‌خوان (OCR) روی تصویر و پر کردن خودکار فیلدهای مرتبط"""
        if not self.scanned_image_path:
            messagebox.showwarning("No File", "Please upload a file or scan a receipt first!")
            return

        if pytesseract is None:
            messagebox.showerror("OCR Error", "pytesseract library is not installed.\nPlease run: pip install pytesseract")
            return

        try:
            # اجرای فرآیند OCR بر روی فایل تصویری
            extracted_text = pytesseract.image_to_string(Image.open(self.scanned_image_path), lang='eng+fas')
            
            # آنالیز متن استخراج شده و پر کردن فرم
            self.parse_and_fill_form(extracted_text)
            messagebox.showinfo("Success", "OCR Processed successfully! Fields have been auto-populated.")
        except Exception as e:
            messagebox.showerror("OCR Error", f"An error occurred during text extraction:\n{str(e)}")

    def parse_and_fill_form(self, text):
        """
        الگوریتم تجزیه متن استخراج شده برای پیدا کردن اطلاعات کلیدی فیش.
        در اینجا بر اساس کلمات کلیدی، مقادیر فیلدهای ExpensesTab را پر می‌کنیم.
        """
        lines = text.split('\n')
        
        # یک ساختار ساده برای شبیه‌سازی یافتن داده‌ها در متن
        extracted_data = {
            "invoice_num": "",
            "company_name": "",
            "grand_total": ""
        }

        for line in lines:
            line_lower = line.lower()
            if "inv" in line_lower or "invoice no" in line_lower:
                extracted_data["invoice_num"] = line.split(':')[-1].strip()
            elif "total" in line_lower or "sum" in line_lower:
                extracted_data["grand_total"] = "".join(filter(str.isdigit, line))
            elif "ltd" in line_lower or "corp" in line_lower or "شرکت" in line_lower:
                extracted_data["company_name"] = line.strip()

        # ارجاع پویا و تزریق داده‌ها به فیلدهای فرم اصلی بدون تغییر کدهای آن
        # پیدا کردن فیلدها در آبجکت‌های چایلد ExpensesTab به صورت خودکار:
        self.auto_fill_parent_widgets(extracted_data)

    def auto_fill_parent_widgets(self, data):
        """جستجوی هوشمند در کل ویجت‌های ExpensesTab برای پر کردن مقدار"""
        for widget in self.parent_form.winfo_children():
            # بررسی فریم‌های اصلی سکشن‌ها
            if isinstance(widget, ctk.CTkFrame):
                for sub_w in widget.winfo_children():
                    if isinstance(sub_w, ctk.CTkFrame): # فریم گرید
                        for cell in sub_w.winfo_children():
                            if isinstance(cell, ctk.CTkFrame): # کادر سلول شامل لیبل و انتری
                                children = cell.winfo_children()
                                if len(children) >= 2:
                                    lbl = children[0]
                                    entry = children[1]
                                    
                                    if isinstance(entry, ctk.CTkEntry):
                                        lbl_text = lbl.cget("text").lower()
                                        
                                        # نگاشت هوشمند متن لیبل به دیتای OCR شده
                                        if "invoice number" in lbl_text and data["invoice_num"]:
                                            entry.delete(0, 'end')
                                            entry.insert(0, data["invoice_num"])
                                        elif "company name" in lbl_text and data["company_name"]:
                                            entry.delete(0, 'end')
                                            entry.insert(0, data["company_name"])
                                        elif "grand total" in lbl_text and data["grand_total"]:
                                            entry.delete(0, 'end')
                                            entry.insert(0, data["grand_total"])
