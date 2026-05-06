# for number in range(2, 9, 2):
#   print(number)
# print("we have 4even number")
count = 0
for number in range(1, 10):
    if number % 2 == 0:
        count += 1
        print(number)
print(f"we have {count}even numbers")
