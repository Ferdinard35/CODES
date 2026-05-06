print("Secure Password Retry")
password = "1508"
attempts = 3
while attempts > 0:
    user_input = input("Enter the password: ")
    if user_input == password:
        print("Access granted!")
        break
    else:
        attempts -= 1
        print(f"Incorrect password. You have {attempts} attempts left.")
if attempts == 0:
    print("Access denied. You have used all your attempts.")
