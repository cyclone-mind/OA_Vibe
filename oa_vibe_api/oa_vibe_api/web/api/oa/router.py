"""OA API router."""
from datetime import date
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from oa_vibe_api.services import leave_request_service
from oa_vibe_api.db.models import User
from oa_vibe_api.web.api.system.deps import get_current_user
from oa_vibe_api.web.api.oa.schemas import (
    LeaveRequestCreate,
    LeaveRequestUpdate,
    LeaveRequestApprove,
    LeaveRequestReject,
    LeaveRequestResponse,
)

router = APIRouter()


@router.post("/leave-requests", response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_leave_request(
    request: LeaveRequestCreate,
    current_user: User = Depends(get_current_user),
):
    """Create a new leave request (draft)."""
    if request.end_date < request.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date",
        )
    leave_request = await leave_request_service.create_leave_request(
        user_id=current_user.id,
        leave_type=request.leave_type,
        start_date=request.start_date,
        end_date=request.end_date,
        reason=request.reason,
    )
    return LeaveRequestResponse(
        id=leave_request.id,
        user_id=leave_request.user_id,
        leave_type=leave_request.leave_type,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        reason=leave_request.reason,
        status=leave_request.status,
        approver_id=leave_request.approver_id,
        approved_at=leave_request.approved_at,
        approved_comment=leave_request.approved_comment,
        created_at=leave_request.created_at,
        updated_at=leave_request.updated_at,
    )


@router.get("/leave-requests", response_model=list[LeaveRequestResponse])
async def list_leave_requests(
    status: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
):
    """List leave requests for current user."""
    leave_requests = await leave_request_service.list_leave_requests(
        user_id=current_user.id,
        status=status,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        limit=limit,
    )
    return [
        LeaveRequestResponse(
            id=lr.id,
            user_id=lr.user_id,
            leave_type=lr.leave_type,
            start_date=lr.start_date,
            end_date=lr.end_date,
            reason=lr.reason,
            status=lr.status,
            approver_id=lr.approver_id,
            approved_at=lr.approved_at,
            approved_comment=lr.approved_comment,
            created_at=lr.created_at,
            updated_at=lr.updated_at,
        )
        for lr in leave_requests
    ]


@router.get("/leave-requests/{leave_id}", response_model=LeaveRequestResponse)
async def get_leave_request(
    leave_id: int,
    current_user: User = Depends(get_current_user),
):
    """Get leave request by ID."""
    leave_request = await leave_request_service.get_leave_request_by_id(leave_id)
    if not leave_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave request not found")
    return LeaveRequestResponse(
        id=leave_request.id,
        user_id=leave_request.user_id,
        leave_type=leave_request.leave_type,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        reason=leave_request.reason,
        status=leave_request.status,
        approver_id=leave_request.approver_id,
        approved_at=leave_request.approved_at,
        approved_comment=leave_request.approved_comment,
        created_at=leave_request.created_at,
        updated_at=leave_request.updated_at,
    )


@router.patch("/leave-requests/{leave_id}", response_model=LeaveRequestResponse)
async def update_leave_request(
    leave_id: int,
    request: LeaveRequestUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update a draft leave request."""
    leave_request = await leave_request_service.update_leave_request(
        leave_id,
        leave_type=request.leave_type,
        start_date=request.start_date,
        end_date=request.end_date,
        reason=request.reason,
    )
    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Leave request not found or not in draft status",
        )
    return LeaveRequestResponse(
        id=leave_request.id,
        user_id=leave_request.user_id,
        leave_type=leave_request.leave_type,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        reason=leave_request.reason,
        status=leave_request.status,
        approver_id=leave_request.approver_id,
        approved_at=leave_request.approved_at,
        approved_comment=leave_request.approved_comment,
        created_at=leave_request.created_at,
        updated_at=leave_request.updated_at,
    )


@router.post("/leave-requests/{leave_id}/submit", response_model=LeaveRequestResponse)
async def submit_leave_request(
    leave_id: int,
    current_user: User = Depends(get_current_user),
):
    """Submit a draft leave request for approval."""
    leave_request = await leave_request_service.submit_for_approval(leave_id)
    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Leave request not found or not in draft status",
        )
    return LeaveRequestResponse(
        id=leave_request.id,
        user_id=leave_request.user_id,
        leave_type=leave_request.leave_type,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        reason=leave_request.reason,
        status=leave_request.status,
        approver_id=leave_request.approver_id,
        approved_at=leave_request.approved_at,
        approved_comment=leave_request.approved_comment,
        created_at=leave_request.created_at,
        updated_at=leave_request.updated_at,
    )


@router.post("/leave-requests/{leave_id}/approve", response_model=LeaveRequestResponse)
async def approve_leave_request(
    leave_id: int,
    request: LeaveRequestApprove,
    current_user: User = Depends(get_current_user),
):
    """Approve a pending leave request."""
    leave_request = await leave_request_service.approve(
        leave_id,
        approver_id=current_user.id,
        comment=request.comment,
    )
    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Leave request not found or not pending",
        )
    return LeaveRequestResponse(
        id=leave_request.id,
        user_id=leave_request.user_id,
        leave_type=leave_request.leave_type,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        reason=leave_request.reason,
        status=leave_request.status,
        approver_id=leave_request.approver_id,
        approved_at=leave_request.approved_at,
        approved_comment=leave_request.approved_comment,
        created_at=leave_request.created_at,
        updated_at=leave_request.updated_at,
    )


@router.post("/leave-requests/{leave_id}/reject", response_model=LeaveRequestResponse)
async def reject_leave_request(
    leave_id: int,
    request: LeaveRequestReject,
    current_user: User = Depends(get_current_user),
):
    """Reject a pending leave request."""
    leave_request = await leave_request_service.reject(
        leave_id,
        approver_id=current_user.id,
        comment=request.comment,
    )
    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Leave request not found or not pending",
        )
    return LeaveRequestResponse(
        id=leave_request.id,
        user_id=leave_request.user_id,
        leave_type=leave_request.leave_type,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        reason=leave_request.reason,
        status=leave_request.status,
        approver_id=leave_request.approver_id,
        approved_at=leave_request.approved_at,
        approved_comment=leave_request.approved_comment,
        created_at=leave_request.created_at,
        updated_at=leave_request.updated_at,
    )


@router.post("/leave-requests/{leave_id}/cancel", response_model=LeaveRequestResponse)
async def cancel_leave_request(
    leave_id: int,
    current_user: User = Depends(get_current_user),
):
    """Cancel a draft or pending leave request."""
    leave_request = await leave_request_service.cancel(leave_id)
    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Leave request not found or cannot be cancelled",
        )
    return LeaveRequestResponse(
        id=leave_request.id,
        user_id=leave_request.user_id,
        leave_type=leave_request.leave_type,
        start_date=leave_request.start_date,
        end_date=leave_request.end_date,
        reason=leave_request.reason,
        status=leave_request.status,
        approver_id=leave_request.approver_id,
        approved_at=leave_request.approved_at,
        approved_comment=leave_request.approved_comment,
        created_at=leave_request.created_at,
        updated_at=leave_request.updated_at,
    )
