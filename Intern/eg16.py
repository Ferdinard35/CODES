print(" EMPLOYEE BONUS")
salary = float(input("Enter the salary: "))
years_of_service = int(input("Enter the years of service: "))


def calculate_bonus(salary, years_of_service):
    if years_of_service > 5:
        bonus = salary * 0.10
    else:
        bonus = salary * 0.05
    return bonus


bonus = calculate_bonus(salary, years_of_service)
print("The bonus is:", bonus)
