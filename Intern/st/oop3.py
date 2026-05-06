class eligibility:
    def __init__(self, age):
        self.age = age

    @property
    def check(self):
        if self.age >= 18:
            return "eligible for voting"
        else:
            return "not eligible for voting"


# Running code to test the eligibility class
person1 = eligibility(20)
print(person1.check)
person2 = eligibility(5)
print(person2.check)
