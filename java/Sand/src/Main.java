import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Enter your mark: ");
        int score = input.nextInt();

        // Call the high-level method
        GradeReport.executeGradeReport(score);
    }
}

class GradeReport {

    // HIGH-LEVEL METHOD (Controller)
    public static void executeGradeReport(int score) {
        if (!validateScore(score)) {
            System.out.println("Invalid Score");
            return;
        }
        char grade = calculateLetterGrade(score);
        displayPerformanceMessage(grade);
    }

    // HELPER METHOD 1: Validation
    public static boolean validateScore(int score) {
        return score >= 0 && score <= 100;
    }

    // HELPER METHOD 2: Grade calculation
    public static char calculateLetterGrade(int score) {
        if (score >= 80) return 'A';
        else if (score >= 70) return 'B';
        else if (score >= 60) return 'C';
        else if (score >= 50) return 'D';
        else return 'F';
    }

    // HELPER METHOD 3: Output message
    public static void displayPerformanceMessage(char grade) {
        switch (grade) {
            case 'A':
                System.out.println("Excellent performance!");
                break;
            case 'B':
                System.out.println("Very good job!");
                break;
            case 'C':
                System.out.println("Good effort.");
                break;
            case 'D':
                System.out.println("You passed, but improve.");
                break;
            case 'F':
                System.out.println("You failed. Try harder next time.");
                break;
        }
    }
}
