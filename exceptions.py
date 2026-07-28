"""
exceptions.py

Custom exception hierarchy for the Student Management System Pro application.
Using specific exception types (rather than a generic Exception) makes error
handling in the Academy controller and the menu-driven UI more precise and
easier to maintain.
"""


class AcademyError(Exception):
    """Base class for all application-specific exceptions."""
    pass


class DuplicateIDError(AcademyError):
    """Raised when an operation would create a record with a duplicate unique ID."""
    pass


class RecordNotFoundError(AcademyError):
    """Raised when a requested record (student, teacher, course, etc.) does not exist."""
    pass


class ValidationError(AcademyError):
    """Raised when input data fails validation rules."""
    pass


class EnrollmentError(AcademyError):
    """Raised for invalid enrollment/assignment operations (e.g. double enrollment)."""
    pass


class DuplicateRecordError(AcademyError):
    """Raised when a business rule forbids a duplicate record (e.g. one fee per month)."""
    pass


class StorageError(AcademyError):
    """Raised when saving, loading, backing up, or restoring data fails."""
    pass