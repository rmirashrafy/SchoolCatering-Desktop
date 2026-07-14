import customtkinter as ctk

def init_theme():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

# Fonts
FONT_TITLE = ("Tahoma", 18, "bold")
FONT_LABEL = ("Tahoma", 12, "bold")
FONT_TEXT = ("Tahoma", 12)

# Menu Items (Structured as a Dictionary)
MENU_OPTIONS = {
    "Sandwiches": [
        "Chicken Shawarma",
        "Falafel",
        "Beef Kebab",
        "Chicken Kebab",
        "Beef Burger",
        "Chicken Burger",
        "Olivier Sandwich"
    ],
    "Pastry": [
        "Mini Chicken Pizza",
        "Mini Vegetable Pizza",
        "Chicken Puff",
        "Za'atar Bread"
    ],
    "Bread": [
        "Labneh Bread",
        "Labneh with Za'atar",
        "Labneh with Olives",
        "Cheese Bread"
    ],
    "Desserts": [
        "Plain Croissant",
        "Chocolate Croissant",
        "Cheese Croissant",
        "Za'atar Croissant",
        "Date Maamoul",
        "Cupcake",
        "Carrot Cake",
        "Plain Cake",
        "Donuts",
        "Cookies"
    ]
}

# Expenses
FIXED_EXPENSES = ["Rent", "Water", "Electricity", "Gas", "Employee Salary"]
MATERIAL_EXPENSES = ["Raw Materials", "Maintenance", "Transportation", "Fuel", "Kitchen Supplies"]
BUFFET_EXPENSES = ["Buffet Rent", "Buffet Staff Salary"]


'''


* Document ID (داخلی سیستم)
* Invoice Number
* Receipt Number
* Bill Number
* Order Number
* Check Number
* Sequence Number
* Batch Number
* Approval Number
* Reference Number
* Version
* Invoice Type

* Tax Invoice
* Simplified Tax Invoice
* Receipt
* Sales Invoice
* Purchase Invoice
* Credit Note
* Debit Note
* Status
* Currency
* Language
* Notes

---

# 2. اطلاعات فروشنده (Seller)

* Business Name
* Branch Name
* Branch Code
* Company Name
* Owner Name
* VAT Number
* Tax Registration Number
* Commercial Registration (CR)
* License Number
* Address
* Building
* Street
* Area
* City
* Country
* Postal Code
* Phone
* Mobile
* WhatsApp
* Email
* Website

---

# 3. اطلاعات خریدار (Customer)

* Customer Name
* Customer ID
* Customer Code
* Customer VAT Number
* Customer Phone
* Customer Address
* Customer Email
* Customer Type
* Call Name
* Contact Person

---

# 4. اطلاعات تاریخ و زمان

* Invoice Date
* Invoice Time
* Printed Date
* Printed Time
* Created Date
* Modified Date
* Delivery Date

---

# 5. اطلاعات پرداخت

* Payment Method

  * Cash
  * Visa
  * MasterCard
  * Bank Transfer
  * Credit
  * Wallet
  * Mixed

* Payment Status

* Paid Amount

* Remaining Amount

* Change Amount

* Card Number (Last 4 digits)

* Authorization Code

* Transaction ID

* POS Number

---

# 6. اطلاعات صندوق و سیستم

* Cashier Name
* Cashier ID
* Salesman
* Staff
* Operator
* Terminal ID (TID)
* Machine ID
* Device ID
* Register Number
* Shift Number
* Session Number

---

# 7. اطلاعات کالاها (Invoice Items)

برای هر ردیف:

* Line Number
* Item Code
* Barcode
* SKU
* Product Name
* Product Description
* Category
* Brand
* Batch Number
* Serial Number
* Unit
* Package
* Quantity
* Free Quantity
* Unit Price
* Gross Price
* Discount (%)
* Discount Amount
* Tax Rate
* Tax Amount
* Excise Tax
* Net Price
* Total Price
* Expiry Date
* Manufacturing Date
* Notes

---

# 8. جمع مبالغ

* Gross Amount
* Total Sales Amount
* Discount Amount
* VAT
* Excise Tax
* Other Taxes
* Service Charge
* Delivery Charge
* Additional Charges
* Net Amount
* Grand Total
* Paid Amount
* Balance

---

# 9. اطلاعات مالیات

* VAT Number
* VAT Rate
* VAT Amount
* VAT Inclusive
* VAT Exclusive
* Tax Amount
* Tax Type
* Tax Category

---

# 10. اطلاعات حمل و نقل

* Vehicle Number
* Plate Number
* Driver Name
* Delivery Person
* Delivery Method
* Route

---

# 11. اطلاعات مخصوص پمپ بنزین

* Fuel Station
* Pump Number
* Nozzle Number
* Product
* Fuel Type
* Fuel Grade
* Price Per Liter
* Volume (Liter)
* Odometer
* Vehicle Plate
* Vehicle ID
* Driver

---

# 12. اطلاعات مخصوص کافی‌شاپ و رستوران

* Table Number
* Order Type
* Dine In
* Take Away
* Pick Up
* Delivery
* Waiter
* Kitchen Order Number
* Guest Count

---

# 13. اطلاعات مخصوص فروش عمده

* Package Count
* Unit In Box
* Box Count
* Carton Count
* Retail Price
* Wholesale Price

---

# 14. اطلاعات امضا

* Customer Signature
* Seller Signature
* Receiver Signature
* Salesman Signature
* Department Head
* Stamp

---

# 15. اطلاعات چاپ

* Print Count
* Printed By
* Printer Name
* QR Code
* Barcode
* Logo

---

# 16. اطلاعات سیستمی

* Created By
* Updated By
* Deleted By
* Created At
* Updated At
* Deleted At
* Sync Status
* Backup Status

---

# 17. یادداشت‌ها

* Customer Note
* Internal Note
* Terms & Conditions
* Footer Message
* Thank You Message

---

# 18. اطلاعات کالا (Master Product Data)

این اطلاعات بهتر است در جدول جداگانه محصولات نگهداری شوند:

* Product ID
* Product Name
* Arabic Name
* English Name
* Barcode
* SKU
* Category
* Brand
* Purchase Price
* Selling Price
* Tax Rate
* Unit
* Minimum Stock
* Current Stock
* Supplier

---

## ساختار پیشنهادی فرم

برای اینکه فرم شلوغ نشود، آن را به تب‌های زیر تقسیم کن:

1. اطلاعات سند
2. فروشنده
3. مشتری
4. کالاها (جدول)
5. پرداخت
6. مالیات
7. حمل و نقل
8. اطلاعات اختصاصی (پمپ بنزین، رستوران و...)
9. جمع مبالغ
10. یادداشت و امضا

این ساختار تقریباً تمام اطلاعاتی را که در نمونه‌فیش‌های ارسالی دیده می‌شود و همچنین اکثر فاکتورهای فروش و خرید استاندارد را پوشش می‌دهد و پایه‌ی مناسبی برای یک نرم‌افزار حسابداری و مدیریت فاکتور خواهد بود.

'''
