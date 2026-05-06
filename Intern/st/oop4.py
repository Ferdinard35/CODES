class average:
    def __init__(self, marks):
        self.marks = marks

    def calculate(self):
        if all(mark >= 0 for mark in self.marks):
            return sum(self.marks) / len(self.marks)


# Running code to test the average class
marks = average([85, 90, 78, 92, 88])
print(marks.calculate())
