from app.api.models import EmployeeSchema
from app.db import employees, database


async def post(payload: EmployeeSchema):
    query = employees.insert().values(name=payload.name, second_name=payload.second_name, salary=payload.salary)
    return await database.execute(query=query)


async def get(id: int):
    query = employees.select().where(id == employees.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = employees.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: EmployeeSchema):
    query = (
        employees
        .update()
        .where(id == employees.c.id)
        .values(name=payload.name, second_name=payload.second_name, salary=payload.salary)
        .returning(employees.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = employees.delete().where(id == employees.c.id)
    return await database.execute(query=query)