print("Daily Expense Monitor")
daily_expense = []
expense = float(input("Enter your daily expense: "))
daily_expense.append(expense)
while True:
    more_expense = input("Do you want to add more expenses? (yes/no): ")
    if more_expense.lower() == "yes":
        expense = float(input("Enter your daily expense: "))
        daily_expense.append(expense)
    else:
        break
total_expense = sum(daily_expense)
print(f"Your total daily expense is: {total_expense}")
