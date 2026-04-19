## ADDED Requirements

### Requirement: Create menu
The system SHALL allow administrators to create menus with optional parent for hierarchy.

#### Scenario: Create root menu
- **WHEN** admin submits valid menu data to POST /api/system/menus
- **THEN** system returns 201 with created menu

#### Scenario: Create child menu
- **WHEN** admin submits menu data with valid parent_id to POST /api/system/menus
- **THEN** system returns 201 with child menu

### Requirement: Query menu tree
The system SHALL return menus in a tree structure for sidebar navigation.

#### Scenario: Get menu tree
- **WHEN** user calls GET /api/system/menus/tree
- **THEN** system returns 200 with nested tree structure of all active menus

### Requirement: Create permission
The system SHALL allow administrators to create permission points associated with menus and API paths.

#### Scenario: Create API permission
- **WHEN** admin submits permission data with menu_id, api_path, method to POST /api/system/permissions
- **THEN** system returns 201 with created permission

#### Scenario: Create permission with duplicate code
- **WHEN** admin submits permission code that already exists to POST /api/system/permissions
- **THEN** system returns 409 Conflict

### Requirement: Query permissions
The system SHALL return permissions with optional filtering by menu or status.

#### Scenario: List all active permissions
- **WHEN** user calls GET /api/system/permissions
- **THEN** system returns 200 with list of all active permissions

#### Scenario: Filter permissions by menu
- **WHEN** user calls GET /api/system/permissions?menu_id={id}
- **THEN** system returns 200 with permissions belonging to specified menu

### Requirement: Update and delete menu/permission
The system SHALL allow updating and soft-deleting menus and permissions.

#### Scenario: Update menu
- **WHEN** admin submits updated data to PATCH /api/system/menus/{id}
- **THEN** system returns 200 with updated menu

#### Scenario: Delete menu with children
- **WHEN** admin calls DELETE /api/system/menus/{id} for menu with child menus
- **THEN** system returns 409 Conflict
