"""OA API schemas."""
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel


class LeaveRequestCreate(BaseModel):
    leave_type: str
    start_date: date
    end_date: date
    reason: str


class LeaveRequestUpdate(BaseModel):
    leave_type: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None


class LeaveRequestApprove(BaseModel):
    comment: Optional[str] = None


class LeaveRequestReject(BaseModel):
    comment: Optional[str] = None


class LeaveRequestResponse(BaseModel):
    id: int
    user_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str
    status: str
    approver_id: Optional[int]
    approved_at: Optional[datetime]
    approved_comment: Optional[str]
    created_at: datetime
    updated_at: datetime
