from fastapi import APIRouter, HTTPException, Path
from typing import List

from app.api import crud
from app.api.models import EmployeeDB, EmployeeSchema

router = APIRouter()


@router.post("/", response_model=EmployeeDB, status_code=201)
async def create_employee(payload: EmployeeSchema):
    employee_id = await crud.post(payload)

    response_object = {
        "id": employee_id,
        "name": payload.name,
        "second_name": payload.second_name,
        "salary": payload.salary,
    }
    return response_object


@router.get("/{id}/", response_model=EmployeeDB)
async def read_employee(id: int = Path(..., gt=0), ):
    employee = await crud.get(id)
    if not employee:
        raise HTTPException(status_code=404, detail="Note not found")
    return employee


@router.put("/{id}/", response_model=EmployeeDB)
async def update_employee(payload: EmployeeSchema, id: int = Path(..., gt=0), ):
    employee = await crud.get(id)
    if not employee:
        raise HTTPException(status_code=404, detail="Note not found")

    employee_id = await crud.put(id, payload)

    response_object = {
        "id": employee_id,
        "name": payload.name,
        "second_name": payload.second_name,
        "salary": payload.salary,
    }
    return response_object


@router.get("/", response_model=List[EmployeeDB])
async def read_all_employees():
    return await crud.get_all()


@router.delete("/{id}/", response_model=EmployeeDB)
async def delete_employee(id: int = Path(..., gt=0)):
    employee = await crud.get(id)
    if not employee:
        raise HTTPException(status_code=404, detail="Note not found")

    await crud.delete(id)

    return employee