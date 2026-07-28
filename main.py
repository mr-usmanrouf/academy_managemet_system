#!/usr/bin/env python3
"""
main.py

Menu-driven console entry point for Student Management System Pro.
Loads existing data on startup and saves before exiting, per the project
requirements. All user-facing errors are custom exceptions defined in
exceptions.py; unexpected errors are still allowed to surface so bugs are
not silently hidden.
"""

from academy import Academy
from exceptions import AcademyError


def prompt(label):
    return input(f"{label}: ").strip()


def pause():
    input("\nPress Enter to continue...")


def print_header(title):
    print("\n" + "=" * 42)
    print(title)
    print("=" * 42)


# ----------------------------------------------------------------------
# STUDENT MENU
# ----------------------------------------------------------------------
def student_menu(academy):
    while True:
        print_header("STUDENT MANAGEMENT")
        print("1. Add Student")
        print("2. Search Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Enroll in Course")
        print("6. Withdraw from Course")
        print("7. Mark Fee Paid")
        print("8. View Student Details")
        print("9. View All Students")
        print("0. Back to Main Menu")
        choice = prompt("Choose an option")

        try:
            if choice == "1":
                name = prompt("Name")
                father_name = prompt("Father Name")
                age = prompt("Age")
                phone = prompt("Phone")
                email = prompt("Email")
                student = academy.addStudent(name, father_name, age, phone, email)
                print(f"\nStudent added successfully with ID: {student.student_id}")

            elif choice == "2":
                keyword = prompt("Enter Student ID or Name to search")
                results = academy.searchStudents(keyword)
                if not results:
                    print("No matching students found.")
                for s in results:
                    print("\n" + s.displayDetails())

            elif choice == "3":
                sid = prompt("Student ID to update")
                print("Leave any field blank to keep its current value.")
                name = prompt("New Name") or None
                father_name = prompt("New Father Name") or None
                age = prompt("New Age") or None
                phone = prompt("New Phone") or None
                email = prompt("New Email") or None
                academy.updateStudent(
                    sid, name=name, father_name=father_name, age=age, phone=phone, email=email
                )
                print("Student updated successfully.")

            elif choice == "4":
                sid = prompt("Student ID to delete")
                confirm = prompt(f"Type YES to confirm deleting {sid}")
                if confirm.upper() == "YES":
                    academy.removeStudent(sid)
                    print("Student deleted successfully.")
                else:
                    print("Deletion cancelled.")

            elif choice == "5":
                sid = prompt("Student ID")
                cid = prompt("Course ID")
                academy.enrollStudent(sid, cid)
                print("Student enrolled successfully.")

            elif choice == "6":
                sid = prompt("Student ID")
                academy.withdrawStudent(sid)
                print("Student withdrawn successfully.")

            elif choice == "7":
                sid = prompt("Student ID")
                academy.findStudent(sid)
                pending = [f for f in academy.viewFeeHistory(sid) if not f.isPaid()]
                if not pending:
                    print("This student has no pending fees.")
                elif len(pending) == 1:
                    fee = pending[0]
                    academy.collectFee(fee.fee_id)
                    print(f"Fee {fee.fee_id} for {fee.month} marked as paid.")
                else:
                    print("Pending fees:")
                    for i, f in enumerate(pending, start=1):
                        print(f"  {i}. {f.fee_id}  {f.month}  Rs.{f.amount}")
                    idx = prompt("Select fee number to mark as paid")
                    try:
                        fee = pending[int(idx) - 1]
                        academy.collectFee(fee.fee_id)
                        print(f"Fee {fee.fee_id} for {fee.month} marked as paid.")
                    except (ValueError, IndexError):
                        print("Invalid selection.")

            elif choice == "8":
                sid = prompt("Student ID")
                print("\n" + academy.findStudent(sid).displayDetails())

            elif choice == "9":
                students = academy.viewAllStudents()
                if not students:
                    print("No students registered.")
                for s in students:
                    print("\n" + s.displayDetails())

            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except AcademyError as exc:
            print(f"\nError: {exc}")
        pause()


# ----------------------------------------------------------------------
# TEACHER MENU
# ----------------------------------------------------------------------
def teacher_menu(academy):
    while True:
        print_header("TEACHER MANAGEMENT")
        print("1. Add Teacher")
        print("2. Search Teacher")
        print("3. Update Teacher")
        print("4. Delete Teacher")
        print("5. Assign Course")
        print("6. Remove Course")
        print("7. View Teacher Details")
        print("8. View All Teachers")
        print("0. Back to Main Menu")
        choice = prompt("Choose an option")

        try:
            if choice == "1":
                name = prompt("Name")
                phone = prompt("Phone")
                email = prompt("Email")
                qualification = prompt("Qualification")
                salary = prompt("Salary")
                teacher = academy.addTeacher(name, phone, email, qualification, salary)
                print(f"\nTeacher added successfully with ID: {teacher.teacher_id}")

            elif choice == "2":
                keyword = prompt("Enter Teacher ID or Name to search")
                results = academy.searchTeachers(keyword)
                if not results:
                    print("No matching teachers found.")
                for t in results:
                    print("\n" + t.displayDetails())

            elif choice == "3":
                tid = prompt("Teacher ID to update")
                print("Leave any field blank to keep its current value.")
                name = prompt("New Name") or None
                phone = prompt("New Phone") or None
                email = prompt("New Email") or None
                qualification = prompt("New Qualification") or None
                salary = prompt("New Salary") or None
                academy.updateTeacher(
                    tid, name=name, phone=phone, email=email,
                    qualification=qualification, salary=salary
                )
                print("Teacher updated successfully.")

            elif choice == "4":
                tid = prompt("Teacher ID to delete")
                confirm = prompt(f"Type YES to confirm deleting {tid}")
                if confirm.upper() == "YES":
                    academy.removeTeacher(tid)
                    print("Teacher deleted successfully.")
                else:
                    print("Deletion cancelled.")

            elif choice == "5":
                tid = prompt("Teacher ID")
                cid = prompt("Course ID")
                academy.assignCourseToTeacher(tid, cid)
                print("Course assigned successfully.")

            elif choice == "6":
                tid = prompt("Teacher ID")
                cid = prompt("Course ID")
                academy.removeCourseFromTeacher(tid, cid)
                print("Course removed successfully.")

            elif choice == "7":
                tid = prompt("Teacher ID")
                print("\n" + academy.findTeacher(tid).displayDetails())

            elif choice == "8":
                teachers = academy.viewAllTeachers()
                if not teachers:
                    print("No teachers registered.")
                for t in teachers:
                    print("\n" + t.displayDetails())

            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except AcademyError as exc:
            print(f"\nError: {exc}")
        pause()


# ----------------------------------------------------------------------
# COURSE MENU
# ----------------------------------------------------------------------
def course_menu(academy):
    while True:
        print_header("COURSE MANAGEMENT")
        print("1. Create Course")
        print("2. Search Course")
        print("3. Update Course")
        print("4. Delete Course")
        print("5. Assign Teacher")
        print("6. Enroll Student")
        print("7. Remove Student")
        print("8. View Course Details")
        print("9. View All Courses")
        print("0. Back to Main Menu")
        choice = prompt("Choose an option")

        try:
            if choice == "1":
                name = prompt("Course Name")
                duration = prompt("Duration")
                fee = prompt("Monthly Fee")
                course = academy.createCourse(name, duration, fee)
                print(f"\nCourse created successfully with ID: {course.course_id}")

            elif choice == "2":
                keyword = prompt("Enter Course ID or Name to search")
                results = academy.searchCourses(keyword)
                if not results:
                    print("No matching courses found.")
                for c in results:
                    print("\n" + c.displayDetails())

            elif choice == "3":
                cid = prompt("Course ID to update")
                print("Leave any field blank to keep its current value.")
                name = prompt("New Course Name") or None
                duration = prompt("New Duration") or None
                fee = prompt("New Monthly Fee") or None
                academy.updateCourse(cid, course_name=name, duration=duration, monthly_fee=fee)
                print("Course updated successfully.")

            elif choice == "4":
                cid = prompt("Course ID to delete")
                confirm = prompt(f"Type YES to confirm deleting {cid}")
                if confirm.upper() == "YES":
                    academy.removeCourse(cid)
                    print("Course deleted successfully.")
                else:
                    print("Deletion cancelled.")

            elif choice == "5":
                cid = prompt("Course ID")
                tid = prompt("Teacher ID")
                academy.assignCourseToTeacher(tid, cid)
                print("Teacher assigned successfully.")

            elif choice == "6":
                cid = prompt("Course ID")
                sid = prompt("Student ID")
                academy.enrollStudent(sid, cid)
                print("Student enrolled successfully.")

            elif choice == "7":
                cid = prompt("Course ID")
                sid = prompt("Student ID")
                academy.removeStudentFromCourse(cid, sid)
                print("Student removed from course successfully.")

            elif choice == "8":
                cid = prompt("Course ID")
                print("\n" + academy.findCourse(cid).displayDetails())

            elif choice == "9":
                courses = academy.viewAllCourses()
                if not courses:
                    print("No courses available.")
                for c in courses:
                    print("\n" + c.displayDetails())

            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except AcademyError as exc:
            print(f"\nError: {exc}")
        pause()


# ----------------------------------------------------------------------
# ATTENDANCE MENU
# ----------------------------------------------------------------------
def attendance_menu(academy):
    while True:
        print_header("ATTENDANCE MANAGEMENT")
        print("1. Mark Attendance")
        print("2. Search Attendance")
        print("3. View Student Attendance")
        print("4. View Daily Attendance")
        print("5. Update Attendance Record")
        print("0. Back to Main Menu")
        choice = prompt("Choose an option")

        try:
            if choice == "1":
                sid = prompt("Student ID")
                date_str = prompt("Date (YYYY-MM-DD)")
                status = prompt("Status (Present/Absent/Late)")
                record = academy.markAttendance(sid, date_str, status)
                print(f"\nAttendance marked successfully with ID: {record.attendance_id}")

            elif choice == "2":
                sid = prompt("Student ID (leave blank for all)") or None
                date_str = prompt("Date YYYY-MM-DD (leave blank for all)") or None
                results = academy.searchAttendance(student_id=sid, date_str=date_str)
                if not results:
                    print("No matching attendance records found.")
                for r in results:
                    print("\n" + r.displayDetails())

            elif choice == "3":
                sid = prompt("Student ID")
                results = academy.viewStudentAttendance(sid)
                if not results:
                    print("No attendance records for this student.")
                for r in results:
                    print("\n" + r.displayDetails())

            elif choice == "4":
                date_str = prompt("Date (YYYY-MM-DD)")
                results = academy.viewDailyAttendance(date_str)
                if not results:
                    print("No attendance records for this date.")
                for r in results:
                    print("\n" + r.displayDetails())

            elif choice == "5":
                aid = prompt("Attendance ID")
                status = prompt("New Status (Present/Absent/Late)")
                academy.updateAttendanceRecord(aid, status)
                print("Attendance record updated successfully.")

            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except AcademyError as exc:
            print(f"\nError: {exc}")
        pause()


# ----------------------------------------------------------------------
# FEE MENU
# ----------------------------------------------------------------------
def fee_menu(academy):
    while True:
        print_header("FEE MANAGEMENT")
        print("1. Generate Monthly Fee")
        print("2. Collect Fee")
        print("3. Search Fee Record")
        print("4. View Pending Fees")
        print("5. View Fee History")
        print("6. View Monthly Collection")
        print("0. Back to Main Menu")
        choice = prompt("Choose an option")

        try:
            if choice == "1":
                sid = prompt("Student ID")
                month = prompt("Month (YYYY-MM)")
                amount = prompt("Amount (leave blank to use the course's monthly fee)") or None
                fee = academy.generateMonthlyFee(sid, month, amount)
                print(f"\nFee record generated with ID: {fee.fee_id} (Amount: {fee.amount})")

            elif choice == "2":
                fid = prompt("Fee ID")
                payment_date = prompt("Payment Date YYYY-MM-DD (leave blank for today)") or None
                fee = academy.collectFee(fid, payment_date)
                print(f"Fee {fee.fee_id} collected successfully on {fee.payment_date}.")

            elif choice == "3":
                sid = prompt("Student ID (leave blank for all)") or None
                month = prompt("Month YYYY-MM (leave blank for all)") or None
                results = academy.searchFeeRecord(student_id=sid, month=month)
                if not results:
                    print("No matching fee records found.")
                for f in results:
                    print("\n" + f.displayDetails())

            elif choice == "4":
                results = academy.viewPendingFees()
                if not results:
                    print("No pending fees.")
                for f in results:
                    print("\n" + f.displayDetails())

            elif choice == "5":
                sid = prompt("Student ID")
                results = academy.viewFeeHistory(sid)
                if not results:
                    print("No fee history for this student.")
                for f in results:
                    print("\n" + f.displayDetails())

            elif choice == "6":
                month = prompt("Month (YYYY-MM)")
                results = academy.viewMonthlyCollection(month)
                total = sum(f.amount for f in results)
                print(f"\n{len(results)} payment(s) collected in {month}. Total: Rs.{total:,.2f}")
                for f in results:
                    print("\n" + f.displayDetails())

            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except AcademyError as exc:
            print(f"\nError: {exc}")
        pause()


# ----------------------------------------------------------------------
# REPORTS MENU
# ----------------------------------------------------------------------
def reports_menu(academy):
    while True:
        print_header("REPORTS")
        print("1. Student Report")
        print("2. Teacher Report")
        print("3. Course Report")
        print("4. Attendance Report")
        print("5. Fee Report")
        print("6. Monthly Income Report")
        print("7. Academy Summary Report")
        print("0. Back to Main Menu")
        choice = prompt("Choose an option")

        try:
            if choice == "1":
                sid = prompt("Student ID (leave blank for all)") or None
                print("\n" + academy.reports.studentReport(sid))
            elif choice == "2":
                tid = prompt("Teacher ID (leave blank for all)") or None
                print("\n" + academy.reports.teacherReport(tid))
            elif choice == "3":
                cid = prompt("Course ID (leave blank for all)") or None
                print("\n" + academy.reports.courseReport(cid))
            elif choice == "4":
                sid = prompt("Student ID (leave blank for all)") or None
                start = prompt("Start Date YYYY-MM-DD (leave blank)") or None
                end = prompt("End Date YYYY-MM-DD (leave blank)") or None
                print("\n" + academy.reports.attendanceReport(sid, start, end))
            elif choice == "5":
                print("\n" + academy.reports.feeReport())
            elif choice == "6":
                month = prompt("Month YYYY-MM (leave blank for all)") or None
                print("\n" + academy.reports.incomeReport(month))
            elif choice == "7":
                print("\n" + academy.reports.academySummary())
            elif choice == "0":
                break
            else:
                print("Invalid option.")
        except AcademyError as exc:
            print(f"\nError: {exc}")
        pause()


# ----------------------------------------------------------------------
# BACKUP / RESTORE
# ----------------------------------------------------------------------
def handle_backup(academy):
    try:
        target = academy.backup()
        print(f"\nBackup created successfully at: {target}")
    except AcademyError as exc:
        print(f"\nError: {exc}")
    pause()


def handle_restore(academy):
    try:
        backups = academy.listBackups()
        if not backups:
            print("\nNo backups available to restore.")
            pause()
            return
        print("\nAvailable backups (View Backup Status):")
        for i, b in enumerate(backups, start=1):
            print(f"  {i}. {b}")
        choice = prompt("Enter backup number to restore (leave blank for most recent)")
        backup_name = None
        if choice:
            try:
                index = int(choice) - 1
                backup_name = backups[index]
            except (ValueError, IndexError):
                print("Invalid selection.")
                pause()
                return
        restored = academy.restore(backup_name)
        print(f"\nData restored successfully from: {restored}")
    except AcademyError as exc:
        print(f"\nError: {exc}")
    pause()


# ----------------------------------------------------------------------
# MAIN MENU
# ----------------------------------------------------------------------
def main_menu(academy):
    while True:
        print_header("AL-FALAH ENGLISH ACADEMY")
        print("1. Student Management")
        print("2. Teacher Management")
        print("3. Course Management")
        print("4. Fee Management")
        print("5. Attendance Management")
        print("6. Reports")
        print("7. Backup Data")
        print("8. Restore Data")
        print("9. Exit")
        choice = prompt("Choose an option")

        if choice == "1":
            student_menu(academy)
        elif choice == "2":
            teacher_menu(academy)
        elif choice == "3":
            course_menu(academy)
        elif choice == "4":
            fee_menu(academy)
        elif choice == "5":
            attendance_menu(academy)
        elif choice == "6":
            reports_menu(academy)
        elif choice == "7":
            handle_backup(academy)
        elif choice == "8":
            handle_restore(academy)
        elif choice == "9":
            academy.save()
            print("\nData saved. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


def main():
    academy = Academy()
    academy.load()
    print("Welcome to Student Management System Pro")
    has_data = bool(academy.students or academy.teachers or academy.courses)
    print("Existing data loaded successfully." if has_data else "Starting with a fresh database.")
    try:
        main_menu(academy)
    except KeyboardInterrupt:
        print("\n\nInterrupted. Saving data before exit...")
        academy.save()
        print("Data saved. Goodbye!")


if __name__ == "__main__":
    main()