"""
course.py

Represents a single course offered by the academy. A course has at most
one assigned teacher at any time, but may have many enrolled students.
"""

from validator import validate_non_empty_string, validate_amount, validate_duration
from exceptions import EnrollmentError


class Course:
    def __init__(
        self,
        course_id,
        course_name,
        duration,
        monthly_fee,
        teacher_id=None,
        student_ids=None,
    ):
        self.course_id = validate_non_empty_string(course_id, "Course ID")
        self.course_name = validate_non_empty_string(course_name, "Course Name")
        self.duration = validate_duration(duration)
        self.monthly_fee = validate_amount(monthly_fee, "Monthly Fee")
        self.teacher_id = teacher_id
        self.student_ids = list(student_ids) if student_ids else []

    def updateDetails(self, course_name=None, duration=None, monthly_fee=None):
        if course_name is not None:
            self.course_name = validate_non_empty_string(course_name, "Course Name")
        if duration is not None:
            self.duration = validate_duration(duration)
        if monthly_fee is not None:
            self.monthly_fee = validate_amount(monthly_fee, "Monthly Fee")

    def assignTeacher(self, teacher_id):
        self.teacher_id = teacher_id

    def removeTeacher(self):
        self.teacher_id = None

    def addStudent(self, student_id):
        if student_id in self.student_ids:
            raise EnrollmentError(f"Student {student_id} is already enrolled in {self.course_id}.")
        self.student_ids.append(student_id)

    def removeStudent(self, student_id):
        if student_id not in self.student_ids:
            raise EnrollmentError(f"Student {student_id} is not enrolled in {self.course_id}.")
        self.student_ids.remove(student_id)

    def studentCount(self):
        return len(self.student_ids)

    def displayDetails(self):
        students = ", ".join(self.student_ids) if self.student_ids else "-"
        lines = [
            f"Course ID        : {self.course_id}",
            f"Course Name      : {self.course_name}",
            f"Duration         : {self.duration}",
            f"Monthly Fee      : {self.monthly_fee}",
            f"Teacher ID       : {self.teacher_id or '-'}",
            f"Enrolled Students: {students} ({self.studentCount()} total)",
        ]
        return "\n".join(lines)

    def toDict(self):
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "duration": self.duration,
            "monthly_fee": self.monthly_fee,
            "teacher_id": self.teacher_id,
            "student_ids": self.student_ids,
        }

    @staticmethod
    def fromDict(data):
        return Course(
            course_id=data["course_id"],
            course_name=data["course_name"],
            duration=data["duration"],
            monthly_fee=data["monthly_fee"],
            teacher_id=data.get("teacher_id"),
            student_ids=data.get("student_ids", []),
        )