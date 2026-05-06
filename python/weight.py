weight = float(input("how much do you weigh: "))
units = input("(K)g or (L)bs: ")
if units.upper() == "k":
    converted = weight // 0.45
    print(f"weight in Lbs: {converted}")
else:
    converted = weight * 0.45
    print(f"weight in kgs: {converted}")
