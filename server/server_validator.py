import re
from typing import Optional

"""
This is not a duplicate of the client's validator code.
This protects against unauthorized attempts by the user to bypass validation rules.
Email validation is planned to be migrated to pydantic's EmailStr in the future.
"""

def serv_validate_name(name: Optional[str]) -> Optional[str]:
    if name is None:
        return name
    if not name or not name.strip():
        raise ValueError("Name cannot be empty")
    if len(name.strip()) > 100:
        raise ValueError("Name must be less than 100 characters")
    return name.strip()


def serv_validate_email(email: Optional[str]) -> Optional[str]:
    if email is None:
        return email
    if not email:
        raise ValueError("Email cannot be empty")
    if "@" not in email:
        raise ValueError("Email must contain @")
    if len(email) < 5:
        raise ValueError("Email must contain at least 5 characters")
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        raise ValueError("Invalid email format (example: user@example.com)")
    return email