# age = 22
# message = "eligible" if age >= 18 else "not eligibe"
# print(message)
# high_income = True
# good_credit = True
# student = False
# if (high_income or good_credit) and not student:
#   print("allowed")
# else:
#   print("not allowed")

# for number in range(1, 10, 2):
# print("attempt", number)

successful = True
for number in range(3):
    print("Attempt")
    if successful:
        print("Successful")
        break
    else:
        print("Attempted 3times and failed ")
