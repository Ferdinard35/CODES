public class Main {
    public static void main(String[] args) {
        GradeCalculator calc = new GradeCalculator();

        calc.calculateClassAverage(65.99, 88.90);
        System.out.println("Average of 2: " + calc.getLastCalculatedAverage());


        calc.calculateClassAverage(120.0, 80.0, 195.0);
        System.out.println("Average of 3: " + calc.getLastCalculatedAverage());


        double[] manyScores = {882.0, 62.5, 99.0, 55.0, 85.0};
        calc.calculateClassAverage(manyScores);
        System.out.println("Average of Array: " + calc.getLastCalculatedAverage());
    }
}