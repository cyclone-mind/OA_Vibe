## ADDED Requirements

### Requirement: Create role
The system SHALL allow administrators to create roles with unique code, name, and description.

#### Scenario: Create valid role
- **WHEN** admin submits valid role data to POST /api/system/roles
- **THEN** system returns 201 with created role

#### Scenario: Create role with duplicate code
- **WHEN** admin submits role code that already exists to POST /api/system/roles
- **THEN** system returns 409 Conflict

### Requirement: Assign permissions to role
The system SHALL allow administrators to assign multiple permissions to a role.

#### Scenario: Assign permissions to role
- **WHEN** admin submits permission_ids to PUT /api/system/roles/{id}/permissions
- **THEN** system returns 200 and replaces role's permission associations

### Requirement: Query roles
The system SHALL return roles with optional filtering and pagination.

#### Scenario: List all active roles
- **WHEN** user calls GET /api/system/roles
- **THEN** system returns 200 with list of all active roles

#### Scenario: Get role with permissions
- **WHEN** user calls GET /api/system/roles/{id}
- **THEN** system returns 200 with role including associated permissions

### Requirement: Update and delete role
The system SHALL allow updating role details and soft-deleting roles.

#### Scenario: Update role
- **WHEN** admin submits updated data to PATCH /api/system/roles/{id}
- **THEN** system returns 200 with updated role

#### Scenario: Delete role with assigned positions
- **WHEN** admin calls DELETE /api/system/roles/{id} for role assigned to positions
- **THEN** system returns 409 Conflict
