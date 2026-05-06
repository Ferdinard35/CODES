username = "Ferdinard Afful Bentum"
password = 22303446

print("Welcome to the login page.")
print("Please enter your username and password to continue.")

user_input_username = input("Username: ")
user_input_password = int(input("Password: "))


def login(username, password):
    if username == user_input_username and password == user_input_password:
        return "Login successful"
    else:
        return "Login failed"


print(login(username, password))
