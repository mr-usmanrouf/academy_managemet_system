"""
student.py

Represents a single student enrolled at the academy. Inherits shared
personal fields (name, phone, email) from Person and adds student-specific
enrollment, attendance, and fee information.
"""

from datetime import date

from person import Person
from validator import (
    validate_non_empty_string,
    validate_age,
    validate_phone,
    validate_email,
)
from exceptions import EnrollmentError


class Student(Person):
    def __init__(
        self,
        student_id,
        name,
        father_name,
        age,
        phone,
        email,
        course_id=None,
        admission_date=None,
        attendance_percentage=0.0,
        fee_status="Pending",
    ):
        super().__init__(name, phone, email)
        self.student_id = validate_non_empty_string(student_id, "Student ID")
        self.father_name = validate_non_empty_string(father_name, "Father Name")
        self.age = validate_age(age)
        self.course_id = course_id
        self.admission_date = admission_date or date.today().isoformat()
        self.attendance_percentage = float(attendance_percentage)
        self.fee_status = fee_status

    # ---- profile ----
    def updateProfile(self, name=None, father_name=None, age=None, phone=None, email=None):
        if name is not None:
            self.name = validate_non_empty_string(name, "Name")
        if father_name is not None:
            self.father_name = validate_non_empty_string(father_name, "Father Name")
        if age is not None:
            self.age = validate_age(age)
        if phone is not None:
            self.phone = validate_phone(phone)
        if email is not None:
            self.email = validate_email(email)

    # ---- enrollment ----
    def enroll(self, course_id):
        if self.course_id is not None:
            raise EnrollmentError(
                f"Student {self.student_id} is already enrolled in {self.course_id}. "
                "Withdraw first before enrolling in a new course."
            )
        self.course_id = course_id

    def withdraw(self):
        if self.course_id is None:
            raise EnrollmentError(f"Student {self.student_id} is not enrolled in any course.")
        self.course_id = None

    # ---- attendance ----
    def calculateAttendance(self, present_count, total_count):
        if total_count <= 0:
            self.attendance_percentage = 0.0
        else:
            self.attendance_percentage = round((present_count / total_count) * 100, 2)
        return self.attendance_percentage

    # ---- fees ----
    def markFeePaid(self):
        self.fee_status = "Paid"

    def markFeePending(self):
        self.fee_status = "Pending"

    # ---- display / serialization ----
    def displayDetails(self):
        lines = [
            f"Student ID       : {self.student_id}",
            f"Name             : {self.name}",
            f"Father Name      : {self.father_name}",
            f"Age              : {self.age}",
            f"Phone            : {self.phone}",
            f"Email            : {self.email}",
            f"Course ID        : {self.course_id or '-'}",
            f"Admission Date   : {self.admission_date}",
            f"Attendance %     : {self.attendance_percentage}%",
            f"Fee Status       : {self.fee_status}",
        ]
        return "\n".join(lines)

    def toDict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "father_name": self.father_name,
            "age": self.age,
            "phone": self.phone,
            "email": self.email,
            "course_id": self.course_id,
            "admission_date": self.admission_date,
            "attendance_percentage": self.attendance_percentage,
            "fee_status": self.fee_status,
        }

    @staticmethod
    def fromDict(data):
        return Student(
            student_id=data["student_id"],
            name=data["name"],
            father_name=data["father_name"],
            age=data["age"],
            phone=data["phone"],
            email=data["email"],
            course_id=data.get("course_id"),
            admission_date=data.get("admission_date"),
            attendance_percentage=data.get("attendance_percentage", 0.0),
            fee_status=data.get("fee_status", "Pending"),
        )