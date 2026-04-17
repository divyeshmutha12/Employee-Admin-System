"""SQLAlchemy models for the Employee Management System."""

from sqlalchemy import Column, Integer, String

try:
    from .database import Base
except ImportError:
    from database import Base


class Employee(Base):
    """Employee table mapped to a Python class."""

    # This is the table name created in SQLite.
    __tablename__ = "employees"

    # id: auto-incrementing primary key.
    id = Column(Integer, primary_key=True, index=True)
    # name: employee full name.
    name = Column(String, nullable=False)
    # role: employee role/designation.
    role = Column(String, nullable=False)
