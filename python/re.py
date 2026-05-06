def fib(n):
    # Base case
    if n == 0 or n == 1:
        return n
    # Recursive case
    elif n > 1:
        return fib(n - 1) + fib(n - 2)
    # Error case
    else:
        print("Fibonacci numbers begin at 0.")

        # Test code
print(fib(7))
