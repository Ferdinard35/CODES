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
            System.out.println("Deposit successful. New balance: " + balance);
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

    public double getBalance() {
        return balance;
    }

    public String getAccountNumber() {
        return accountNumber;
    }
}





class Student {

    private String studentId;
    private String name;
    private int score;

    public void setStudentId(String studentId) {
        this.studentId = studentId;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setScore(int score) {

        if (score < 0 || score > 100) {
            System.out.println("Invalid score! Score must be between 0 and 100.");
        } else {
            this.score = score;
        }

    }

    public String getStudentId() {
        return studentId;
    }

    public String getName() {
        return name;
    }

    public int getScore() {
        return score;
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

    public double calculateAnnualSalary() {
        return salary * 12;
    }

}

class FullTimeEmployee extends Employee {

    double bonus;

    public FullTimeEmployee(String name, double salary, double bonus) {
        super(name, salary);
        this.bonus = bonus;
    }

    @Override
    public double calculateAnnualSalary() {
        return (salary * 12) + bonus;
    }

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
    public double calculateAnnualSalary() {
        return hoursWorked * hourlyRate * 12;
    }

}


class Vehicle {

    String brand;

    public Vehicle(String brand) {
        this.brand = brand;
    }

    public void startEngine() {
        System.out.println("Vehicle engine starting...");
    }

}

class Car extends Vehicle {

    public Car(String brand) {
        super(brand);
    }

    @Override
    public void startEngine() {
        System.out.println("Car engine started for brand: " + brand);
    }

}

class Motorcycle extends Vehicle {

    public Motorcycle(String brand) {
        super(brand);
    }

    @Override
    public void startEngine() {
        System.out.println("Motorcycle engine started for brand: " + brand);
    }

}



abstract class Payment {

    public abstract void processPayment(double amount);

}

class CreditCardPayment extends Payment {

    public void processPayment(double amount) {
        System.out.println("Processing credit card payment of " + amount);
    }

}

class MobileMoneyPayment extends Payment {

    public void processPayment(double amount) {
        System.out.println("Processing mobile money payment of " + amount);
    }

}

class BankTransferPayment extends Payment {

    public void processPayment(double amount) {
        System.out.println("Processing bank transfer payment of " + amount);
    }

}



interface ATMOperations {

    void withdraw(double amount);

    void deposit(double amount);

    void checkBalance();

}

class BankATM implements ATMOperations {

    private double balance = 0;

    public void withdraw(double amount) {

        if (amount > balance) {
            System.out.println("ATM: Insufficient balance.");
        } else {
            balance -= amount;
            System.out.println("ATM Withdrawal successful. Balance: " + balance);
        }

    }

    public void deposit(double amount) {

        if (amount <= 0) {
            System.out.println("ATM: Invalid deposit amount.");
        } else {
            balance += amount;
            System.out.println("ATM Deposit successful. Balance: " + balance);
        }

    }

    public void checkBalance() {
        System.out.println("ATM Balance: " + balance);
    }

}



public class Main {

    public static void main(String[] args) {

        BankAccount acc = new BankAccount("22303446", "Ferdinard  Afful Bentum", 6000);

        acc.deposit(250);
        acc.deposit(-900);
        acc.withdraw(150);
        acc.withdraw(1700);

        System.out.println();



        Student s = new Student();

        s.setStudentId("CS250");
        s.setName("Rexford");
        s.setScore(85);

        System.out.println("Student Grade: " + s.getGrade());

        s.setScore(78);

        System.out.println();


        FullTimeEmployee f = new FullTimeEmployee("Alex", 3000, 2000);
        PartTimeEmployee p = new PartTimeEmployee("Addo", 90, 15);

        System.out.println("Full-time annual salary: " + f.calculateAnnualSalary());
        System.out.println("Part-time annual salary: " + p.calculateAnnualSalary());

        System.out.println();


        Car car = new Car("Toyota");
        Motorcycle bike = new Motorcycle("Yamaha");

        car.startEngine();
        bike.startEngine();

        System.out.println();



        List<Payment> payments = new ArrayList<>();

        payments.add(new CreditCardPayment());
        payments.add(new MobileMoneyPayment());
        payments.add(new BankTransferPayment());

        for (Payment pay : payments) {
            pay.processPayment(100);
        }

        System.out.println();



        BankATM atm = new BankATM();

        atm.deposit(900);
        atm.withdraw(290);
        atm.checkBalance();

    }

}
