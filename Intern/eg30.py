print("Menu Driven ATM Simulation")
balance = 0
while True:
    print("\n1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        print(f"Your balance is: {balance}")
    elif choice == 2:
        amount = float(input("Enter the amount to deposit: "))
        balance += amount
        print(f"Your balance is: {balance}")
    elif choice == 3:
        amount = float(input("Enter the amount to withdraw: "))
        if amount <= balance:
            balance -= amount
            print(f"Your balance is: {balance}")
        else:
            print("Insufficient funds")
    elif choice == 4:
        print("Thank you for using the ATM. Goodbye!")
        break
    else:
        print("Invalid choice")
