import json
import os
from datetime import datetime
from difflib import get_close_matches


Snack_Menu = {
    "Pasta": 50,
    "Pizza": 80,
    "Noodles": 90,
    "Salad": 60,
    "Burger": 120,
    "Thukpa": 50,
    "Chicken Chilli": 150
}

Khana_Menu = {
    "Veg Khana Set": 200,
    "Chicken Khana Set": 250,
    "Mutton Khana Set": 300
}

Drink_Menu = {
    "Milk Tea": 35,
    "Lemon Tea": 20,
    "Cold Drink": 200,
    "Cold Coffee": 115,
    "Hot Coffee": 105,
    "Fruit Juice": 135,
    "Mocktail": 150
}

Momo_Menu = {
    "Veg Momo": 70,
    "Chicken Momo": 120,
    "Mutton Momo": 150
}

Dessert_Menu = {
    "Chocolate Pastries": 160,
    "Black Forest Pastries": 120,
    "Gulab Jamun": 25,
    "Falooda": 125,
    "Rasmalai": 100,
    "Gajar Ka Halwa": 115
}

default_menu = Snack_Menu | Khana_Menu | Drink_Menu | Momo_Menu | Dessert_Menu

try:

    with open("menu.json", "r") as file:
        Menu = json.load(file)

except:

    Menu = default_menu

    with open("menu.json", "w") as file:
        json.dump(Menu, file, indent=4)
        
ADMIN_PASSWORD = "1234"

try:
    with open("receipt_no.txt", "r") as f:
        receipt_no = int(f.read())
except:
    receipt_no = 1

with open("receipt_no.txt", "w") as f:
    f.write(str(receipt_no + 1))

ordered_items = []
sales_count = {}
order_total = 0

categories = {
    "1": ("Snack", Snack_Menu),
    "2": ("Khana", Khana_Menu),
    "3": ("Drink", Drink_Menu),
    "4": ("Momo", Momo_Menu),
    "5": ("Dessert", Dessert_Menu)
}

def show_menu_numbered(category_dict):
    items = list(category_dict.items())
    for i, (name, price) in enumerate(items, start=1):
        print(f"{i}. {name} : Rs.{price}")
    return items

def get_item_by_number(items, choice):
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(items):
            return items[idx]
        return None
    except:
        return None
    
print("\n===== WELCOME TO KAVYA BAKERY & RESTAURANT =====")

with open("visitors.txt", "a") as f:
    f.write("1\n")

start = input("\nPress Enter to Order items : ").lower().strip()

# ================= ADMIN PANEL =================

if start == "admin":

    password = input("Enter admin password: ")

    if password == ADMIN_PASSWORD:

        while True:

            print("\n========== ADMIN PANEL ==========")
            print("1. View Report")
            print("2. Add Item")
            print("3. Remove Item")
            print("4. Update Price")
            print("5. Show Full Menu")
            print("6. Exit")
            print("7. Search Item")
            

            admin_choice = input("Enter choice: ")
            
            if admin_choice == "1":

                print("\n========== BUSINESS REPORT ==========")

                # 1. Revenue & Orders
                total_revenue = 0
                total_orders = 0

                try:
                    with open("sales.txt", "r") as f:
                        for line in f:
                            date, amount = line.strip().split(",")
                            total_revenue += float(amount)
                            total_orders += 1
                except:
                    pass

                # 2. Customers
                try:
                    with open("customers.txt", "r") as f:
                        total_customers = len(f.readlines())
                except:
                    total_customers = 0

                # 3. Visitors
                try:
                    with open("visitors.txt", "r") as f:
                        total_visitors = len(f.readlines())
                except:
                    total_visitors = 0

                # 4. Conversion Rate (SAFE)
                if total_visitors > 0:
                    conversion_rate = (total_orders / total_visitors) * 100
                else:
                    conversion_rate = 0

                # 5. Item Sales
                item_sales = {}

                try:
                    with open("items_sales.txt", "r") as f:
                        for line in f:
                            item, qty = line.strip().split(",")
                            item_sales[item] = item_sales.get(item, 0) + int(qty)
                except:
                    pass

                # 6. Most sold item
                if item_sales:
                    most_sold_item = max(item_sales, key=item_sales.get)
                    most_sold_qty = item_sales[most_sold_item]
                else:
                    most_sold_item = "N/A"
                    most_sold_qty = 0

                # 7. PRINT REPORT
                print(f"\nTotal Revenue      : Rs.{total_revenue:.2f}")
                print(f"Total Customers    : {total_customers}")
                print(f"Total Orders       : {total_orders}")
                print(f"Total Visitors     : {total_visitors}")
                print(f"Conversion Rate    : {conversion_rate:.2f}%")
                print(f"Most Sold Item     : {most_sold_item}")
                print(f"Quantity Sold      : {most_sold_qty}")

                print("\n========== ITEM SALES GRAPH ==========")

                for item, qty in sorted(item_sales.items(), key=lambda x: x[1], reverse=True):
                    print(f"{item:<25} {'█' * min(qty, 50)} ({qty})")

            elif admin_choice == "2":

                item = input("Enter new item name: ").title().strip()

                if item == "":
                    print("Item name cannot be empty!")
                    continue

                if item in Menu:
                    print("Item already exists!")
                    continue

                try:
                    price = float(input("Enter price: "))

                except ValueError:
                    print("Invalid price!")
                    continue

                Menu[item] = price

                with open("menu.json", "w") as file:
                    json.dump(Menu, file, indent=4)

                print(f"{item} added successfully!")

            elif admin_choice == "3":
                item = input("Enter item name to remove: ").title()

                if item in Menu:
                    del Menu[item]

                    with open("menu.json", "w") as file:
                        json.dump(Menu, file, indent=4)

                    print(f"{item} removed successfully!")
                else:
                    print("Item not found!")

            elif admin_choice == "4":
                item = input("Enter item name: ").title()

                if item in Menu:
                    new_price = float(input("Enter new price: "))
                    Menu[item] = new_price

                    with open("menu.json", "w") as file:
                        json.dump(Menu, file, indent=4)

                    print(f"{item} price updated!")
                else:
                    print("Item not found!")

            elif admin_choice == "5":
                print("\n===== FULL MENU =====")
                for item, price in Menu.items():
                    print(f"{item} = Rs.{price}")

            elif admin_choice == "6":

                print("Exiting...")
                break

            elif admin_choice == "7":

                search = input("Enter item name to search: ").title()

                found = False

                for item, price in Menu.items():

                    if search in item:

                        print(f"{item} = Rs.{price}")
                        found = True

                if not found:
                    print("Item not found!")

            else:

                print("Invalid choice!")

    else:
        print("Wrong password!")
        exit()

while True:

    print("\nSelect Category:")
    for k, v in categories.items():
        print(f"{k}. {v[0]}")

    cat_choice = input("Enter category number: ").strip()

    if cat_choice not in categories:
        print("Invalid category!")
        continue

    category_name, category_menu = categories[cat_choice]

    print(f"\n--- {category_name} MENU ---")

    items_list = show_menu_numbered(category_menu)

    item_choice = input("\nEnter item number you want to order: ").strip()

    selected = get_item_by_number(items_list, item_choice)

    if not selected:
        print("Invalid item selection!")
        continue

    item_name, price = selected

    try:
        qty = int(input("Enter the quantity you want to Order: "))
        if qty <= 0:
            print("Invalid quantity")
            continue
    except:
        print("Invalid input")
        continue

    found = False

    for i in range(len(ordered_items)):

        item, old_qty = ordered_items[i]

        if item == item_name:
            ordered_items[i] = (item, old_qty + qty)
            found = True
            break

    if not found:
        ordered_items.append((item_name, qty))
    order_total += Menu[item_name] * qty
    sales_count[item_name] = sales_count.get(item_name, 0) + qty

    more = input("Do you want to add more items? (yes/no): ").lower()
    if more != "yes":
        break

if order_total == 0:
    print("No order placed.")
    exit()

tax = order_total * 0.13
discount = order_total * 0.10 if order_total >= 1000 else 0
grand_total = order_total + tax - discount

with open("customers.txt", "a") as f:
    f.write("1\n")

with open("sales.txt", "a") as f:
    today = datetime.now().strftime("%d-%m-%Y")
    f.write(f"{today},{grand_total}\n")
    
with open("items_sales.txt", "a") as f:
    for item, qty in ordered_items:
        f.write(f"{item},{qty}\n")
    
while True:

    payment_method = input("Enter payment method (Cash/Card/Online): ").lower().strip()

    if payment_method in ["cash", "card", "online"]:
        break

    else:
        print("Invalid input! Please enter Cash, Card, or Online.")

now = datetime.now()
current_time = now.strftime("%d-%m-%Y %I:%M:%S")

print("\n=======================================")
print("   KAVYA BAKERY & RESTAURANT")
print("========================================")

print("Welcome and Thank You for Visiting")


print(f"Receipt No : {receipt_no}")
print(f"Date & Time : {current_time}")
print(f"Payment Mode : {payment_method.title()}")

print("\n------------------ RECEIPT --------------------")

print(f"{'Item':<25}{'Price':<10}{'Qty':<10}{'Total'}")

for item, qty in ordered_items:

    price = Menu[item]
    total = price * qty

    print(f"{item:<25}{price:<10}{qty:<10}Rs.{total}")
    

print("\n-----------------------------------------------")
print(f"Subtotal      = Rs.{order_total:.2f}")
print(f"VAT (13%)     = Rs.{tax:.2f}")
print(f"Discount      = Rs.{discount:.2f}")
print(f"Grand Total   = Rs.{grand_total:.2f}")

print("\nThank You! Visit Again 😊")
print("=====================================================")

filename = f"receipt_{receipt_no}.txt"

with open(filename, "w") as file:
    file.write("\n=======================================\n")
    file.write("KAVYA BAKERY & RESTAURANT\n\n")
    file.write("========================================\n")


    file.write(f"Receipt No: {receipt_no}\n")
    file.write(f"Date: {current_time}\n\n")
    file.write(f"Payment Mode : {payment_method.title()}\n\n")
    
    file.write("------------------- ITEMS --------------------\n")
    
    file.write(f"{'Item':<25}{'Price':<10}{'Qty':<10}{'Total'}\n")

    for item, qty in ordered_items:

        price = Menu[item]
        total = price * qty

        file.write(f"{item:<25}{price:<10}{qty:<10}Rs.{total}\n")
    

    file.write("\n------------------------------------------\n")
    file.write(f"Subtotal      = Rs.{order_total:.2f}\n")
    file.write(f"VAT (13%)     = Rs.{tax:.2f}\n")
    file.write(f"Discount      = Rs.{discount:.2f}\n")
    file.write(f"Grand Total   = Rs.{grand_total:.2f}\n")
    file.write("\nThank You! Visit Again 😊\n")
    
print(f"\nReceipt saved as {filename}")

try:
    os.startfile(filename, "print")

except:
    print("Printer not connected.")
receipt_no += 1

with open("receipt_no.txt", "w") as f:
    f.write(str(receipt_no))