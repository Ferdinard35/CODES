print("simple calculator program")
print("input the numbers you want to calculate")
num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))
print("select the operation you want to perform")
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")
operation = input("Enter the operation (1/2/3/4): ")
if operation == '1':
    result = num1 + num2
    print("The result of addition is: ", result)
elif operation == '2':
    result = num1 - num2
    print("The result of subtraction is: ", result)
elif operation == '3':
    result = num1 * num2
    print("The result of multiplication is: ", result)
elif operation == '4':
    calc = num1 / num2
    result = round(calc, 2)
    print("The result of division is: ", result)
else:
    print("Invalid operation selected.")
