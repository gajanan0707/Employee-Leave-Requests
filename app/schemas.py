from pydantic import BaseModel, constr
from datetime import date
from .schema.schema import LeaveType

class LeaveRequestCreate(BaseModel):
    employee_id: str
    start_date: date
    end_date: date
    leave_type: LeaveType
    reason: constr(min_length=10)

class LeaveRequestResponse(BaseModel):
    id: int
    employee_id: str
    start_date: date
    end_date: date
    leave_type: str
    reason: str
    status: str
    working_days: int

    class Config:
        from_attributes = True