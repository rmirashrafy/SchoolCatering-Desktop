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

