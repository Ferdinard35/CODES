
    public class GradeCalculator {

        private double lastCalculatedAverage;


        public double getLastCalculatedAverage() {
            return lastCalculatedAverage;
        }


        public double calculateClassAverage(double score1, double score2) {
            this.lastCalculatedAverage = (score1 + score2) / 2;
            return this.lastCalculatedAverage;
        }


        public double calculateClassAverage(double score1, double score2, double score3) {
            this.lastCalculatedAverage = (score1 + score2 + score3) / 3;
            return this.lastCalculatedAverage;
        }

        public double calculateClassAverage(double[] scores) {
            if (scores.length == 0) return 0.0;

            double sum = 0;
            for (double score : scores) {
                sum += score;
            }
            this.lastCalculatedAverage = sum / scores.length;
            return this.lastCalculatedAverage;
        }
    }



