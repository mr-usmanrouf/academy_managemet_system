"""
teacher.py

Represents a single teacher employed by the academy. Inherits shared
personal fields from Person and adds qualification, salary, and the list
of assigned course IDs.
"""

from person import Person
from validator import (
    validate_non_empty_string,
    validate_amount,
    validate_phone,
    validate_email,
)
from exceptions import EnrollmentError


class Teacher(Person):
    def __init__(
        self,
        teacher_id,
        name,
        phone,
        email,
        qualification,
        salary,
        assigned_courses=None,
    ):
        super().__init__(name, phone, email)
        self.teacher_id = validate_non_empty_string(teacher_id, "Teacher ID")
        self.qualification = validate_non_empty_string(qualification, "Qualification")
        self.salary = validate_amount(salary, "Salary")
        self.assigned_courses = list(assigned_courses) if assigned_courses else []

    def updateProfile(self, name=None, phone=None, email=None, qualification=None, salary=None):
        if name is not None:
            self.name = validate_non_empty_string(name, "Name")
        if phone is not None:
            self.phone = validate_phone(phone)
        if email is not None:
            self.email = validate_email(email)
        if qualification is not None:
            self.qualification = validate_non_empty_string(qualification, "Qualification")
        if salary is not None:
            self.salary = validate_amount(salary, "Salary")

    def assignCourse(self, course_id):
        if course_id in self.assigned_courses:
            raise EnrollmentError(f"Teacher {self.teacher_id} is already assigned to {course_id}.")
        self.assigned_courses.append(course_id)

    def removeCourse(self, course_id):
        if course_id not in self.assigned_courses:
            raise EnrollmentError(f"Teacher {self.teacher_id} is not assigned to {course_id}.")
        self.assigned_courses.remove(course_id)

    def displayDetails(self):
        courses = ", ".join(self.assigned_courses) if self.assigned_courses else "-"
        lines = [
            f"Teacher ID       : {self.teacher_id}",
            f"Name             : {self.name}",
            f"Phone            : {self.phone}",
            f"Email            : {self.email}",
            f"Qualification    : {self.qualification}",
            f"Salary           : {self.salary}",
            f"Assigned Courses : {courses}",
        ]
        return "\n".join(lines)

    def toDict(self):
        return {
            "teacher_id": self.teacher_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "qualification": self.qualification,
            "salary": self.salary,
            "assigned_courses": self.assigned_courses,
        }

    @staticmethod
    def fromDict(data):
        return Teacher(
            teacher_id=data["teacher_id"],
            name=data["name"],
            phone=data["phone"],
            email=data["email"],
            qualification=data["qualification"],
            salary=data["salary"],
            assigned_courses=data.get("assigned_courses", []),
        )