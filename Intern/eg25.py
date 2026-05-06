print("Restaurant Ordering System")

menu = {
    "Burger": 5.99,
    "Pizza": 8.99,
    "Salad": 4.99,
    "Soda": 1.99,
    "Fries": 2.99,
    "Ice Cream": 3.99
}

total = 0
print("Menu:")
for item, price in menu.items():
    print(f"{item}: {price:.2f}")
while True:
    item = input("Enter item to order and done when finished: ").title()

    if item.lower() == "done":
        break
    elif item in menu:
        total += menu[item]
        print(f"{item} added.")
    else:
        print("Item not on menu.")

print(f"Total bill: {total:.2f}")
