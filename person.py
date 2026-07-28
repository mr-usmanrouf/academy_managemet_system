"""
person.py

Abstract base class shared by Student and Teacher. Demonstrates inheritance
and abstraction: both subclasses need a name, phone, and email, and both
must implement displayDetails/toDict/fromDict, but Person itself is never
instantiated directly.
"""

from abc import ABC, abstractmethod

from validator import validate_non_empty_string, validate_email, validate_phone


class Person(ABC):
    def __init__(self, name, phone, email):
        self.name = validate_non_empty_string(name, "Name")
        self.phone = validate_phone(phone)
        self.email = validate_email(email)

    @abstractmethod
    def displayDetails(self):
        """Return a human-readable multi-line summary of the person."""
        raise NotImplementedError

    @abstractmethod
    def toDict(self):
        """Return a JSON-serializable dict representation."""
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def fromDict(data):
        """Reconstruct an instance from a dict produced by toDict()."""
        raise NotImplementedError