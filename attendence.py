"""
attendance.py

Represents a single attendance record for one student on one date.
Attendance records are stored independently of the Student class; the
Academy controller recalculates each student's attendance percentage
whenever a record is added or updated.
"""

from validator import validate_non_empty_string, validate_date, validate_attendance_status


class Attendance:
    def __init__(self, attendance_id, student_id, date, status="Present"):
        self.attendance_id = validate_non_empty_string(attendance_id, "Attendance ID")
        self.student_id = validate_non_empty_string(student_id, "Student ID")
        self.date = validate_date(date)
        self.status = validate_attendance_status(status)

    def mark(self, status):
        self.status = validate_attendance_status(status)

    def isPresent(self):
        return self.status == "Present"

    def displayDetails(self):
        lines = [
            f"Attendance ID    : {self.attendance_id}",
            f"Student ID       : {self.student_id}",
            f"Date             : {self.date}",
            f"Status           : {self.status}",
        ]
        return "\n".join(lines)

    def toDict(self):
        return {
            "attendance_id": self.attendance_id,
            "student_id": self.student_id,
            "date": self.date,
            "status": self.status,
        }

    @staticmethod
    def fromDict(data):
        return Attendance(
            attendance_id=data["attendance_id"],
            student_id=data["student_id"],
            date=data["date"],
            status=data["status"],
        )