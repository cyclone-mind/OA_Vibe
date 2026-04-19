## ADDED Requirements

### Requirement: Create position
The system SHALL allow administrators to create positions with unique code and name.

#### Scenario: Create valid position
- **WHEN** admin submits valid position data to POST /api/system/positions
- **THEN** system returns 201 with created position

#### Scenario: Create position with duplicate code
- **WHEN** admin submits position code that already exists to POST /api/system/positions
- **THEN** system returns 409 Conflict

### Requirement: Query positions
The system SHALL return positions with optional filtering by status.

#### Scenario: List all active positions
- **WHEN** user calls GET /api/system/positions
- **THEN** system returns 200 with list of all active positions

#### Scenario: Filter positions by status
- **WHEN** user calls GET /api/system/positions?status=inactive
- **THEN** system returns 200 with list of inactive positions

### Requirement: Assign roles to position
The system SHALL allow administrators to assign multiple roles to a position.

#### Scenario: Assign roles to position
- **WHEN** admin submits role_ids to PUT /api/system/positions/{id}/roles
- **THEN** system returns 200 and replaces position's role associations

### Requirement: Update and delete position
The system SHALL allow updating position name/code and soft-deleting positions.

#### Scenario: Update position
- **WHEN** admin submits updated data to PATCH /api/system/positions/{id}
- **THEN** system returns 200 with updated position

#### Scenario: Delete position with users
- **WHEN** admin calls DELETE /api/system/positions/{id} for position assigned to users
- **THEN** system returns 409 Conflict
