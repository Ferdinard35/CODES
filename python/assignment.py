from abc import ABC, abstractmethod


class BankAccount:
    def __init__(self, account_number, account_holder_name, initial_balance=0.0):
        self.__account_number = account_number
        self.__account_holder_name = account_holder_name
        self.__balance = initial_balance

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


class Student:
    def __init__(self, student_id, name, score):
        self.__student_id = student_id
        self.__name = name
        self.score = score

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        if not (0 <= value <= 100):
            raise ValueError(
                f"Invalid score {value}. Score must be between 0 and 100.")
        self.__score = value

    @property
    def name(self):
        return self.__name

    @property
    def student_id(self):
        return self.__student_id

    def get_grade(self):
        if self.__score >= 70:
            return "A"
        elif self.__score >= 60:
            return "B"
        elif self.__score >= 50:
            return "C"
        elif self.__score >= 45:
            return "D"
        else:
            return "F"


class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def calculate_annual_salary(self):
        return self.salary * 12


class FullTimeEmployee(Employee):
    def __init__(self, name, salary, bonus):
        super().__init__(name, salary)
        self.bonus = bonus

    def calculate_annual_salary(self):
        return super().calculate_annual_salary() + self.bonus


class PartTimeEmployee(Employee):
    def __init__(self, name, hours_worked, hourly_rate):
        super().__init__(name, salary=0)
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate

    def calculate_annual_salary(self):
        return self.hours_worked * self.hourly_rate * 52


class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def start_engine(self):
        print(f"{self.brand} engine starting...")


class Car(Vehicle):
    def start_engine(self):
        super().start_engine()
        print(f"{self.brand} car engine running smoothly.")


class Motorcycle(Vehicle):
    def start_engine(self):
        super().start_engine()
        print(f"{self.brand} motorcycle engine roaring.")


class Payment(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass


class CreditCardPayment(Payment):
    def process_payment(self, amount):
        print(f"Processing credit card payment of GHS {amount:.2f}")


class MobileMoneyPayment(Payment):
    def process_payment(self, amount):
        print(f"Processing mobile money payment of GHS {amount:.2f}")


class BankTransferPayment(Payment):
    def process_payment(self, amount):
        print(f"Processing bank transfer of GHS {amount:.2f}")


class ATMOperations(ABC):
    @abstractmethod
    def withdraw(self, amount):
        pass

    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def check_balance(self):
        pass


class BankATM(ATMOperations):
    def __init__(self, initial_balance=0.0):
        self.__balance = initial_balance

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid deposit amount.")
            return
        self.__balance += amount
        print(f"ATM: Deposited GHS {amount:.2f}.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid withdrawal amount.")
            return
        if amount > self.__balance:
            print("ATM: Insufficient funds.")
            return
        self.__balance -= amount
        print(f"ATM: Dispensing GHS {amount:.2f}.")

    def check_balance(self):
        print(f"ATM: Current balance is GHS {self.__balance:.2f}")


if __name__ == "__main__":

    acc = BankAccount("234908892", "Kwame Addo Mensah", 500.0)
    acc.deposit(200)
    acc.deposit(-50)
    acc.withdraw(100)
    acc.withdraw(1000)
    print(
        f"Account: {acc.get_account_number()} | Balance: GHS {acc.get_balance():.2f}")

    s = Student("22303446", "Ferdinard Afful Bentum", 75)
    print(f"{s.name} scored {s.score} Grade: {s.get_grade()}")
    s.score = 80
    print(f"Updated score: {s.score} Grade: {s.get_grade()}")
    try:
        s.score = 110
    except ValueError as e:
        print(f"Caught error: {e}")

    ft = FullTimeEmployee("Kofi Asante", 3000, 5000)
    pt = PartTimeEmployee("Abena Boateng", 20, 25)
    print(f"{ft.name} annual salary: GHS {ft.calculate_annual_salary():.2f}")
    print(f"{pt.name} annual salary: GHS {pt.calculate_annual_salary():.2f}")

    car = Car("Toyota")
    moto = Motorcycle("Yamaha")
    car.start_engine()
    moto.start_engine()

    payments = [CreditCardPayment(), MobileMoneyPayment(),
                BankTransferPayment()]
    amounts = [150.00, 75.50, 300.00]
    for payment, amount in zip(payments, amounts):
        payment.process_payment(amount)

    atm = BankATM(1000.0)
    atm.check_balance()
    atm.deposit(500)
    atm.withdraw(200)
    atm.withdraw(2000)
    atm.check_balance()
