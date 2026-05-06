def add(a, b):
    return a+b


def sub(a, b):
    return a-b


def add_num(*args):
    total = 0
    for num in args:
        total += num
    return total


students_info = {
    "Dan": {"age": 30, "city": "Accra"},
    "John": {"age": 25, "city": "Kumasi"}
}
