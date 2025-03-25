import sqlalchemy
from typing import List
from .schema import schema
from datetime import date, datetime
from sqlalchemy import create_engine
from pydantic import BaseModel, constr
from sqlalchemy.orm import Session, sessionmaker
from fastapi import FastAPI, Depends, HTTPException
from app.schema.schema import LeaveType, LeaveStatus
from dateutil.rrule import rrule, DAILY, MO, TU, WE, TH, FR
from sqlalchemy import Column, Integer, String, DateTime, Enum

app = FastAPI()
database_url = "sqlite:///./employee_db.db"


engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = sqlalchemy.orm.declarative_base()


class EmployeeLeaveRequest(Base):
    __tablename__ = "employe_leave_request"

    id = Column(Integer, primary_key=True)
    employee_id = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    leave_type = Column(Enum(LeaveType))
    reason = Column(String)
    status = Column(Enum(LeaveStatus), default=LeaveStatus.PENDING)
    working_days = Column(Integer)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def health_check():
    return {"status": "OK"}


class LeaveRequestCreate(BaseModel):
    employee_id: str
    start_date: date
    end_date: date
    leave_type: schema.LeaveType
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


def calculate_working_days(start_date: date, end_date: date):
    days = rrule(
        DAILY, dtstart=start_date, until=end_date, byweekday=(MO, TU, WE, TH, FR)
    )

    return len(list(days))


@app.post("/api/v1/leave-requests")
async def LeaveRequest(request: LeaveRequestCreate, db: Session = Depends(get_db)):
    start_date = request.start_date
    end_date = request.end_date
    if end_date <= start_date:
        return HTTPException(
            status_code=400, detail={"error": "end_date must be after start_date"}
        )

    working_days = calculate_working_days(start_date, end_date)
    if working_days > 14:
        return HTTPException(
            status_code=400, detail={"error": "Maximum consecutive leave days: 14"}
        )

    overlapping = (
        db.query(EmployeeLeaveRequest)
        .filter(
            EmployeeLeaveRequest.employee_id == request.employee_id,
            EmployeeLeaveRequest.start_date <= request.start_date,
            EmployeeLeaveRequest.end_date >= request.end_date,
        )
        .first()
    )

    if overlapping:
        return HTTPException(
            status_code=400, detail={"error": "overlapping leave request exist"}
        )

    db_request = EmployeeLeaveRequest(
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


@app.get(
    "/api/v1/leave-requests/{employee_id}", response_model=List[LeaveRequestResponse]
)
async def get_employee_leave_request(employee_id: str, db: Session = Depends(get_db)):
    employe_data = (
        db.query(EmployeeLeaveRequest)
        .filter(EmployeeLeaveRequest.employee_id == employee_id)
        .all()
    )

    return employe_data
