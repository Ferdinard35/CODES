class bank_account:
    def __init__(self, account_number, account_holder_name, balance=0.0):
        self.__account_number = account_number
        self.__account_holder_name = account_holder_name
        self.__balance = balance

    def deposit(self, amount):
        if amount <= 0:
            print("Error: Deposit amount must be positive.")
            return
        self.__balance += amount
        print(
            f"Deposited GHS {amount:.2f}. New balance: GHS {self.__balance:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Error: Withdrawal amount must be positive.")
            return
        if amount > self.__balance:
            print("Error: Insufficient funds.")
            return
        self.__balance -= amount
        print(
            f"Withdrew GHS {amount:.2f}. New balance: GHS {self.__balance:.2f}")

    def get_balance(self):
        return self.__balance

    def get_account_number(self):
        return self.__account_number

    def get_account_holder_name(self):
        return self.__account_holder_name


# Running code to test the BankAccount class
account = bank_account("22303446", "Rexford Badu", 1508.90)
account.deposit(500)
account.withdraw(200)
print(f"Current balance: GHS {account.get_balance():.2f}")
print(f"Account number: {account.get_account_number()}")
print(f"Account holder name: {account.get_account_holder_name()}")
