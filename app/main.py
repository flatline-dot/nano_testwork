from typing import List
from fastapi import FastAPI, Depends, HTTPException
from databases import Database

from app import schemas
from .db import employees
from .dependencies import db_conn


app = FastAPI()


@app.get(
         '/employee/{employee_id}',
         response_model=schemas.Employee,
         responses={404: {"message": 'Employee not found'}}
         )
async def get_employee(employee_id: int, db: Database = Depends(db_conn)):
    query = employees.select().where(employees.c.id == employee_id)
    employee = await db.fetch_one(query)
    if not employee:
        raise HTTPException(status_code=404, detail='Employee not found')
    return employee


@app.get('/employees/', response_model=List[schemas.Employee])
async def get_employees(skip: int = 0, limit: int = 10, db: Database = Depends(db_conn)):
    query = employees.select()
    employees_list = await db.fetch_all(query)

    return employees_list[skip:skip + limit]


@app.post('/employee/',
          response_model=schemas.Employee,
          responses={400: {"message": 'Email yet using'}}
          )
async def create_employee(employee_data: schemas.EmployeeData, db: Database = Depends(db_conn)):
    employee_data = employee_data.dict()

    is_employee = employees.select().where(employees.c.email == employee_data['email'])
    employee = await db.execute(is_employee)
    if employee:
        raise HTTPException(status_code=400, detail='Email yet using')

    query = employees.insert().values(**employee_data)
    employee_id = await db.execute(query)

    return {'id': employee_id, **employee_data}


@app.put('/employee/{employee_id}',
         response_model=schemas.EmployeeData,
         status_code=201,
         responses={400: {"message": 'Email yet using'}}
         )
async def up_employee(employee_id: int, employee_data: schemas.EmployeeData, db: Database = Depends(db_conn)):
    employee_data = employee_data.dict()
    is_employee = employees.select().where(employees.c.id == employee_id)
    employee = await db.execute(is_employee)

    if not employee:
        raise HTTPException(status_code=404, detail='Employee not found')

    is_email = employees.select().where(employees.c.email == employee_data['email'])
    employee = await db.execute(is_email)

    if employee and employee != employee_id:
        raise HTTPException(status_code=400, detail='Email yet using')

    query = employees.update().where(employees.c.id == employee_id).values(**employee_data)
    await db.execute(query)

    return employee_data


@app.delete('/employee/{employee_id}', status_code=204)
async def del_employee(employee_id: int, db: Database = Depends(db_conn)):
    del_query = employees.delete().where(employees.c.id == employee_id)
    await db.execute(del_query)
