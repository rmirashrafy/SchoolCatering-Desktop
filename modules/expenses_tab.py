import customtkinter as ctk
from modules.receipt_ocr_handler import ReceiptOCRHandler
import config


class ExpensesTab(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, width=950, height=650)
        self.item_rows = []  # Holds dynamic product/item rows
        
        # 🟢 یک دیکشنری برای ذخیره ارجاع به تمام فیلدهای ورودی فرم بر اساس نام فیلد
        self.form_entries = {} 
        
        self.setup_ui()

    def setup_ui(self):
        # Main Title
        title_label = ctk.CTkLabel(self, text="Comprehensive Invoice & Expense Form", font=config.FONT_TITLE)
        title_label.pack(pady=15)

        # OCR Module Widget
        ocr_widget = ReceiptOCRHandler(self, parent_form=self)
        ocr_widget.pack(padx=20, pady=15, fill="x")

        # 1. Document Information Section
        self.create_section_box("1. Document Information", config.DOCUMENT_FIELDS)

        # 2. Seller Information Section
        #self.create_section_box("2. Seller Information", config.SELLER_FIELDS)

        # 3. Buyer Information Section
        # self.create_section_box("3. Buyer Information", config.BUYER_FIELDS)

        # 4. Items Table Section (Dynamic Rows)
        self.create_dynamic_items_section()

        # 5. Payment Information Section
        #self.create_section_box("2. Payment Information", config.PAYMENT_FIELDS)

        # 6. Tax and Shipping Section
        #self.create_section_box("5. Tax & Shipping Information", config.TAX_SHIPPING_FIELDS)

        # 7. Specialized Fields Section (Gas Station / Restaurant)
        #self.create_specialized_section()

        # 8. Totals and Notes Section
        self.create_totals_notes_section()

        # Submit button at the very bottom
        submit_btn = ctk.CTkButton(self, text="Save Invoice", command=self.submit_invoice, height=40, font=config.FONT_LABEL)
        submit_btn.pack(pady=30, padx=20, fill="x")

    def create_section_box(self, title, fields):
        """Creates a styled card/box with a section title containing a 2-column grid of inputs"""
        box = ctk.CTkFrame(self, border_width=1, border_color="gray30")
        box.pack(padx=20, pady=15, fill="x")

        # Section Header
        lbl_header = ctk.CTkLabel(box, text=title, font=config.FONT_TITLE, text_color="cyan")
        lbl_header.pack(anchor="w", padx=15, pady=10)

        # Grid Frame
        grid_frame = ctk.CTkFrame(box, fg_color="transparent")
        grid_frame.pack(fill="x", padx=10, pady=5)

        for i, (label_text, placeholder) in enumerate(fields):
            row = i // 2
            col = i % 2
            
            cell_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
            cell_frame.grid(row=row, column=col, padx=15, pady=8, sticky="ew")
            grid_frame.grid_columnconfigure(col, weight=1)

            lbl = ctk.CTkLabel(cell_frame, text=label_text, font=config.FONT_LABEL, anchor="w")
            lbl.pack(side="top", fill="x", padx=5)

            if isinstance(placeholder, list):
                entry = ctk.CTkComboBox(cell_frame, values=placeholder)
            else:
                entry = ctk.CTkEntry(cell_frame, placeholder_text=placeholder)
            entry.pack(side="top", fill="x", padx=5, pady=2)
            
            # 🟢 ذخیره ارجاع ویجت ورودی در دیکشنری براساس برچسب (Label) آن به عنوان کلید یکتا
            self.form_entries[label_text] = entry

    def create_dynamic_items_section(self):
        """Creates the dynamic items table within its own dedicated frame"""
        box = ctk.CTkFrame(self, border_width=1, border_color="gray30")
        box.pack(padx=20, pady=15, fill="x")

        # Section Header
        lbl_header = ctk.CTkLabel(box, text="4. Items & Services Table", font=config.FONT_TITLE, text_color="cyan")
        lbl_header.pack(anchor="w", padx=15, pady=10)

        # Control panel (Add button)
        control_frame = ctk.CTkFrame(box, fg_color="transparent")
        control_frame.pack(fill="x", pady=5)
        
        add_btn = ctk.CTkButton(control_frame, text="+ Add New Item", command=self.add_item_row)
        add_btn.pack(side="left", padx=15)

        # Table container
        self.table_frame = ctk.CTkFrame(box, fg_color="transparent")
        self.table_frame.pack(fill="x", padx=15, pady=5)

        # Header titles
        headers = ["Item Name / Barcode", "Qty", "Unit Price", "Discount (%)", "Tax (%)", "Total Price", "Action"]
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="gray25")
        header_frame.pack(fill="x", pady=2)
        
        for h in headers:
            lbl = ctk.CTkLabel(header_frame, text=h, font=config.FONT_LABEL, width=110)
            lbl.pack(side="left", padx=10, fill="x", expand=True)

        # Insert first row automatically
        self.add_item_row()

    def add_item_row(self):
        row_frame = ctk.CTkFrame(self.table_frame)
        row_frame.pack(fill="x", pady=2)

        name_entry = ctk.CTkEntry(row_frame, placeholder_text="Name / Barcode", width=110)
        qty_entry = ctk.CTkEntry(row_frame, placeholder_text="1", width=110)
        price_entry = ctk.CTkEntry(row_frame, placeholder_text="Price", width=110)
        discount_entry = ctk.CTkEntry(row_frame, placeholder_text="0", width=110)
        tax_entry = ctk.CTkEntry(row_frame, placeholder_text="9", width=110)
        total_lbl = ctk.CTkLabel(row_frame, text="0", font=config.FONT_LABEL, width=110)

        del_btn = ctk.CTkButton(row_frame, text="Delete", fg_color="red", hover_color="darkred", width=80,
                                 command=lambda rf=row_frame: self.remove_item_row(rf))

        name_entry.pack(side="left", padx=10, fill="x", expand=True)
        qty_entry.pack(side="left", padx=10, fill="x", expand=True)
        price_entry.pack(side="left", padx=10, fill="x", expand=True)
        discount_entry.pack(side="left", padx=10, fill="x", expand=True)
        tax_entry.pack(side="left", padx=10, fill="x", expand=True)
        total_lbl.pack(side="left", padx=10, fill="x", expand=True)
        del_btn.pack(side="right", padx=10)

        self.item_rows.append({
            "frame": row_frame,
            "name": name_entry,
            "qty": qty_entry,
            "price": price_entry,
            "discount": discount_entry,
            "tax": tax_entry,
            "total_lbl": total_lbl
        })

    def remove_item_row(self, row_frame):
        if len(self.item_rows) <= 1:
            return
        
        for item in self.item_rows:
            if item["frame"] == row_frame:
                item["frame"].destroy()
                self.item_rows.remove(item)
                break

    def create_specialized_section(self):
        """Creates specialized sub-sections for target business niches"""
        box = ctk.CTkFrame(self, border_width=1, border_color="gray30")
        box.pack(padx=20, pady=15, fill="x")

        # Main Header
        lbl_header = ctk.CTkLabel(box, text="6. Specialized Industry Fields", font=config.FONT_TITLE, text_color="cyan")
        lbl_header.pack(anchor="w", padx=15, pady=10)

        # Petrol Section Container
        petrol_frame = ctk.CTkFrame(box)
        petrol_frame.pack(fill="x", padx=15, pady=10)
        petrol_lbl = ctk.CTkLabel(petrol_frame, text="⛽ Fuel & Gas Station Details", font=config.FONT_LABEL, text_color="yellow")
        petrol_lbl.pack(anchor="w", padx=10, pady=5)
        
        self.create_grid_fields_sub(petrol_frame, config.GAS_STATION_FIELDS)

        # Restaurant Section Container
        rest_frame = ctk.CTkFrame(box)
        rest_frame.pack(fill="x", padx=15, pady=10)
        rest_lbl = ctk.CTkLabel(rest_frame, text="☕ Restaurant & Cafe Details", font=config.FONT_LABEL, text_color="yellow")
        rest_lbl.pack(anchor="w", padx=10, pady=5)

        self.create_grid_fields_sub(rest_frame, config.RESTAURANT_FIELDS)

    def create_totals_notes_section(self):
        """Creates bottom calculation panels and note taking textboxes"""
        box = ctk.CTkFrame(self, border_width=1, border_color="gray30")
        box.pack(padx=20, pady=15, fill="x")

        lbl_header = ctk.CTkLabel(box, text="7. Totals & Internal Notes", font=config.FONT_TITLE, text_color="cyan")
        lbl_header.pack(anchor="w", padx=15, pady=10)

        inner_frame = ctk.CTkFrame(box, fg_color="transparent")
        inner_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Left Column: Totals Calculations
        totals_frame = ctk.CTkFrame(inner_frame)
        totals_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.create_grid_fields_sub(totals_frame, config.TOTALS_FIELDS)

        # Right Column: Notes & Conditions Text Boxes
        notes_frame = ctk.CTkFrame(inner_frame)
        notes_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        lbl_notes = ctk.CTkLabel(notes_frame, text="Internal Notes & Comments:", font=config.FONT_LABEL)
        lbl_notes.pack(anchor="w", padx=10, pady=5)
        self.notes_txt = ctk.CTkTextbox(notes_frame, height=100)
        self.notes_txt.pack(fill="x", padx=10, pady=5)

        # lbl_terms = ctk.CTkLabel(notes_frame, text="Terms and Conditions / Footer Message:", font=config.FONT_LABEL)
        # lbl_terms.pack(anchor="w", padx=10, pady=5)
        # self.terms_txt = ctk.CTkTextbox(notes_frame, height=80)
        # self.terms_txt.pack(fill="x", padx=10, pady=5)

    def create_grid_fields_sub(self, parent_frame, fields):
        """Sub-helper method to populate sub-frames dynamically without outer margin overlaps"""
        grid_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=5, pady=5)

        for i, (label_text, placeholder) in enumerate(fields):
            row = i // 2
            col = i % 2
            
            cell_frame = ctk.CTkFrame(grid_frame, fg_color="transparent")
            cell_frame.grid(row=row, column=col, padx=10, pady=6, sticky="ew")
            grid_frame.grid_columnconfigure(col, weight=1)

            lbl = ctk.CTkLabel(cell_frame, text=label_text, font=config.FONT_LABEL, anchor="w")
            lbl.pack(side="top", fill="x", padx=5)

            if isinstance(placeholder, list):
                entry = ctk.CTkComboBox(cell_frame, values=placeholder)
            else:
                entry = ctk.CTkEntry(cell_frame, placeholder_text=placeholder)
            entry.pack(side="top", fill="x", padx=5, pady=2)
            
            # 🟢 ذخیره ارجاع به فیلدهای فرعی (مثل بخش پمپ‌بنزین، رستوران و مجموع‌ها)
            self.form_entries[label_text] = entry

    def submit_invoice(self):
        print("Submitting invoice payload to the backend...")
        for idx, item in enumerate(self.item_rows):
            name = item["name"].get()
            qty = item["qty"].get()
            price = item["price"].get()
            print(f"Row {idx+1}: Item={name} | Qty={qty} | Price={price}")
