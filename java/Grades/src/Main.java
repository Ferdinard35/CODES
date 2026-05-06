public class Main {
        public static void main(String[] args) {
            GradeManager manager = new GradeManager();

            // Testing different scenarios
            System.out.print("95.5: ");
            manager.executeGradeReport(95.5);

            System.out.print("-5: ");
            manager.executeGradeReport(-5);
        }
    }
