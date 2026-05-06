<?php

class BankAccount
{
    private $accountNumber;
    private $accountHolderName;
    private $balance;

    public function __construct($accountNumber, $name, $initialBalance)
    {
        $this->accountNumber = $accountNumber;
        $this->accountHolderName = $name;
        $this->balance = $initialBalance;
    }

    public function deposit($amount)
    {
        if ($amount <= 0) {
            echo "Error: Deposit amount must be positive" . "\n";
        } else {
            $this->balance += $amount;
            echo "Successfully deposited {$amount}" . "\n";
        }
    }

    public function withdraw($amount)
    {
        if ($amount > $this->balance) {
            echo "Error: Insufficient funds for withdrawal" . "\n";
        } else {
            $this->balance -= $amount;
            echo "Successfully withdrew {$amount}" . "\n";
        }
    }

    public function getBalance()
    {
        return $this->balance;
    }
    public function getAccountNumber()
    {
        return $this->accountNumber;
    }
}


class Student
{
    private $studentId;
    private $name;
    private $score;

    public function setScore($score)
    {
        if ($score >= 0 && $score <= 100) {
            $this->score = $score;
        } else {
            echo "Error: Invalid score ({$score}), Must be between 0 and 100" . "\n";
        }
    }

    public function getGrade()
    {
        if ($this->score >= 70) return "A";
        if ($this->score >= 60) return "B";
        if ($this->score >= 50) return "C";
        if ($this->score >= 45) return "D";
        return "F";
    }
}


class Employee
{
    protected $name;
    protected $salary;

    public function __construct($name, $salary)
    {
        $this->name = $name;
        $this->salary = $salary;
    }

    public function calculateAnnualSalary()
    {
        return $this->salary * 12;
    }
}

class FullTimeEmployee extends Employee
{
    private $bonus;

    public function __construct($name, $salary, $bonus)
    {
        parent::__construct($name, $salary);
        $this->bonus = $bonus;
    }

    public function calculateAnnualSalary()
    {
        return ($this->salary * 12) + $this->bonus;
    }
}

class PartTimeEmployee extends Employee
{
    private $hoursWorked;
    private $hourlyRate;

    public function __construct($name, $hours, $rate)
    {
        parent::__construct($name, 0);
        $this->hoursWorked = $hours;
        $this->hourlyRate = $rate;
    }

    public function calculateAnnualSalary()
    {
        return ($this->hoursWorked * $this->hourlyRate) * 12;
    }
}


class Vehicle
{
    protected $brand;

    public function __construct($brand)
    {
        $this->brand = $brand;
    }

    public function startEngine()
    {
        return "Starting the {$this->brand} engine: ";
    }
}

class Car extends Vehicle
{
    public function startEngine()
    {
        return parent::startEngine() . "Vroom vroom!" . "\n";
    }
}

class Motorcycle extends Vehicle
{
    public function startEngine()
    {
        return parent::startEngine() . "Brap brap!" . "\n";
    }
}


abstract class Payment
{
    abstract public function processPayment($amount);
}

class CreditCardPayment extends Payment
{
    public function processPayment($amount)
    {
        echo "Paid {$amount} via Credit Card" . "\n";
    }
}

class MobileMoneyPayment extends Payment
{
    public function processPayment($amount)
    {
        echo "Paid {$amount} via MoMo" . "\n";
    }
}


interface ATMOperations
{
    public function withdraw($amount);
    public function deposit($amount);
    public function checkBalance();
}

class BankATM implements ATMOperations
{
    private $currentBalance = 1000.0;
    public function withdraw($amount)
    {
        $this->currentBalance -= $amount;
        echo "ATM: Withdrew {$amount}" . "\n";
    }
    public function deposit($amount)
    {
        $this->currentBalance += $amount;
        echo "ATM: Deposited {$amount}" . "\n";
    }
    public function checkBalance()
    {
        echo "ATM Balance: {$this->currentBalance}" . "\n";
    }
}


$acc = new BankAccount("240454799", "Ferdinard Afful Bentum", 500);
$acc->deposit(200);
$acc->deposit(-50);
$acc->withdraw(100);
$acc->withdraw(2000);


$stu = new Student();
$stu->setScore(150);
$stu->setScore(85);
echo "Grade: " . $stu->getGrade() . "\n";


$ft = new FullTimeEmployee("Hafeez", 5000, 2000);
$pt = new PartTimeEmployee("Adam", 40, 50);
echo "FullTime Annual: {$ft->calculateAnnualSalary()}" . "\n";
echo "PartTime Annual: {$pt->calculateAnnualSalary()}" . "\n";

$myCar = new Car("Toyota");
echo $myCar->startEngine();


$payments = [new CreditCardPayment(), new MobileMoneyPayment()];
foreach ($payments as $p) {
    $p->processPayment(100);
}


$atm = new BankATM();
$atm->checkBalance();
$atm->deposit(500);
