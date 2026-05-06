

import java.text.NumberFormat;
import java.util.Scanner;

public class Main {
    private static Math math;

    public static void main(String[] args) {
        final byte monthsInYear = 12;
        final byte percent = 100;
        int years;
        int numberOfPayments;
        float annualInterestRate =0;
        float monthlyInterestRate;
        int principal =0;
        System.out.println("mortgage calculator");
        Scanner sc = new Scanner(System.in);

        while (true) {
            System.out.print("enter the principal: ");
            principal = sc.nextInt();
            if(principal >= 1000 && principal <= 1_000_000)
                break;
            System.out.println("enter a number between 1K and 1M");
        }

        while (true) {
            System.out.print("Annual Interest Rate: ");
            annualInterestRate = sc.nextFloat();
            if(annualInterestRate >= 1 && annualInterestRate <=30){
                monthlyInterestRate = annualInterestRate/percent/monthsInYear;
                break;
            }
            System.out.println("enter a rate between 1 and 30");
        }

        while (true) {
            System.out.print("Period(Years): ");
             years = sc.nextInt();
            if(years >= 1 && years <= 30){
                 numberOfPayments = years*12;
                break;
            }
            System.out.println("enter a year between 1 and 30");
        }

        double mortgage = principal*(monthlyInterestRate*math.pow(1+monthlyInterestRate,numberOfPayments)/math.pow(1+monthlyInterestRate,numberOfPayments)-1);
        String mortgageFormatted = NumberFormat.getCurrencyInstance().format(mortgage);
        System.out.println("Mortgage"+mortgageFormatted);
    }
}