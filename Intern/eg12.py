print("ATM WITHDRAWAL DECISION")
Account_balance = 2598.90
print("ENTER THE AMOUNT FOR THE WITHDRAWAL")
Amount = float(input("AMOUNT: "))
New_Balance: float = Account_balance - Amount
if Amount > Account_balance:
    print("Insufficient Funds")
else:
    print("Wait for the transaction process to complete")
print(f"Remaining balance is: {New_Balance}")
print(f"You took out {Amount}")
