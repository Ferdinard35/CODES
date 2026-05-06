import java.util.Scanner;

public class Do {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Number:");
        int number= sc.nextInt();
        if(number % 5==0 && number % 3==0){
            System.out.println("Frizzbuzz");
        } else if (number % 5 ==0) {
            System.out.println("Frizz");
        } else if (number % 3==0) {
            System.out.println("buzz");
        }
        else {
            System.out.println(number);
        }

    }
}