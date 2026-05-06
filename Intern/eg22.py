print("Transaction Balance Calculator")

balance = 0

transactions = [100, -50, 200, -30, 606.90, -100.50]

for t in transactions:
    balance += t

print("Final balance:", balance)
