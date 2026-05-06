print("Student Information Reporter")

student = {
    "Name": "Rexford Mensah",
    "Age": 20,
    "Grade": "A"
}

print("\nStudent Report:")
for key, value in student.items():
    print(f"{key}: {value}")
