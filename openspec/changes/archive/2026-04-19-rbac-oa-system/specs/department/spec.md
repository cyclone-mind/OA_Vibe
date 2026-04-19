## ADDED Requirements

### Requirement: Create department
The system SHALL allow administrators to create departments with optional parent for hierarchy.

#### Scenario: Create root department
- **WHEN** admin submits valid department data to POST /api/system/departments
- **THEN** system returns 201 with created department including auto-computed level

#### Scenario: Create child department
- **WHEN** admin submits department data with valid parent_id to POST /api/system/departments
- **THEN** system returns 201 with child department having level = parent.level + 1

### Requirement: Query department tree
The system SHALL return departments in a tree structure or flat list with parent references.

#### Scenario: Get department tree
- **WHEN** user calls GET /api/system/departments/tree
- **THEN** system returns 200 with nested tree structure of all active departments

#### Scenario: Get department flat list
- **WHEN** user calls GET /api/system/departments
- **THEN** system returns 200 with flat list including id, name, parent_id, level

### Requirement: Update department
The system SHALL allow administrators to update department name or move department to new parent.

#### Scenario: Update department name
- **WHEN** admin submits updated name to PATCH /api/system/departments/{id}
- **THEN** system returns 200 with updated department

#### Scenario: Move department to new parent
- **WHEN** admin submits new parent_id to PATCH /api/system/departments/{id}
- **THEN** system recalculates level for department and all descendants

### Requirement: Delete department
The system SHALL soft-delete departments. Departments with child departments or assigned users SHALL NOT be deletable.

#### Scenario: Delete empty department
- **WHEN** admin calls DELETE /api/system/departments/{id} for department with no children or users
- **THEN** system returns 204 and sets status to inactive

#### Scenario: Delete department with children
- **WHEN** admin calls DELETE /api/system/departments/{id} for department with child departments
- **THEN** system returns 409 Conflict with error message
