print("SHOPPING BASKET TOTALIZER")
print("How many  items did you buy?")
items = int(input("Total number "))
list = []
for i in range(items):
    print("Price of item", i + 1)
    price = float(input("Price "))
    list.append(price)
print("Total cost of items in the basket is: ", sum(list))
