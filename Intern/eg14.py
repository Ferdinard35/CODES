print("Guessing Game")
print("Let the games begin!")

secret_number = 1508

while True:
    try:
        num = int(input("Enter the secret number: "))
    except ValueError:
        print("Please enter a valid number.")
        continue

    if num == secret_number:
        print("YOU GOT IT!")
        break
    else:
        print("TRY AGAIN")
        want_hint = input("Do you want a hint? (yes/no): ").strip().lower()
        if want_hint == "yes":
            if num > secret_number:
                print("Hint: The number is lower than your guess.")
            else:
                print("Hint: The number is higher than your guess.")
