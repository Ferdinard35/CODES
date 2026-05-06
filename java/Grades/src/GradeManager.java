public class GradeManager {

    public void executeGradeReport(double score) {
        if (!validateScore(score)) {
            System.out.println("Invalid Score");
            return;
        }

        char letterGrade = calculateLetterGrade(score);
        displayPerformanceMessage(letterGrade);
    }
    private boolean validateScore(double score) {
        return score >= 0 && score <= 100;
    }

    private char calculateLetterGrade(double score) {
        if (score >= 90) return 'A';
        if (score >= 80) return 'B';
        if (score >= 70) return 'C';
        if (score >= 60) return 'D';
        return 'F';
    }

    private void displayPerformanceMessage(char grade) {
        System.out.println("Performance Result: " + grade);
    }
}

