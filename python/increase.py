def increment(number, by=1):
    return number + by


print(increment(2, 9))


def multiply(*numbers):
    total = 1
    for number in numbers:
        total *= number
    return total


print(multiply(2, 4, 5, 3))
