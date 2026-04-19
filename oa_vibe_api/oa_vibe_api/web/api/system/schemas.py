"""System API schemas."""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# Auth schemas
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


# Department schemas
class DepartmentCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None
    sort: int = 0


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None
    sort: Optional[int] = None
    status: Optional[int] = None


class DepartmentResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    level: int
    sort: int
    status: int
    created_at: datetime
    updated_at: datetime


# Position schemas
class PositionCreate(BaseModel):
    name: str
    code: str


class PositionUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[int] = None


class PositionResponse(BaseModel):
    id: int
    name: str
    code: str
    status: int
    created_at: datetime
    updated_at: datetime


# Role schemas
class RoleCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[int] = None


class RoleResponse(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str]
    status: int
    created_at: datetime
    updated_at: datetime


# Menu schemas
class MenuCreate(BaseModel):
    name: str
    path: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    sort: int = 0


class MenuUpdate(BaseModel):
    name: Optional[str] = None
    path: Optional[str] = None
    icon: Optional[str] = None
    parent_id: Optional[int] = None
    sort: Optional[int] = None
    status: Optional[int] = None


class MenuResponse(BaseModel):
    id: int
    name: str
    path: Optional[str]
    icon: Optional[str]
    parent_id: Optional[int]
    sort: int
    status: int
    created_at: datetime
    updated_at: datetime


# Permission schemas
class PermissionCreate(BaseModel):
    name: str
    code: str
    api_path: Optional[str] = None
    method: Optional[str] = None
    menu_id: Optional[int] = None


class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    api_path: Optional[str] = None
    method: Optional[str] = None
    menu_id: Optional[int] = None
    status: Optional[int] = None


class PermissionResponse(BaseModel):
    id: int
    name: str
    code: str
    api_path: Optional[str]
    method: Optional[str]
    menu_id: Optional[int]
    status: int
    created_at: datetime
    updated_at: datetime


# User schemas
class UserCreate(BaseModel):
    username: str
    password: str
    real_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None


class UserUpdate(BaseModel):
    real_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    status: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    username: str
    real_name: str
    email: Optional[str]
    phone: Optional[str]
    department_id: Optional[int]
    position_id: Optional[int]
    status: int
    created_at: datetime
    updated_at: datetime
