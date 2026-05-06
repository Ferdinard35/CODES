import java.util.ArrayList;
import java.util.List;

class BankAccount {
    private String accountNumber;
    private String accountHolderName;
    private double balance;

    public BankAccount(String accountNumber, String accountHolderName, double balance) {
        this.accountNumber = accountNumber;
        this.accountHolderName = accountHolderName;
        this.balance = balance;
    }

    public void deposit(double amount) {
        if (amount <= 0) {
            System.out.println("Error: Cannot deposit a negative amount.");
        } else {
            balance += amount;
            System.out.println("Deposit successful for " + accountHolderName + ". New balance: " + balance);
        }
    }

    public void withdraw(double amount) {
        if (amount > balance) {
            System.out.println("Error: Insufficient funds.");
        } else if (amount <= 0) {
            System.out.println("Error: Invalid withdrawal amount.");
        } else {
            balance -= amount;
            System.out.println("Withdrawal successful. New balance: " + balance);
        }
    }

    public double getBalance() { return balance; }
    public String getAccountNumber() { return accountNumber; }
}

// --- Student Management ---
class Student {
    private String studentId;
    private String name;
    private int score;

    public void setStudentId(String studentId) { this.studentId = studentId; }
    public void setName(String name) { this.name = name; }
    public void setScore(int score) {
        if (score < 0 || score > 100) {
            System.out.println("Invalid score! Score must be between 0 and 100.");
        } else {
            this.score = score;
        }
    }

    public String getGrade() {
        if (score >= 70) return "A";
        else if (score >= 60) return "B";
        else if (score >= 50) return "C";
        else if (score >= 45) return "D";
        else return "F";
    }
}


class Employee {
    String name;
    double salary;

    public Employee(String name, double salary) {
        this.name = name;
        this.salary = salary;
    }

    public double calculateAnnualSalary() { return salary * 12; }
}

class FullTimeEmployee extends Employee {
    double bonus;
    public FullTimeEmployee(String name, double salary, double bonus) {
        super(name, salary);
        this.bonus = bonus;
    }

    @Override
    public double calculateAnnualSalary() { return (salary * 12) + bonus; }
}

class PartTimeEmployee extends Employee {
    int hoursWorked;
    double hourlyRate;

    public PartTimeEmployee(String name, int hoursWorked, double hourlyRate) {
        super(name, 0);
        this.hoursWorked = hoursWorked;
        this.hourlyRate = hourlyRate;
    }

    @Override
    public double calculateAnnualSalary() { return hoursWorked * hourlyRate * 12; }
}


class Vehicle {
    String brand;
    public Vehicle(String brand) { this.brand = brand; }
    public void startEngine() { System.out.println("Vehicle engine starting..."); }
}

class Car extends Vehicle {
    public Car(String brand) { super(brand); }
    @Override
    public void startEngine() { System.out.println("Car [" + brand + "] engine purring smoothly."); }
}

class Motorcycle extends Vehicle {
    public Motorcycle(String brand) { super(brand); }
    @Override
    public void startEngine() { System.out.println("Motorcycle [" + brand + "] engine roaring to life."); }
}


abstract class Payment {
    public abstract void processPayment(double amount);
}

class CreditCardPayment extends Payment {
    public void processPayment(double amount) { System.out.println("Charging $" + amount + " to Credit Card."); }
}

class MobileMoneyPayment extends Payment {
    public void processPayment(double amount) { System.out.println("Processing Mobile Money transfer: $" + amount); }
}

class BankTransferPayment extends Payment {
    public void processPayment(double amount) { System.out.println("Executing Bank Wire for $" + amount); }
}

interface ATMOperations {
    void withdraw(double amount);
    void deposit(double amount);
    void checkBalance();
}

class BankATM implements ATMOperations {
    private double balance = 0;
    public void withdraw(double amount) {
        if (amount > balance) System.out.println("ATM: Insufficient funds.");
        else { balance -= amount; System.out.println("ATM: Dispensed "+ amount); }
    }
    public void deposit(double amount) {
        balance += amount;
        System.out.println("ATM: Accepted deposit of "+ amount);
    }
    public void checkBalance() { System.out.println("Current ATM Balance: " + balance); }
}


public class Main {
    public static void main(String[] args) {

        BankAccount acc = new BankAccount("99887766", "Kwame Mensah", 12500.50);
        acc.deposit(1200);
        acc.withdraw(5000);
        System.out.println();


        Student s = new Student();
        s.setStudentId("IT-2026");
        s.setName("Ama Serwaa");
        s.setScore(92);
        System.out.println(s.getGrade() + " grade for student: " + s.getGrade());
        System.out.println();


        FullTimeEmployee f = new FullTimeEmployee("Elena", 4500, 5000);
        PartTimeEmployee p = new PartTimeEmployee("Marcus", 120, 25);
        System.out.println("Elena's Annual: " + f.calculateAnnualSalary());
        System.out.println("Marcus's Annual: " + p.calculateAnnualSalary());
        System.out.println();


        Car car = new Car("Tesla");
        Motorcycle bike = new Motorcycle("Ducati");
        car.startEngine();
        bike.startEngine();
        System.out.println();


        List<Payment> payments = new ArrayList<>();
        payments.add(new CreditCardPayment());
        payments.add(new MobileMoneyPayment());
        payments.add(new BankTransferPayment());
        for (Payment pay : payments) {
            pay.processPayment(250.75);
        }
        System.out.println();

        BankATM atm = new BankATM();
        atm.deposit(5000);
        atm.withdraw(1200);
        atm.checkBalance();
    }
}