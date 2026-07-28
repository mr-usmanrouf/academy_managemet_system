"""
validator.py

Centralized input validation helpers used across the application. Keeping
validation logic in one module avoids duplicating rules inside every entity
class and menu handler, and keeps error messages consistent.
"""

import re
from datetime import datetime

from exceptions import ValidationError

EMAIL_PATTERN = re.compile(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$")
PHONE_PATTERN = re.compile(r"^\+?[0-9\-\s]{7,15}$")

VALID_ATTENDANCE_STATUSES = ("Present", "Absent", "Late")
VALID_PAYMENT_STATUSES = ("Paid", "Pending")


def validate_non_empty_string(value, field_name):
    if value is None or str(value).strip() == "":
        raise ValidationError(f"{field_name} cannot be empty.")
    return str(value).strip()


def validate_email(email):
    email = validate_non_empty_string(email, "Email")
    if not EMAIL_PATTERN.match(email):
        raise ValidationError(f"'{email}' is not a valid email address.")
    return email


def validate_phone(phone):
    phone = validate_non_empty_string(phone, "Phone")
    if not PHONE_PATTERN.match(phone):
        raise ValidationError(f"'{phone}' is not a valid phone number.")
    return phone


def validate_age(age, minimum=3, maximum=100):
    try:
        age = int(age)
    except (TypeError, ValueError):
        raise ValidationError("Age must be a whole number.")
    if age < minimum or age > maximum:
        raise ValidationError(f"Age must be between {minimum} and {maximum}.")
    return age


def validate_amount(amount, field_name="Amount"):
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValidationError(f"{field_name} must be a number.")
    if amount < 0:
        raise ValidationError(f"{field_name} cannot be negative.")
    return amount


def validate_date(date_str, field_name="Date"):
    date_str = validate_non_empty_string(date_str, field_name)
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValidationError(f"{field_name} must be in YYYY-MM-DD format.")
    return date_str


def validate_month(month_str, field_name="Month"):
    month_str = validate_non_empty_string(month_str, field_name)
    try:
        datetime.strptime(month_str, "%Y-%m")
    except ValueError:
        raise ValidationError(f"{field_name} must be in YYYY-MM format.")
    return month_str


def validate_attendance_status(status):
    status = validate_non_empty_string(status, "Attendance status")
    status = status.strip().capitalize()
    if status not in VALID_ATTENDANCE_STATUSES:
        raise ValidationError(
            f"Attendance status must be one of {VALID_ATTENDANCE_STATUSES}."
        )
    return status


def validate_duration(duration):
    return validate_non_empty_string(duration, "Duration")