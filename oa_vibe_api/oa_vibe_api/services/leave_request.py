"""Leave request service."""
from datetime import datetime
from typing import Optional, List
from oa_vibe_api.db.models import LeaveRequest, User


class LeaveRequestService:
    """Service for leave request operations."""

    @staticmethod
    async def create_leave_request(
        user_id: int,
        leave_type: str,
        start_date: datetime,
        end_date: datetime,
        reason: str,
    ) -> LeaveRequest:
        """Create a new leave request (draft status)."""
        leave_request = LeaveRequest(
            user_id=user_id,
            leave_type=leave_type,
            start_date=start_date,
            end_date=end_date,
            reason=reason,
            status="draft",
        )
        await leave_request.save()
        return leave_request

    @staticmethod
    async def get_leave_request_by_id(leave_id: int) -> Optional[LeaveRequest]:
        """Get leave request by ID."""
        return await LeaveRequest.filter(id=leave_id).first()

    @staticmethod
    async def list_leave_requests(
        user_id: Optional[int] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> List[LeaveRequest]:
        """List leave requests with filters."""
        query = LeaveRequest.all()
        if user_id is not None:
            query = query.filter(user_id=user_id)
        if status is not None:
            query = query.filter(status=status)
        if start_date is not None:
            query = query.filter(start_date__gte=start_date)
        if end_date is not None:
            query = query.filter(end_date__lte=end_date)
        return await query.order_by("-id").offset(skip).limit(limit)

    @staticmethod
    async def update_leave_request(
        leave_id: int,
        leave_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        reason: Optional[str] = None,
    ) -> Optional[LeaveRequest]:
        """Update a draft leave request."""
        leave_request = await LeaveRequest.filter(id=leave_id, status="draft").first()
        if not leave_request:
            return None
        if leave_type is not None:
            leave_request.leave_type = leave_type
        if start_date is not None:
            leave_request.start_date = start_date
        if end_date is not None:
            leave_request.end_date = end_date
        if reason is not None:
            leave_request.reason = reason
        await leave_request.save()
        return leave_request

    @staticmethod
    async def submit_for_approval(leave_id: int) -> Optional[LeaveRequest]:
        """Submit a draft leave request for approval."""
        leave_request = await LeaveRequest.filter(id=leave_id, status="draft").first()
        if not leave_request:
            return None
        leave_request.status = "pending"
        await leave_request.save()
        return leave_request

    @staticmethod
    async def approve(leave_id: int, approver_id: int, comment: Optional[str] = None) -> Optional[LeaveRequest]:
        """Approve a pending leave request."""
        leave_request = await LeaveRequest.filter(id=leave_id, status="pending").first()
        if not leave_request:
            return None
        leave_request.status = "approved"
        leave_request.approver_id = approver_id
        leave_request.approved_at = datetime.utcnow()
        leave_request.approved_comment = comment
        await leave_request.save()
        return leave_request

    @staticmethod
    async def reject(leave_id: int, approver_id: int, comment: Optional[str] = None) -> Optional[LeaveRequest]:
        """Reject a pending leave request."""
        leave_request = await LeaveRequest.filter(id=leave_id, status="pending").first()
        if not leave_request:
            return None
        leave_request.status = "rejected"
        leave_request.approver_id = approver_id
        leave_request.approved_at = datetime.utcnow()
        leave_request.approved_comment = comment
        await leave_request.save()
        return leave_request

    @staticmethod
    async def cancel(leave_id: int) -> Optional[LeaveRequest]:
        """Cancel a draft or pending leave request."""
        leave_request = await LeaveRequest.filter(id=leave_id, status__in=["draft", "pending"]).first()
        if not leave_request:
            return None
        leave_request.status = "cancelled"
        await leave_request.save()
        return leave_request


leave_request_service = LeaveRequestService()
