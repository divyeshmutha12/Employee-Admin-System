"""Pydantic schemas for request and response validation."""

from pydantic import BaseModel, ConfigDict


class EmployeeCreate(BaseModel):
    """Data required to create a new employee."""

    name: str
    role: str


class EmployeeResponse(BaseModel):
    """Data returned to API clients for an employee."""

    id: int
    name: str
    role: str

    # Allow returning SQLAlchemy model objects directly.
    model_config = ConfigDict(from_attributes=True)
