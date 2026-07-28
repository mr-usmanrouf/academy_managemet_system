"""
report_generator.py

Generates read-only summary reports from Academy data. This module never
mutates any records; it only reads from the Academy's in-memory
dictionaries and formats the results.
"""


class ReportGenerator:
    def __init__(self, academy):
        self.academy = academy

    # ------------------------------------------------------------------
    def studentReport(self, student_id=None):
        academy = self.academy
        if student_id:
            student = academy.findStudent(student_id)
            return student.displayDetails()

        lines = ["=" * 60, "STUDENT REPORT - ALL STUDENTS", "=" * 60]
        if not academy.students:
            lines.append("No students registered.")
        for student in academy.students.values():
            lines.append(student.displayDetails())
            lines.append("-" * 60)
        return "\n".join(lines)

    # ------------------------------------------------------------------
    def teacherReport(self, teacher_id=None):
        academy = self.academy
        if teacher_id:
            teacher = academy.findTeacher(teacher_id)
            return teacher.displayDetails()

        lines = ["=" * 60, "TEACHER REPORT - ALL TEACHERS", "=" * 60]
        if not academy.teachers:
            lines.append("No teachers registered.")
        for teacher in academy.teachers.values():
            lines.append(teacher.displayDetails())
            lines.append("-" * 60)
        return "\n".join(lines)

    # ------------------------------------------------------------------
    def courseReport(self, course_id=None):
        academy = self.academy
        if course_id:
            course = academy.findCourse(course_id)
            return course.displayDetails()

        lines = ["=" * 60, "COURSE REPORT - ALL COURSES", "=" * 60]
        if not academy.courses:
            lines.append("No courses available.")
        for course in academy.courses.values():
            lines.append(course.displayDetails())
            lines.append("-" * 60)
        return "\n".join(lines)

    # ------------------------------------------------------------------
    def attendanceReport(self, student_id=None, start_date=None, end_date=None):
        academy = self.academy
        records = list(academy.attendance_records.values())
        if student_id:
            records = [r for r in records if r.student_id == student_id]
        if start_date:
            records = [r for r in records if r.date >= start_date]
        if end_date:
            records = [r for r in records if r.date <= end_date]

        lines = ["=" * 60, "ATTENDANCE REPORT", "=" * 60]
        if not records:
            lines.append("No attendance records found for the given criteria.")
        for record in sorted(records, key=lambda r: (r.student_id, r.date)):
            lines.append(f"{record.date}  {record.student_id:<10} {record.status}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    def feeReport(self):
        academy = self.academy
        paid = [f for f in academy.fees.values() if f.isPaid()]
        pending = [f for f in academy.fees.values() if not f.isPaid()]

        lines = ["=" * 60, "FEE REPORT", "=" * 60]
        lines.append(f"Total Fee Records : {len(academy.fees)}")
        lines.append(f"Paid              : {len(paid)}")
        lines.append(f"Pending           : {len(pending)}")
        lines.append("-" * 60)
        lines.append("PENDING FEES:")
        if not pending:
            lines.append("  None")
        for fee in pending:
            lines.append(f"  {fee.fee_id}  {fee.student_id}  {fee.month}  Rs.{fee.amount}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    def incomeReport(self, month=None):
        academy = self.academy
        collected = [f for f in academy.fees.values() if f.isPaid()]
        if month:
            collected = [f for f in collected if f.month == month]
        total = sum(f.amount for f in collected)

        title = "MONTHLY INCOME REPORT" + (f" - {month}" if month else "")
        lines = ["=" * 60, title, "=" * 60]
        lines.append(f"Total Payments Collected : {len(collected)}")
        lines.append(f"Total Income             : Rs.{total:,.2f}")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    def academySummary(self):
        academy = self.academy
        total_students = len(academy.students)
        total_teachers = len(academy.teachers)
        total_courses = len(academy.courses)
        total_income = sum(f.amount for f in academy.fees.values() if f.isPaid())
        pending_income = sum(f.amount for f in academy.fees.values() if not f.isPaid())
        avg_attendance = (
            sum(s.attendance_percentage for s in academy.students.values()) / total_students
            if total_students else 0.0
        )

        lines = ["=" * 60, "ACADEMY SUMMARY REPORT", "=" * 60]
        lines.append(f"Total Students        : {total_students}")
        lines.append(f"Total Teachers        : {total_teachers}")
        lines.append(f"Total Courses         : {total_courses}")
        lines.append(f"Total Income Collected: Rs.{total_income:,.2f}")
        lines.append(f"Pending Fee Amount    : Rs.{pending_income:,.2f}")
        lines.append(f"Average Attendance %  : {avg_attendance:.2f}%")
        return "\n".join(lines)