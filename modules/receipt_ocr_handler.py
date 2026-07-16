import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import config
import base64
import json
from PIL import Image
from openai import OpenAI

# تعریف کلاینت OpenAI
client = OpenAI(api_key="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") 

class ReceiptOCRHandler(ctk.CTkFrame):
    def __init__(self, master, parent_form):
        super().__init__(master, border_width=1, border_color="gray30")
        self.parent_form = parent_form
        self.scanned_image_path = None
        self.setup_ocr_ui()

    def setup_ocr_ui(self):
        lbl_header = ctk.CTkLabel(self, text="🧾 Receipt Attachment & AI OCR", font=config.FONT_TITLE, text_color="cyan")
        lbl_header.pack(anchor="w", padx=15, pady=10)

        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=10)

        actions_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        actions_frame.pack(side="left", fill="y", padx=10, pady=5)

        self.upload_btn = ctk.CTkButton(actions_frame, text="📁 Choose File / Upload", command=self.upload_file)
        self.upload_btn.pack(fill="x", pady=8)

        self.ocr_btn = ctk.CTkButton(actions_frame, text="🔍 Extract Data (AI OCR)", fg_color="green", hover_color="darkgreen", command=self.run_ocr_processing)
        self.ocr_btn.pack(fill="x", pady=15)

        self.preview_frame = ctk.CTkFrame(content_frame, width=200, height=120, border_width=1, border_color="gray50")
        self.preview_frame.pack(side="right", padx=20, pady=5)
        self.preview_frame.pack_propagate(False)

        self.preview_label = ctk.CTkLabel(self.preview_frame, text="No Receipt Selected", font=config.FONT_LABEL, text_color="gray")
        self.preview_label.pack(expand=True, fill="both")

    def upload_file(self):
        file_types = [('Image Files', '*.png *.jpg *.jpeg *.bmp *.tiff')]
        file_path = filedialog.askopenfilename(title="Select Receipt Image", filetypes=file_types)
        if file_path:
            self.scanned_image_path = file_path
            self.update_image_preview(file_path)

    def update_image_preview(self, file_path):
        try:
            img = Image.open(file_path)
            img.thumbnail((190, 110))
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            self.preview_label.configure(image=ctk_img, text="")
            self.preview_label.image = ctk_img
        except Exception as e:
            self.preview_label.configure(text="Preview Error")

    def encode_image_to_base64(self, image_path):
        """تبدیل تصویر به فرمت Base64 برای ارسال به API"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def run_ocr_processing(self):
        """ارسال تصویر به GPT-4o-mini و دریافت ساختار متنی انگلیسی"""
        if not self.scanned_image_path:
            messagebox.showwarning("No File", "Please upload a receipt first!")
            return

        try:
            base64_image = self.encode_image_to_base64(self.scanned_image_path)
            
            # ۱. استخراج لیست برچسب‌های موجود در فرم برای ساختن راهنمای پویای پرامپت
            known_labels = list(self.parent_form.form_entries.keys())
            labels_list_str = ", ".join([f'"{lbl}"' for lbl in known_labels])

            # ۲. نوشتن پرامپت دقیق برای دریافت خروجی کاملاً سازگار با فیلدهای فرم
            prompt_instruction = (
                "You are an advanced OCR system. Scan the receipt image, extract all fields in English, "
                "and align them with the provided form keys. Translate any Persian/Farsi details to English.\n\n"
                "Strictly return your output as a JSON object with this exact structure:\n"
                "{\n"
                "  \"form_fields\": {\n"
                "    \"Key From Provided List 1\": \"Extracted Value\",\n"
                "    \"Key From Provided List 2\": \"Extracted Value\"\n"
                "  },\n"
                "  \"items_table\": [\n"
                "    {\n"
                "      \"name\": \"Item Name or Description\",\n"
                "      \"qty\": \"Quantity\",\n"
                "      \"price\": \"Price per unit\",\n"
                "      \"discount\": \"Discount percentage or 0\",\n"
                "      \"tax\": \"Tax percentage or 9\"\n"
                "    }\n"
                "  ]\n"
                "}\n\n"
                f"Use ONLY keys from this list for the 'form_fields' dictionary: [{labels_list_str}]. "
                "If any field from this list is not found on the receipt, omit it or set its value to null. "
                "Do not invent keys outside of this list."
            )

            # ۳. ارسال درخواست به مدل
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text", 
                                "text": prompt_instruction
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1200
            )

            # ۴. پارس کردن پاسخ متنی دریافتی به JSON پایتون
            result_json = json.loads(response.choices[0].message.content)
            
            # ۵. پر کردن اتوماتیک فرم
            self.auto_fill_parent_widgets(result_json)
            messagebox.showinfo("Success", "AI OCR completed! Form fields populated successfully.")
            
        except Exception as e:
            messagebox.showerror("AI OCR Error", f"An error occurred during AI processing:\n{str(e)}")

    def auto_fill_parent_widgets(self, data):
        """تزریق هوشمند داده‌های استخراج شده به فیلدهای متناظر در فرم اصلی"""
        form_data = data.get("form_fields", {})
        
        # بخش اول: پر کردن تمامی فیلدهای تک سطری (Entry / ComboBox)
        for label, val in form_data.items():
            if label in self.parent_form.form_entries:
                entry_widget = self.parent_form.form_entries[label]
                
                # نادیده گرفتن مقادیر خالی یا ناهنجار
                if val in [None, "null", "NaN", "N/A", "None", ""]:
                    continue
                
                if isinstance(entry_widget, ctk.CTkEntry):
                    entry_widget.delete(0, 'end')
                    entry_widget.insert(0, str(val))
                elif isinstance(entry_widget, ctk.CTkComboBox):
                    entry_widget.set(str(val))

        # بخش دوم: پر کردن جدول پویا کالاها (Items Table) بدون ایجاد حلقه بی‌نهایت
        items_data = data.get("items_table", [])
        if items_data:
            # پاک کردن ردیف‌های اضافه قبلی به صورت ایمن (نگه داشتن ردیف اول برای ممانعت از کرش)
            while len(self.parent_form.item_rows) > 1:
                row_to_destroy = self.parent_form.item_rows[-1]["frame"]
                self.parent_form.remove_item_row(row_to_destroy)

            # پر کردن ردیف اول که همواره وجود دارد
            first_item = items_data[0]
            first_row = self.parent_form.item_rows[0]
            self._fill_row_data(first_row, first_item)

            # ساخت ردیف‌های جدید برای بقیه اقلام جدول
            for item in items_data[1:]:
                self.parent_form.add_item_row()
                new_row = self.parent_form.item_rows[-1]
                self._fill_row_data(new_row, item)

    def _fill_row_data(self, row, data_dict):
        """تابع کمکی برای درج امن مقادیر درون خانه‌های یک ردیف جدول"""
        fields_mapping = {
            "name": row["name"],
            "qty": row["qty"],
            "price": row["price"],
            "discount": row["discount"],
            "tax": row["tax"]
        }
        
        for key, entry_widget in fields_mapping.items():
            val = data_dict.get(key)
            if val not in [None, "null", "NaN", "N/A", "None", ""]:
                entry_widget.delete(0, 'end')
                entry_widget.insert(0, str(val))
