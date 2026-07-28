"""
fee.py

Represents one monthly fee record for a student.
"""

from validator import validate_non_empty_string, validate_amount, validate_month, validate_date
from exceptions import ValidationError


class Fee:
    def __init__(self, fee_id, student_id, month, amount, payment_status="Pending", payment_date=None):
        self.fee_id = validate_non_empty_string(fee_id, "Fee ID")
        self.student_id = validate_non_empty_string(student_id, "Student ID")
        self.month = validate_month(month)
        self.amount = validate_amount(amount, "Amount")
        self.payment_status = payment_status
        self.payment_date = payment_date

    def pay(self, payment_date):
        if self.payment_status == "Paid":
            raise ValidationError(f"Fee {self.fee_id} has already been paid and cannot be paid again.")
        self.payment_date = validate_date(payment_date, "Payment Date")
        self.payment_status = "Paid"

    def isPaid(self):
        return self.payment_status == "Paid"

    def displayDetails(self):
        lines = [
            f"Fee ID           : {self.fee_id}",
            f"Student ID       : {self.student_id}",
            f"Month            : {self.month}",
            f"Amount           : {self.amount}",
            f"Payment Status   : {self.payment_status}",
            f"Payment Date     : {self.payment_date or '-'}",
        ]
        return "\n".join(lines)

    def toDict(self):
        return {
            "fee_id": self.fee_id,
            "student_id": self.student_id,
            "month": self.month,
            "amount": self.amount,
            "payment_status": self.payment_status,
            "payment_date": self.payment_date,
        }

    @staticmethod
    def fromDict(data):
        return Fee(
            fee_id=data["fee_id"],
            student_id=data["student_id"],
            month=data["month"],
            amount=data["amount"],
            payment_status=data.get("payment_status", "Pending"),
            payment_date=data.get("payment_date"),
        )