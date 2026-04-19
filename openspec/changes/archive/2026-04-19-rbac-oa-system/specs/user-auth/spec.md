## ADDED Requirements

### Requirement: User login with JWT
The system SHALL allow users to authenticate using username and password, returning JWT access and refresh tokens.

#### Scenario: Successful login
- **WHEN** user submits valid username and password to POST /api/system/auth/login
- **THEN** system returns 200 with access_token, refresh_token, token_type, and user info

#### Scenario: Invalid credentials
- **WHEN** user submits invalid username or password to POST /api/system/auth/login
- **THEN** system returns 401 Unauthorized with error message

### Requirement: User logout
The system SHALL invalidate the current JWT token on logout.

#### Scenario: Successful logout
- **WHEN** authenticated user calls POST /api/system/auth/logout with valid token
- **THEN** system returns 200 and marks token as invalid

### Requirement: Token refresh
The system SHALL allow users to obtain a new access token using a valid refresh token.

#### Scenario: Refresh with valid token
- **WHEN** user submits valid refresh_token to POST /api/system/auth/refresh
- **THEN** system returns 200 with new access_token and refresh_token

#### Scenario: Refresh with expired token
- **WHEN** user submits expired refresh_token to POST /api/system/auth/refresh
- **THEN** system returns 401 Unauthorized

### Requirement: No user registration
The system SHALL NOT provide a user registration endpoint. Users MUST be created by administrators.

#### Scenario: Registration attempt
- **WHEN** client calls POST /api/system/auth/register
- **THEN** system returns 405 Method Not Allowed
