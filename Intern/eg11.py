print("Students Grading System")
print("Input Your Marks")
Score = int(input("What Was Your Score: "))
if Score > 80:
    print("A   Execellent")
elif Score > 69:
    print("B  Very Good")
elif Score > 55:
    print(" C  Good")
elif Score > 35:
    print("D Pass ")
elif Score > 30:
    print("E Credit")
else:
    print("F Fail")
