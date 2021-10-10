from pydantic import BaseModel, Field


class EmployeeSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    second_name: str = Field(..., min_length=2, max_length=50)
    salary: int = Field(..., gt=0, lt=50000)


class EmployeeDB(EmployeeSchema):
    id: int