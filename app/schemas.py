from pydantic import BaseModel
from datetime import date


class EmployeeData(BaseModel):
    firstname: str
    lastname: str
    date_of_birth: date
    email: str
    position: str


class Employee(EmployeeData):
    id: int
