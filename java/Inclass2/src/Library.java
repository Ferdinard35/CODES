public class Library {
    private final int isbn;
    private final String title;
    private final String author;
    private final String publisher;
    int totalCopies;
    int availableCopies;

    public Library() {
        isbn = 22303446;
        title = "NICE AND SWEET";
        author = "DAVID MENSAH";
        publisher = "KBA PUBLISHING FIRM";
        totalCopies = 500;
        availableCopies = 350;
    }
    public void borrowBook() {

    }

    public void availableBook() {
        if (availableCopies > 0) {
            System.out.println("There are available copies.");
        } else {
            System.out.println("Sorry, There are no  available copies");
        }

    }
}
