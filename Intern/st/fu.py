
def bonus(salary):
    if salary < 1000:
        return salary * 0.1
    elif salary < 2000:
        return salary * 0.15
    else:
        return salary * 0.2


salary = 1508.89
bonus_amount = bonus(salary)
print(f"Your bonus is: {bonus_amount:.2f}")


def largest_score_finder():
    scores = [85, 92, 78, 90, 88]
    largest_score = max(scores)
    return largest_score


print(f"The largest score is: {largest_score_finder()}")
