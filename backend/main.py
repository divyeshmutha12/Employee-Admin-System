import logging
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

try:
    from . import models
    from .database import Base, engine, get_db
    from .schemas import EmployeeCreate, EmployeeResponse
except ImportError:
    import models
    from database import Base, engine, get_db
    from schemas import EmployeeCreate, EmployeeResponse

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
# Logs appear in the terminal where uvicorn is running.
# Levels: DEBUG < INFO < WARNING < ERROR < CRITICAL
# Change level to logging.DEBUG to see even more detail.
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Common beginner mistakes that cause 422 / 500 errors:
#   1. Sending wrong Content-Type — must be "application/json" for POST/PUT.
#   2. Missing required fields in the request body (name or role).
#   3. Sending employee_id as a string ("/employees/abc") — must be an int.
#   4. Calling a DELETE without the ID ("/employees" instead of "/employees/1").
#   5. Forgetting to activate the virtual environment before running uvicorn.
# ---------------------------------------------------------------------------

# Create tables on startup if they don't exist yet.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Management System")

# Allow local frontend origins so any local dev port works.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Health/welcome endpoint."""
    return {"message": "Welcome to the Employee Management System"}


# ---------- CREATE ----------
@app.post("/employees", response_model=EmployeeResponse, status_code=201)
def add_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Add a new employee to the database.

    Common mistake: sending an empty string for name or role.
    FastAPI will reject them automatically if you add validation to schemas.
    """
    # Reject blank strings before they reach the database.
    if not employee.name.strip():
        logger.warning("add_employee called with empty name")
        raise HTTPException(status_code=422, detail="name must not be blank")
    if not employee.role.strip():
        logger.warning("add_employee called with empty role")
        raise HTTPException(status_code=422, detail="role must not be blank")

    logger.info("Creating employee: name=%s role=%s", employee.name, employee.role)

    try:
        new_employee = models.Employee(name=employee.name.strip(), role=employee.role.strip())
        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)
        logger.info("Employee created with id=%s", new_employee.id)
        return new_employee
    except SQLAlchemyError as exc:
        db.rollback()
        logger.error("Database error while creating employee: %s", exc)
        raise HTTPException(status_code=500, detail="Could not create employee") from exc


# ---------- READ ----------
@app.get("/employees", response_model=List[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)):
    """Return all employees."""
    logger.info("Fetching all employees")

    try:
        employees = db.query(models.Employee).all()
        logger.info("Found %s employee(s)", len(employees))
        return employees
    except SQLAlchemyError as exc:
        logger.error("Database error while fetching employees: %s", exc)
        raise HTTPException(status_code=500, detail="Could not fetch employees") from exc


# ---------- DELETE ----------
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Delete one employee by id.

    Common mistake: passing a non-integer id such as /employees/abc.
    FastAPI returns 422 automatically for that.
    """
    logger.info("Deleting employee id=%s", employee_id)

    try:
        employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

        if not employee:
            logger.warning("Employee id=%s not found", employee_id)
            raise HTTPException(status_code=404, detail="Employee not found")

        db.delete(employee)
        db.commit()
        logger.info("Employee id=%s deleted", employee_id)
        return {"message": f"Employee {employee_id} deleted successfully"}
    except HTTPException:
        # Re-raise HTTPExceptions so FastAPI handles them correctly.
        raise
    except SQLAlchemyError as exc:
        db.rollback()
        logger.error("Database error while deleting employee id=%s: %s", employee_id, exc)
        raise HTTPException(status_code=500, detail="Could not delete employee") from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
