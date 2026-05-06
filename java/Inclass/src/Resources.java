public class Resources {
   private final String Accountnumber;
     private double balance =300_000_000 ;
     private int dailyLimit =15_00_00;
     private int amount;
     private boolean withdrawnToday;
    private int inputPin = 1508;
    public Resources(String Accountnumber, double balance, int dailyLimit, boolean withdrawnToday) {
        this.Accountnumber = Accountnumber;
        this.balance = balance;
        this.dailyLimit = dailyLimit;
    }

    public Resources() {
        this.Accountnumber = "";

    }

    public boolean validatepin(int pin) {
        if (pin==inputPin)
             return true;
        else {
            return false;
        }
    }
    public void withdraw(double balance,String pinInput) {
        validatepin(inputPin);
        if (amount<=balance ){

        }
    }
}

