# Employee Admin System

A clean, beginner-friendly Employee Management System backend built with FastAPI, SQLite, and SQLAlchemy.

## Project Structure

```
Employee-Admin-System/
├── backend/
│   ├── .venv/        # Virtual environment (only one, here)
│   ├── main.py       # FastAPI app and routes
│   ├── database.py   # SQLite + SQLAlchemy setup
│   ├── models.py     # SQLAlchemy Employee model
│   ├── employees.db  # SQLite database file (auto-created)
│   └── __pycache__/
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

## Setup (Windows PowerShell)

1. Create virtual environment:

```powershell
python -m venv backend/.venv
```

2. Activate virtual environment:

```powershell
.\backend\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Run FastAPI app with auto-reload:

```powershell
uvicorn backend.main:app --reload --port 8000
```

5. Open API docs:

```
http://127.0.0.1:8000/docs
```

## API Endpoints

- `GET /` - Welcome message
- `GET /employees` - Get all employees
- `POST /employees` - Create employee
- `DELETE /employees/{id}` - Delete employee

## Database

- Type: SQLite (with SQLAlchemy ORM)
- File: `backend/employees.db`
- Table: `employees`
  - `id` (primary key)
  - `name`
  - `role`
	- `created_at`

## Example Requests

Create employee:

```
POST http://127.0.0.1:8000/employees
Content-Type: application/json

{
	"name": "John Doe",
	"role": "Developer"
}
```

Get all employees:

```
GET http://127.0.0.1:8000/employees
```

Delete employee:

```
DELETE http://127.0.0.1:8000/employees/1
```