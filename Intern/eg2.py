Age = int(input("Enter your age: "))
if Age < 18:
    print("Minor(Below 18)")
elif Age > 18 and Age < 59:
    print("Adult(18-59)")
else:
    print("Senior(60 and above)")
