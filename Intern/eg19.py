print("Product Price Search Tool")
print("SMART DEVICES SHOP")
products = {
    "Laptop": 999.99,
    "Smartphone": 499.99,
    "Headphones": 199.99,
    "Smartwatch": 299.99,
    "Tablet": 399.99,
    "Printer": 149.99,
    "Camera": 599.99,
    "Monitor": 249.99,
    "Speaker": 89.99,
    "Keyboard": 49.99
}
print("Enter the product name to search for its price:")
product_name = input().strip().title()

if product_name in products:
    print(f"The price of {product_name} is {products[product_name]:.2f}")
else:
    print(f"Product {product_name} not found.")
