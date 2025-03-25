from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import get_db

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "OK"}

@router.post("/api/v1/leave-requests")
async def create_leave_request(request: schemas.LeaveRequestCreate, db: Session = Depends(get_db)):
    if request.end_date <= request.start_date:
        raise HTTPException(
            status_code=400, detail={"error": "end_date must be after start_date"}
        )

    working_days = utils.calculate_working_days(request.start_date, request.end_date)
    if working_days > 14:
        raise HTTPException(
            status_code=400, detail={"error": "Maximum consecutive leave days: 14"}
        )

    overlapping = (
        db.query(models.EmployeeLeaveRequest)
        .filter(
            models.EmployeeLeaveRequest.employee_id == request.employee_id,
            models.EmployeeLeaveRequest.start_date <= request.start_date,
            models.EmployeeLeaveRequest.end_date >= request.end_date,
        )
        .first()
    )

    if overlapping:
        raise HTTPException(
            status_code=400, detail={"error": "overlapping leave request exist"}
        )

    db_request = models.EmployeeLeaveRequest(
        employee_id=request.employee_id,
        start_date=request.start_date,
        end_date=request.end_date,
        leave_type=request.leave_type,
        reason=request.reason,
        working_days=working_days,
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)

    return {
        "employee_id": request.employee_id,
        "start_date": request.start_date,
        "end_date": request.end_date,
        "leave_type": request.leave_type,
        "reason": request.reason,
    }

@router.get("/api/v1/leave-requests/{employee_id}", response_model=List[schemas.LeaveRequestResponse])
async def get_employee_leave_request(employee_id: str, db: Session = Depends(get_db)):
    employee_data = (
        db.query(models.EmployeeLeaveRequest)
        .filter(models.EmployeeLeaveRequest.employee_id == employee_id)
        .all()
    )
    return employee_data