from pydantic import BaseModel

class Employee(BaseModel):
    Name: str
    Salary: float
