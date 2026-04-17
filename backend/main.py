from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

try:
    from . import models
    from .database import Base, engine, get_db
    from .schemas import EmployeeCreate, EmployeeResponse
except ImportError:
    import models
    from database import Base, engine, get_db
    from schemas import EmployeeCreate, EmployeeResponse

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
@app.post("/employees", response_model=EmployeeResponse)
def add_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    """Add a new employee to the database."""
    # Build a new row from the request body.
    new_employee = models.Employee(name=employee.name, role=employee.role)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee


# ---------- READ ----------
@app.get("/employees", response_model=List[EmployeeResponse])
def get_all_employees(db: Session = Depends(get_db)):
    """Return all employees."""
    # Fetch every row from the employees table.
    return db.query(models.Employee).all()


# ---------- DELETE ----------
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    """Delete one employee by id."""
    # Find the employee by primary key.
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()
    return {"message": f"Employee {employee_id} deleted successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
