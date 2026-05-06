class calculations:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b != 0:
            return a / b
        else:
            return "Cannot divide by zero"


# Running code to test the calculations class
cal = calculations()
print(cal.add(5, 9))
print(cal.subtract(10, 3))
print(cal.multiply(4, 6))
print(cal.divide(10, 2))
