print("Bus Seat Reservation Manager")
total_seats = 40
reserved_seats = 0
while reserved_seats < total_seats:
    user_input = input("Do you want to reserve a seat? (yes/no): ")
    if user_input.lower() == "yes":
        reserved_seats += 1
        print(
            f"Seat reserved. {total_seats - reserved_seats} seats remaining.")
    elif user_input.lower() == "no":
        print("Thank you for using the Bus Seat Reservation Manager.")
        break
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")
if reserved_seats == total_seats:
    print("All seats are reserved. No more seats available.")
