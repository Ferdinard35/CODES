print("Inventory Stock Updater")

stock = {
    "Apples": 50,
    "Bananas": 30,
    "Oranges": 20,
    "Milk": 10
}

while True:
    product = input("Enter product to update (or 'done' to finish): ").title()

    if product.lower() == "done":
        break
    elif product in stock:
        quantity = int(input("Enter quantity to add: "))
        stock[product] += quantity
        print(f"{product} stock updated. New quantity: {stock[product]}")
    else:
        print("Product not found.")

print("\nFinal stock levels:")
for item, qty in stock.items():
    print(f"{item}: {qty}")
