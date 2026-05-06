class student:
    def __init__(self, name, age, grade):
        self.__name = name
        self.__age = age
        self.__grade = grade

    def get_student_name(self):
        return self.__name

    def get_student_age(self):
        return self.__age

    def student_grade(self):
        if self.__grade >= 90:
            return "A"
        elif self.__grade >= 80:
            return "B"
        elif self.__grade >= 70:
            return "C"
        elif self.__grade >= 60:
            return "D"
        elif self.__grade >= 50:
            return "E"
        else:
            return "F"

    def print_student_info(self):
        print(f"{self.__name} had a grade of {self.student_grade()}")


class course:
    def __init__(self, course_name, max_students,):
        self.__course_name = course_name
        self.__max_students = max_students
        self.__students = []

    def get_course_name(self):
        return self.__course_name

    def get_max_students(self):
        return self.__max_students

    def add_student(self, student):
        if len(self.__students) < self.__max_students:
            self.__students.append(student)
            return True
        else:
            return False


# Running code to test the student class
student1 = student("Rexford Badu", 20, 85)
student2 = student("Ama Serwaa", 22, 92)
student3 = student("Kofi Mensah", 19, 78)
print(student1.get_student_name())
print(student1.get_student_age())
print(student1.student_grade())
student1.print_student_info()
print("\n")
# Running code to test the course class
my_course = course("Mathematics", 3)
print(my_course.get_course_name())
print(my_course.get_max_students())
my_course.add_student(student1)
my_course.add_student(student2)
my_course.add_student(student3)
print(f"Students enrolled in {my_course.get_course_name()}:")
for student in my_course._course__students:
    print(student.get_student_name())
print("\n")
print(my_course._course__students[0].get_student_name())
