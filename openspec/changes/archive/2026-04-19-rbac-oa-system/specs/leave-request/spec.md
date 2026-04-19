## ADDED Requirements

### Requirement: Create leave request
The system SHALL allow authenticated users to create leave requests with leave type, date range, and reason.

#### Scenario: Create valid leave request
- **WHEN** user submits valid leave request data to POST /api/oa/leave-requests
- **THEN** system returns 201 with created leave request in "draft" status

#### Scenario: Create leave request with invalid dates
- **WHEN** user submits end_date before start_date to POST /api_oa/leave-requests
- **THEN** system returns 400 Bad Request with validation error

### Requirement: Submit leave request for approval
The system SHALL allow users to submit draft leave requests for approval.

#### Scenario: Submit draft request
- **WHEN** user calls POST /api/oa/leave-requests/{id}/submit for a draft request
- **THEN** system returns 200 and changes status to "pending"

#### Scenario: Submit already pending request
- **WHEN** user calls POST /api/oa/leave-requests/{id}/submit for an already pending request
- **THEN** system returns 409 Conflict

### Requirement: Approve leave request
The system SHALL allow approvers to approve pending leave requests.

#### Scenario: Approve pending request
- **WHEN** approver calls POST /api/oa/leave-requests/{id}/approve with approval comment
- **THEN** system returns 200, sets status to "approved", and records approver_id and approved_at

#### Scenario: Non-approver tries to approve
- **WHEN** non-approver calls POST /api/oa/leave-requests/{id}/approve
- **THEN** system returns 403 Forbidden

### Requirement: Reject leave request
The system SHALL allow approvers to reject pending leave requests with a reason.

#### Scenario: Reject pending request
- **WHEN** approver calls POST /api/oa/leave-requests/{id}/reject with rejection reason
- **THEN** system returns 200, sets status to "rejected", and records approver_id and approved_comment

### Requirement: Query leave requests
The system SHALL return leave requests with filtering by status, user, and date range.

#### Scenario: List user's own leave requests
- **WHEN** user calls GET /api/oa/leave-requests
- **THEN** system returns 200 with list of user's own leave requests

#### Scenario: Filter by status
- **WHEN** approver calls GET /api/oa/leave-requests?status=pending
- **THEN** system returns 200 with all pending leave requests

#### Scenario: Filter by date range
- **WHEN** user calls GET /api/oa/leave-requests?start_date=2026-01-01&end_date=2026-12-31
- **THEN** system returns 200 with leave requests within date range

### Requirement: Cancel leave request
The system SHALL allow users to cancel their own draft or pending leave requests.

#### Scenario: Cancel own pending request
- **WHEN** user calls POST /api/oa/leave-requests/{id}/cancel for their own pending request
- **THEN** system returns 200 and changes status to "cancelled"
