# Academy Management System

A Python-based console application I built for **AL-FALAH English Academy** to simplify the management of students, teachers, courses, attendance, and fee records. The project is developed using **Object-Oriented Programming (OOP)** and stores all data in **JSON files**, so no database is required.

This project was created as part of my Python OOP practice to apply concepts like inheritance, encapsulation, abstraction, file handling, exception handling, and modular programming in a real-world application.

---

## Features

* Manage students, teachers, and courses
* Enroll and withdraw students from courses
* Assign teachers to courses
* Mark daily attendance
* Automatically calculate attendance percentage
* Generate and collect monthly fees
* View pending fee records
* Generate academy reports
* Backup and restore application data
* Automatic ID generation for all records

---

## Built With

* Python 3
* Object-Oriented Programming (OOP)
* JSON
* File Handling
* Exception Handling

No third-party libraries are required.

---

## Project Structure

```text
academy_management_system/
│
├── main.py
├── academy.py
├── person.py
├── student.py
├── teacher.py
├── course.py
├── attendance.py
├── fee.py
├── storage.py
├── report_generator.py
├── validator.py
├── exceptions.py
├── data/
├── backup/
└── README.md
```

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/mr-usmanrouf/academy_managemet_system.git
```

Move into the project folder:

```bash
cd academy_managemet_system
```

Run the program:

```bash
python3 main.py
```

---


## Future Improvements

Some features I'd like to add in the future:

* GUI version using Tkinter or PyQt
* Database support (SQLite/MySQL)
* User authentication
* Export reports as PDF
* Web-based version using Flask or Django

---

## About Me

I'm **Muhammad Usman Rouf**, a Computer Science student from Pakistan who enjoys building Python projects and learning Data Science and Artificial Intelligence.

GitHub: **https://github.com/mr-usmanrouf**

I'm always trying to improve my programming skills by building practical projects and learning new technologies.

---

## License

This project is open for learning and educational purposes. Feel free to explore the code, suggest improvements, or use it as a reference for your own projects.

---

If you find this project helpful, consider giving it a ⭐ on GitHub.
