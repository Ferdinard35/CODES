print("Marks Average Processor")


def calculate_average(marks):
    if len(marks) == 0:
        return 0
    return sum(marks) / len(marks)


marks = [85, 90, 78, 92, 88]
average = calculate_average(marks)
print("Average marks:", average)
