print("Attendance Analyzer")
print("Number  of Present students")


def count_present(register):
    count = 0

    for status in register:
        if status == "P":
            count = count + 1

    return count


attendance = ["P", "A", "P", "P", "A", "P", "P", "A", "P",
              "P", "P", "A", "P", "P", "A", "P", "P", "A", "P", "P"]

print("Number of present students:", count_present(attendance))
