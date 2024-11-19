from fastapi import APIRouter, HTTPException
from typing import List
from app.database import DatabaseManager
from app.models import Employee

db_manager = DatabaseManager(
    server='IN-BWF3NX3',
    database='EmployeeDatabase',
    username='sa',
    password='sa',
    driver='{ODBC Driver 17 for SQL Server}'
)

router = APIRouter()

@router.get("/employees", response_model=List[dict])
async def get_employees():
    query = "SELECT ID, Name, Salary FROM Employee"
    rows = db_manager.fetch_all(query)
    employees = [{"ID": row[0], "Name": row[1], "Salary": float(row[2])} for row in rows]
    return employees

@router.post("/employees")
async def add_employee(employee: Employee):
    name = employee.Name
    salary = employee.Salary
    if not name or not salary:
        raise HTTPException(status_code=400, detail="Name and Salary are required")
    query = "INSERT INTO Employee (Name, Salary) VALUES (?, ?)"
    db_manager.execute_query(query, (name, salary))
    return {"message": "Employee added successfully"}

@router.put("/employees/{id}")
async def update_employee(id: int, employee: Employee):
    name = employee.Name
    salary = employee.Salary
    if not name or not salary:
        raise HTTPException(status_code=400, detail="Name and Salary are required")
    query = "UPDATE Employee SET Name = ?, Salary = ? WHERE ID = ?"
    db_manager.execute_query(query, (name, salary, id))
    rows_affected = db_manager.fetch_all("SELECT * FROM Employee WHERE ID = ?", (id,))
    if not rows_affected:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated successfully"}
