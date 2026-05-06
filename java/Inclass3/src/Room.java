public class Room {
    private final int roomNumber;
    private String roomType;
    private double pricePerNight;
    private boolean isOccupied;
    private String guestName;

    public Room(int roomNumber, String roomType, double pricePerNight) {
        this.roomNumber = roomNumber;
        this.roomType = roomType;
        this.pricePerNight = pricePerNight;
        this.isOccupied = false;
        this.guestName = "";   // ✅ FIX
    }


    public void checkIn(String name) {
        if (!isOccupied) {
            guestName = name;
            isOccupied = true;
        }
    }

    public void checkOut() {
        isOccupied = false;
        guestName = "";
    }

    public void updatePrice(double newPrice) {
        if (!isOccupied) {
            pricePerNight = newPrice;
        }
    }

    public void displayRoomInfo() {
        System.out.println(
                "Room " + roomNumber +
                        " | Type: " + roomType +
                        " | Price: " + pricePerNight +
                        " | Occupied: " + isOccupied +
                        " | Guest: " + (guestName.isEmpty() ? "None" : guestName)
        );
    }
}
