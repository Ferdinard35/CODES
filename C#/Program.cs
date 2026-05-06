using System;
using System.Collections.Generic;

namespace Assignment
{
    class BankAccount
    {
        private string accountNumber;
        private string accountHolderName;
        private double balance;

        public BankAccount(string accountNumber, string accountHolderName, double initialBalance)
        {
            this.accountNumber = accountNumber;
            this.accountHolderName = accountHolderName;
            this.balance = initialBalance;
        }

        public void Deposit(double amount)
        {
            if (amount <= 0)
                Console.WriteLine("Error: Deposit amount must be positive.");
            else
            {
                balance += amount;
                Console.WriteLine("Deposited " + amount + ". New Balance: " + balance);
            }
        }

        public void Withdraw(double amount)
        {
            if (amount > balance)
                Console.WriteLine("Error: Insufficient funds.");
            else
            {
                balance -= amount;
                Console.WriteLine("Withdrew " + amount + ". Remaining Balance: " + balance);
            }
        }

        public double GetBalance() { return balance; }
        public string GetAccountNumber() { return accountNumber; }
    }

    class Student
    {
        private string studentId = "";
        private string name = "";
        private double score;

        public string StudentId
        {
            get { return studentId; }
            set { studentId = value ?? ""; }
        }

        public string Name
        {
            get { return name; }
            set { name = value ?? ""; }
        }

        public double Score
        {
            get { return score; }
            set
            {
                if (value >= 0 && value <= 100)
                    score = value;
                else
                    Console.WriteLine("Error: Score " + value + " is out of range (0-100).");
            }
        }

        public string GetGrade()
        {
            if (score >= 70) return "A";
            if (score >= 60) return "B";
            if (score >= 50) return "C";
            if (score >= 45) return "D";
            return "F";
        }
    }

    class Employee
    {
        public string Name { get; set; } = "";
        public double MonthlySalary { get; set; }

        public virtual double CalculateAnnualSalary()
        {
            return MonthlySalary * 12;
        }
    }

    class FullTimeEmployee : Employee
    {
        public double Bonus { get; set; }

        public override double CalculateAnnualSalary()
        {
            return (MonthlySalary * 12) + Bonus;
        }
    }

    class PartTimeEmployee : Employee
    {
        public int HoursWorked { get; set; }
        public double HourlyRate { get; set; }

        public override double CalculateAnnualSalary()
        {
            return (HoursWorked * HourlyRate) * 12;
        }
    }

    class Vehicle
    {
        public string Brand { get; set; } = "";

        public virtual void StartEngine()
        {
            Console.Write(Brand + " engine is starting: ");
        }
    }

    class Car : Vehicle
    {
        public override void StartEngine()
        {
            base.StartEngine();
            Console.WriteLine("Vroom! The car is idling smoothly.");
        }
    }

    class Motorcycle : Vehicle
    {
        public override void StartEngine()
        {
            base.StartEngine();
            Console.WriteLine("Pop! The bike is roaring to life.");
        }
    }

    abstract class Payment
    {
        public abstract void ProcessPayment(double amount);
    }

    class CreditCardPayment : Payment
    {
        public override void ProcessPayment(double amount)
        {
            Console.WriteLine("Paid " + amount + " via Credit Card.");
        }
    }

    class MobileMoneyPayment : Payment
    {
        public override void ProcessPayment(double amount)
        {
            Console.WriteLine("Paid " + amount + " via Mobile Money.");
        }
    }

    class BankTransferPayment : Payment
    {
        public override void ProcessPayment(double amount)
        {
            Console.WriteLine("Paid " + amount + " via Bank Transfer.");
        }
    }

    interface IATMOperations
    {
        void Withdraw(double amount);
        void Deposit(double amount);
        void CheckBalance();
    }

    class BankATM : IATMOperations
    {
        private double balance = 5000.0;

        public void Withdraw(double amount)
        {
            if (amount > balance)
                Console.WriteLine("ATM: Insufficient funds.");
            else
            {
                balance -= amount;
                Console.WriteLine("ATM: Dispensed " + amount + ".");
            }
        }

        public void Deposit(double amount)
        {
            balance += amount;
            Console.WriteLine("ATM: Accepted deposit of " + amount + ".");
        }

        public void CheckBalance()
        {
            Console.WriteLine("ATM: Current Balance is " + balance + ".");
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("--- Task 1: Bank Account ---");
            BankAccount acc = new BankAccount("22303446464", "Benson Adom", 1000.0);
            acc.Deposit(500);
            acc.Deposit(-50);
            acc.Withdraw(200);
            acc.Withdraw(5000);

            Console.WriteLine("\n--- Task 2: Student Grade ---");
            Student s = new Student();
            s.StudentId = "22303446";
            s.Name = "Bentum Afful Ferdinard";
            s.Score = 40;
            s.Score = 75;
            Console.WriteLine("Grade: " + s.GetGrade());

            Console.WriteLine("\n--- Task 3: Employee Inheritance ---");
            FullTimeEmployee ft = new FullTimeEmployee
            {
                Name = "Adeline Asare",
                MonthlySalary = 3000,
                Bonus = 5000
            };

            PartTimeEmployee pt = new PartTimeEmployee
            {
                Name = "Martin Mensah",
                HoursWorked = 40,
                HourlyRate = 25
            };

            Console.WriteLine(ft.Name + " Annual Salary: " + ft.CalculateAnnualSalary());
            Console.WriteLine(pt.Name + " Annual Salary: " + pt.CalculateAnnualSalary());

            Console.WriteLine("\n--- Task 4: Vehicle Overriding ---");
            Vehicle car = new Car { Brand = "Toyota" };
            Vehicle bike = new Motorcycle { Brand = "Yamaha" };
            car.StartEngine();
            bike.StartEngine();

            Console.WriteLine("\n--- Task 5: Payment Polymorphism ---");
            List<Payment> payments = new List<Payment>
            {
                new CreditCardPayment(),
                new MobileMoneyPayment(),
                new BankTransferPayment()
            };

            foreach (var p in payments)
                p.ProcessPayment(150.0);

            Console.WriteLine("\n--- Task 6: ATM Interface ---");
            IATMOperations atm = new BankATM();
            atm.CheckBalance();
            atm.Deposit(1000);
            atm.Withdraw(500);
        }
    }
}

