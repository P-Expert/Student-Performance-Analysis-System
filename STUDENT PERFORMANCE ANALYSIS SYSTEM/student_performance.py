import csv
from abc import ABC, abstractmethod


# Flexible method: accepts any number of marks.
# A default bonus of zero is used when no bonus is provided.
def calculate_average(*marks, bonus=0):
    if not marks:
        return 0

    average = sum(marks) / len(marks)
    return min(100, average + bonus)


# Abstract base class
class Student(ABC):

    def __init__(self, student_id, name, assignment_mark, exam_mark):
        self.__student_id = student_id
        self.__name = name
        self.__assignment_mark = float(assignment_mark)
        self.__exam_mark = float(exam_mark)

    # Encapsulation: access private attributes through properties.
    @property
    def student_id(self):
        return self.__student_id

    @property
    def name(self):
        return self.__name

    @property
    def assignment_mark(self):
        return self.__assignment_mark

    @property
    def exam_mark(self):
        return self.__exam_mark

    @abstractmethod
    def calculate_final_score(self):
        """Each student type must calculate its own final score."""
        pass

    @abstractmethod
    def get_student_type(self):
        """Each student type must identify itself."""
        pass

    def get_grade(self):
        score = self.calculate_final_score()

        if score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"

    def scholarship_eligible(self):
        return self.calculate_final_score() >= 85


# Inheritance: RegularStudent inherits from Student.
class RegularStudent(Student):

    def calculate_final_score(self):
        # Regular students receive equal weighting.
        return calculate_average(
            self.assignment_mark, self.exam_mark
        )

    # Method overriding
    def get_student_type(self):
        return "Regular"


# Inheritance: ScholarshipStudent also inherits from Student.
class ScholarshipStudent(Student):

    def calculate_final_score(self):
        # Scholarship students receive 40% assignment
        # weighting and 60% examination weighting.
        return (
            self.assignment_mark * 0.40
            + self.exam_mark * 0.60
        )

    # Method overriding
    def get_student_type(self):
        return "Scholarship"


# Analyze the performance of the whole class.
class PerformanceAnalyzer:

    def __init__(self, students):
        self.students = students

    def highest_score(self):
        return max(
            self.students,
            key=lambda student: student.calculate_final_score()
        )

    def lowest_score(self):
        return min(
            self.students,
            key=lambda student: student.calculate_final_score()
        )

    def class_average(self):
        if not self.students:
            return 0

        total = sum(
            student.calculate_final_score()
            for student in self.students
        )
        return total / len(self.students)

    def generate_report(self):
        print("\nSTUDENT PERFORMANCE ANALYSIS REPORT")
        print("=" * 90)

        print(
            f"{'ID':<8} {'Name':<12} {'Type':<13} "
            f"{'Score':<10} {'Grade':<8} {'Scholarship'}"
        )
        print("-" * 90)

        for student in self.students:
            score = student.calculate_final_score()
            grade = student.get_grade()

            eligibility = (
                "Yes" if student.scholarship_eligible() else "No"
            )

            print(
                f"{student.student_id:<8} "
                f"{student.name:<12} "
                f"{student.get_student_type():<13} "
                f"{score:<10.2f} "
                f"{grade:<8} "
                f"{eligibility}"
            )

        if not self.students:
            print("No student records found.")
            return

        highest = self.highest_score()
        lowest = self.lowest_score()

        print("\nCLASS SUMMARY")
        print("-" * 40)
        print(f"Total students: {len(self.students)}")
        print(f"Class average: {self.class_average():.2f}")
        print(
            f"Highest performer: {highest.name} "
            f"({highest.calculate_final_score():.2f})"
        )
        print(
            f"Lowest performer: {lowest.name} "
            f"({lowest.calculate_final_score():.2f})"
        )

        eligible_count = sum(
            student.scholarship_eligible()
            for student in self.students
        )
        print(f"Students eligible for scholarship: {eligible_count}")


# Read student information from the CSV file.
def load_students(filename):
    students = []

    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                student_type = row["student_type"].strip().lower()

                if student_type == "regular":
                    student_class = RegularStudent
                elif student_type == "scholarship":
                    student_class = ScholarshipStudent
                else:
                    raise ValueError(
                        f"Unknown student type: {student_type}"
                    )

                student = student_class(
                    row["student_id"],
                    row["name"],
                    row["assignment_mark"],
                    row["exam_mark"]
                )

                students.append(student)

    except FileNotFoundError:
        print(f"Error: Could not find {filename}.")
    except (KeyError, ValueError) as error:
        print(f"Error reading student data: {error}")

    return students


# Main program
if __name__ == "__main__":
    student_list = load_students("students.csv")

    if student_list:
        analyzer = PerformanceAnalyzer(student_list)
        analyzer.generate_report()
    else:
        print("No student records available for analysis.")