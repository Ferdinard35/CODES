public class Main {
    public static void main(String[] args) {
        Room room = new Room(101, "Deluxe", 250.0);

        room.displayRoomInfo();

        room.checkIn("Ferdinard");
        room.displayRoomInfo();

        room.updatePrice(300.0); // won't change (occupied)

        room.checkOut();
        room.updatePrice(300.0); // now allowed
        room.displayRoomInfo();
    }
}
