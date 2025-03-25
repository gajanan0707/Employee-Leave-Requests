from sqlalchemy import Column, Integer, String, DateTime, Enum
from .database import Base
from .schema.schema import LeaveType, LeaveStatus

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