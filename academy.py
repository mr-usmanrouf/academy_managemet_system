"""
academy.py

Academy is the central controller of the application. All CRUD operations,
cross-entity business rules (e.g. "removing a course must first remove all
enrollments"), and coordination with Storage and ReportGenerator happen
here. Entity classes (Student, Teacher, Course, Attendance, Fee) only
manage their own internal state.
"""

from datetime import date

from student import Student
from teacher import Teacher
from course import Course
from attendence import Attendance
from fee import Fee
from storage import Storage
from report_generator import ReportGenerator
from exceptions import (
    RecordNotFoundError,
    EnrollmentError,
    DuplicateRecordError,
    ValidationError,
)


class Academy:
    def __init__(self, data_dir="data", backup_dir="backup"):
        self.students = {}
        self.teachers = {}
        self.courses = {}
        self.attendance_records = {}
        self.fees = {}

        self.storage = Storage(data_dir=data_dir, backup_dir=backup_dir)
        self.reports = ReportGenerator(self)

    # ------------------------------------------------------------------
    # ID generation
    # ------------------------------------------------------------------
    @staticmethod
    def _next_id(prefix, dictionary, width=3):
        max_num = 0
        for key in dictionary:
            if key.startswith(prefix):
                suffix = key[len(prefix):]
                if suffix.isdigit():
                    max_num = max(max_num, int(suffix))
        return f"{prefix}{str(max_num + 1).zfill(width)}"

    # ==================================================================
    # STUDENT MANAGEMENT
    # ==================================================================
    def addStudent(self, name, father_name, age, phone, email, admission_date=None):
        student_id = self._next_id("STU", self.students)
        student = Student(
            student_id=student_id,
            name=name,
            father_name=father_name,
            age=age,
            phone=phone,
            email=email,
            admission_date=admission_date,
        )
        self.students[student_id] = student
        return student

    def findStudent(self, student_id):
        student = self.students.get(student_id)
        if student is None:
            raise RecordNotFoundError(f"Student '{student_id}' was not found.")
        return student

    def searchStudents(self, keyword):
        keyword = keyword.strip().lower()
        return [
            s for s in self.students.values()
            if keyword in s.student_id.lower() or keyword in s.name.lower()
        ]

    def updateStudent(self, student_id, **kwargs):
        student = self.findStudent(student_id)
        student.updateProfile(**kwargs)
        return student

    def removeStudent(self, student_id):
        student = self.findStudent(student_id)
        if student.course_id:
            course = self.courses.get(student.course_id)
            if course and student_id in course.student_ids:
                course.removeStudent(student_id)
        del self.students[student_id]

    def enrollStudent(self, student_id, course_id):
        student = self.findStudent(student_id)
        course = self.findCourse(course_id)
        student.enroll(course_id)
        course.addStudent(student_id)
        return student

    def withdrawStudent(self, student_id):
        student = self.findStudent(student_id)
        course_id = student.course_id
        student.withdraw()
        if course_id:
            course = self.courses.get(course_id)
            if course and student_id in course.student_ids:
                course.removeStudent(student_id)
        return student

    def removeStudentFromCourse(self, course_id, student_id):
        course = self.findCourse(course_id)
        student = self.findStudent(student_id)
        if student.course_id != course_id:
            raise EnrollmentError(
                f"Student {student_id} is not enrolled in course {course_id}.")
        student.withdraw()
        course.removeStudent(student_id)
        return student

    def viewAllStudents(self):
        return list(self.students.values())

    # ==================================================================
    # TEACHER MANAGEMENT
    # ==================================================================
    def addTeacher(self, name, phone, email, qualification, salary):
        teacher_id = self._next_id("TCH", self.teachers)
        teacher = Teacher(
            teacher_id=teacher_id,
            name=name,
            phone=phone,
            email=email,
            qualification=qualification,
            salary=salary,
        )
        self.teachers[teacher_id] = teacher
        return teacher

    def findTeacher(self, teacher_id):
        teacher = self.teachers.get(teacher_id)
        if teacher is None:
            raise RecordNotFoundError(f"Teacher '{teacher_id}' was not found.")
        return teacher

    def searchTeachers(self, keyword):
        keyword = keyword.strip().lower()
        return [
            t for t in self.teachers.values()
            if keyword in t.teacher_id.lower() or keyword in t.name.lower()
        ]

    def updateTeacher(self, teacher_id, **kwargs):
        teacher = self.findTeacher(teacher_id)
        teacher.updateProfile(**kwargs)
        return teacher

    def removeTeacher(self, teacher_id):
        teacher = self.findTeacher(teacher_id)
        for course_id in list(teacher.assigned_courses):
            course = self.courses.get(course_id)
            if course and course.teacher_id == teacher_id:
                course.removeTeacher()
        del self.teachers[teacher_id]

    def assignCourseToTeacher(self, teacher_id, course_id):
        teacher = self.findTeacher(teacher_id)
        course = self.findCourse(course_id)
        teacher.assignCourse(course_id)
        course.assignTeacher(teacher_id)
        return teacher

    def removeCourseFromTeacher(self, teacher_id, course_id):
        teacher = self.findTeacher(teacher_id)
        course = self.courses.get(course_id)
        teacher.removeCourse(course_id)
        if course and course.teacher_id == teacher_id:
            course.removeTeacher()
        return teacher

    def viewAllTeachers(self):
        return list(self.teachers.values())

    # ==================================================================
    # COURSE MANAGEMENT
    # ==================================================================
    def createCourse(self, course_name, duration, monthly_fee):
        course_id = self._next_id("CRS", self.courses)
        course = Course(
            course_id=course_id,
            course_name=course_name,
            duration=duration,
            monthly_fee=monthly_fee,
        )
        self.courses[course_id] = course
        return course

    def findCourse(self, course_id):
        course = self.courses.get(course_id)
        if course is None:
            raise RecordNotFoundError(f"Course '{course_id}' was not found.")
        return course

    def searchCourses(self, keyword):
        keyword = keyword.strip().lower()
        return [
            c for c in self.courses.values()
            if keyword in c.course_id.lower() or keyword in c.course_name.lower()
        ]

    def updateCourse(self, course_id, **kwargs):
        course = self.findCourse(course_id)
        course.updateDetails(**kwargs)
        return course

    def removeCourse(self, course_id):
        course = self.findCourse(course_id)
        for student_id in list(course.student_ids):
            student = self.students.get(student_id)
            if student and student.course_id == course_id:
                student.withdraw()
        if course.teacher_id:
            teacher = self.teachers.get(course.teacher_id)
            if teacher and course_id in teacher.assigned_courses:
                teacher.removeCourse(course_id)
        del self.courses[course_id]

    def viewAllCourses(self):
        return list(self.courses.values())

    # ==================================================================
    # ATTENDANCE MANAGEMENT
    # ==================================================================
    def markAttendance(self, student_id, date_str, status):
        student = self.findStudent(student_id)
        if not student.course_id:
            raise EnrollmentError(
                f"Student {student_id} is not enrolled in any course; attendance cannot be marked."
            )
        for record in self.attendance_records.values():
            if record.student_id == student_id and record.date == date_str:
                raise DuplicateRecordError(
                    f"Attendance for student {student_id} on {date_str} has already been recorded."
                )
        attendance_id = self._next_id("ATT", self.attendance_records)
        record = Attendance(attendance_id, student_id, date_str, status)
        self.attendance_records[attendance_id] = record
        self._recalculateAttendance(student_id)
        return record

    def updateAttendanceRecord(self, attendance_id, status):
        record = self.attendance_records.get(attendance_id)
        if record is None:
            raise RecordNotFoundError(
                f"Attendance record '{attendance_id}' was not found.")
        record.mark(status)
        self._recalculateAttendance(record.student_id)
        return record

    def _recalculateAttendance(self, student_id):
        student = self.students.get(student_id)
        if not student:
            return
        records = [r for r in self.attendance_records.values()
                if r.student_id == student_id]
        total = len(records)
        present = sum(1 for r in records if r.isPresent())
        student.calculateAttendance(present, total)

    def searchAttendance(self, student_id=None, date_str=None):
        results = list(self.attendance_records.values())
        if student_id:
            results = [r for r in results if r.student_id == student_id]
        if date_str:
            results = [r for r in results if r.date == date_str]
        return results

    def viewStudentAttendance(self, student_id):
        self.findStudent(student_id)  # ensures student exists
        return [r for r in self.attendance_records.values() if r.student_id == student_id]

    def viewDailyAttendance(self, date_str):
        return [r for r in self.attendance_records.values() if r.date == date_str]

    # ==================================================================
    # FEE MANAGEMENT
    # ==================================================================
    def generateMonthlyFee(self, student_id, month, amount=None):
        student = self.findStudent(student_id)
        for f in self.fees.values():
            if f.student_id == student_id and f.month == month:
                raise DuplicateRecordError(
                    f"A fee record for student {student_id} in {month} already exists."
                )
        if amount is None:
            if not student.course_id:
                raise ValidationError(
                    "Student is not enrolled in a course; an amount must be provided explicitly."
                )
            course = self.findCourse(student.course_id)
            amount = course.monthly_fee
        fee_id = self._next_id("FEE", self.fees)
        fee = Fee(fee_id, student_id, month, amount)
        self.fees[fee_id] = fee
        student.markFeePending()
        return fee

    def collectFee(self, fee_id, payment_date=None):
        fee = self.fees.get(fee_id)
        if fee is None:
            raise RecordNotFoundError(f"Fee record '{fee_id}' was not found.")
        payment_date = payment_date or date.today().isoformat()
        fee.pay(payment_date)
        student = self.students.get(fee.student_id)
        if student and not self.hasPendingFees(student.student_id):
            student.markFeePaid()
        return fee

    def hasPendingFees(self, student_id):
        return any(
            f.student_id == student_id and not f.isPaid()
            for f in self.fees.values()
        )

    def searchFeeRecord(self, student_id=None, month=None):
        results = list(self.fees.values())
        if student_id:
            results = [f for f in results if f.student_id == student_id]
        if month:
            results = [f for f in results if f.month == month]
        return results

    def viewPendingFees(self):
        return [f for f in self.fees.values() if not f.isPaid()]

    def viewFeeHistory(self, student_id):
        self.findStudent(student_id)
        return [f for f in self.fees.values() if f.student_id == student_id]

    def viewMonthlyCollection(self, month):
        return [f for f in self.fees.values() if f.month == month and f.isPaid()]

    # ==================================================================
    # PERSISTENCE
    # ==================================================================
    def save(self):
        self.storage.save("students", {sid: s.toDict()
                        for sid, s in self.students.items()})
        self.storage.save("teachers", {tid: t.toDict()
                        for tid, t in self.teachers.items()})
        self.storage.save("courses", {cid: c.toDict()
                        for cid, c in self.courses.items()})
        self.storage.save(
            "attendance",
            {aid: a.toDict() for aid, a in self.attendance_records.items()},
        )
        self.storage.save("fees", {fid: f.toDict()
                          for fid, f in self.fees.items()})

    def load(self):
        self.students = {
            sid: Student.fromDict(data) for sid, data in self.storage.load("students").items()
        }
        self.teachers = {
            tid: Teacher.fromDict(data) for tid, data in self.storage.load("teachers").items()
        }
        self.courses = {
            cid: Course.fromDict(data) for cid, data in self.storage.load("courses").items()
        }
        self.attendance_records = {
            aid: Attendance.fromDict(data)
            for aid, data in self.storage.load("attendance").items()
        }
        self.fees = {
            fid: Fee.fromDict(data) for fid, data in self.storage.load("fees").items()
        }

    def backup(self):
        self.save()
        return self.storage.backup()

    def restore(self, backup_name=None):
        restored = self.storage.restore(backup_name)
        self.load()
        return restored

    def listBackups(self):
        return self.storage.listBackups()
