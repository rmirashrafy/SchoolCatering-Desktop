import os
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox

class FixedReceiptsTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Create directory for saving receipt images if it doesn't exist
        self.upload_dir = "saved_receipt_images"
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

        # In-memory database to store receipts during runtime
        self.saved_receipts = []
        self.selected_image_path = None

        # Grid configuration: 2 equal columns (Left: Form, Right: List)
        self.grid_columnconfigure(0, weight=1, uniform="col")
        self.grid_columnconfigure(1, weight=1, uniform="col")
        self.grid_rowconfigure(0, weight=1)

        # --- Section 1: Create New Receipt Form ---
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.form_title = ctk.CTkLabel(self.form_frame, text="Create New Receipt", font=("Arial", 18, "bold"))
        self.form_title.pack(pady=15)

        # Select Receipt Type
        self.type_label = ctk.CTkLabel(self.form_frame, text="Receipt Type:")
        self.type_label.pack(anchor="w", padx=20, pady=2)
        self.type_select = ctk.CTkOptionMenu(self.form_frame, values=["Water", "Electricity", "Gas", "Rent"])
        self.type_select.pack(fill="x", padx=20, pady=5)

        # Enter Amount
        self.amount_label = ctk.CTkLabel(self.form_frame, text="Amount:")
        self.amount_label.pack(anchor="w", padx=20, pady=2)
        self.amount_entry = ctk.CTkEntry(self.form_frame, placeholder_text="e.g. 500000")
        self.amount_entry.pack(fill="x", padx=20, pady=5)

        # Enter Date
        self.date_label = ctk.CTkLabel(self.form_frame, text="Date:")
        self.date_label.pack(anchor="w", padx=20, pady=2)
        self.date_entry = ctk.CTkEntry(self.form_frame, placeholder_text="YYYY/MM/DD")
        self.date_entry.pack(fill="x", padx=20, pady=5)

        # Upload Receipt Image
        self.image_label = ctk.CTkLabel(self.form_frame, text="Receipt Image:")
        self.image_label.pack(anchor="w", padx=20, pady=2)
        
        self.upload_btn = ctk.CTkButton(self.form_frame, text="Choose & Upload Receipt Image", command=self.upload_image)
        self.upload_btn.pack(fill="x", padx=20, pady=5)
        
        self.file_path_label = ctk.CTkLabel(self.form_frame, text="No image selected", text_color="gray", font=("Arial", 10))
        self.file_path_label.pack(anchor="w", padx=20, pady=2)

        # Submit Button
        self.submit_btn = ctk.CTkButton(self.form_frame, text="Save Receipt", fg_color="green", hover_color="darkgreen", command=self.save_receipt)
        self.submit_btn.pack(fill="x", padx=20, pady=25)


        # --- Section 2: Saved Receipts List ---
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.list_title = ctk.CTkLabel(self.list_frame, text="Saved Receipts History", font=("Arial", 18, "bold"))
        self.list_title.pack(pady=15)

        # Scrollable container for receipts
        self.scrollable_list = ctk.CTkScrollableFrame(self.list_frame, width=380, height=450)
        self.scrollable_list.pack(padx=10, pady=10, fill="both", expand=True)

    def upload_image(self):
        # Open file dialog to choose an image
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

        if not amount or not date:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        saved_img_name = "No Image"
        # Copy image to program directory if selected
        if self.selected_image_path:
            extension = os.path.splitext(self.selected_image_path)[1]
            safe_date = date.replace("/", "-")
            saved_img_name = f"{receipt_type}_{safe_date}{extension}"
            destination = os.path.join(self.upload_dir, saved_img_name)
            try:
                shutil.copy(self.selected_image_path, destination)
            except Exception as e:
                messagebox.showerror("Image Save Error", str(e))
                return

        # Store in list
        receipt_data = {
            "type": receipt_type,
            "amount": amount,
            "date": date,
            "image": saved_img_name
        }
        self.saved_receipts.append(receipt_data)

        # Reset Form
        self.amount_entry.delete(0, 'end')
        self.date_entry.delete(0, 'end')
        self.file_path_label.configure(text="No image selected", text_color="gray")
        self.selected_image_path = None

        # Update List UI
        self.update_receipts_list()
        messagebox.showinfo("Success", "Receipt saved successfully.")

    def update_receipts_list(self):
        # Clear existing widgets in scrollable list
        for widget in self.scrollable_list.winfo_children():
            widget.destroy()

        # Render receipts list (newest on top)
        for receipt in reversed(self.saved_receipts):
            item_frame = ctk.CTkFrame(self.scrollable_list, fg_color="#2b2b2b", corner_radius=8)
            item_frame.pack(fill="x", padx=5, pady=5)

            # Receipt info aligned to left
            info_text = f"Type: {receipt['type']} | Amount: {receipt['amount']} | Date: {receipt['date']}\nImage: {receipt['image']}"
            info_label = ctk.CTkLabel(item_frame, text=info_text, justify="left", anchor="w")
            info_label.pack(side="left", padx=10, pady=10)
