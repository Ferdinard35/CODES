print("Maximum of  a list of numbers")


def max_of_list(lst):
    if len(lst) == 0:
        return None
    max_num = lst[0]
    for num in lst:
        if num > max_num:
            max_num = num
    return max_num


numbers = [3, 7, 2, 9, 1]
print("The maximum number is:", max_of_list(numbers))
