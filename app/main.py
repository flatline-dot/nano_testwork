from typing import List
from app import schemas

from fastapi import FastAPI, HTTPException
from .db import database
from .db import employees


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



@app.get('/employee/{employee_id}', response_model=schemas.Employee, responses={404: {"message": 'Employee not found'}})
async def get_employee(employee_id: int):
    query = employees.select().where(employees.c.id == employee_id)
    employee =  await database.fetch_one(query)
    if employee:
        return employee

    raise HTTPException(status_code=404, detail='Employee not found')

    
@app.get('/employees/', response_model=List[schemas.Employee], responses={404: {"message": 'Employees not found'}})
async def get_employees(skip: int = 0, limit: int = 10):
    query = employees.select()
    employees_list =  await database.fetch_all(query)
    if employees_list:
        return employees_list[skip:skip + limit]

    raise HTTPException(status_code=404, detail='Employees not found')



@app.post('/employee/', response_model=schemas.Employee, responses={400: {"message": 'Email yet using'}})
async def create_employee(employee_data: schemas.EmployeeData):
    employee_data = employee_data.dict()
    query = employees.insert().values(**employee_data)
    try:
        employee_id = await database.execute(query)
        return {**employee_data.dict(), 'id': employee_id}
    except:
        raise HTTPException(status_code=400, detail='Email yet using')


@app.put('/employee/{employee_id}', response_model=schemas.EmployeeData,  status_code=201, responses={400: {"message": 'Email yet using'}})
async def up_employee(employee_id: int, employee_data: schemas.EmployeeData):
    employee_data = employee_data.dict()
    query = employees.update().where(employees.c.id == employee_id).values(**employee_data)
    try:
        employee_id = await database.execute(query)
        return employee_data
    except:
        raise HTTPException(status_code=400, detail='Email yet using')


@app.delete('/employee/{employee_id}', status_code=204)
async def del_employee(employee_id: int):
    query = employees.select().where(employees.c.id == employee_id)
    employee = await database.fetch_one(query)
    if employee:
        del_query = employees.delete().where(employees.c.id == employee_id)
        await database.execute(del_query)
