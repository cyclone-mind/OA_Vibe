"""System API router."""
from datetime import date
from typing import Optional
from fastapi import APIRouter, HTTPException, status, Depends, Query
from oa_vibe_api.services import (
    auth_service,
    user_service,
    department_service,
    position_service,
    role_service,
    menu_service,
    permission_service,
)
from oa_vibe_api.db.models import User
from oa_vibe_api.web.api.system.deps import get_current_user
from oa_vibe_api.web.api.system.schemas import (
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentResponse,
    PositionCreate,
    PositionUpdate,
    PositionResponse,
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    MenuCreate,
    MenuUpdate,
    MenuResponse,
    PermissionCreate,
    PermissionUpdate,
    PermissionResponse,
    UserCreate,
    UserUpdate,
    UserResponse,
)

router = APIRouter()


# Auth endpoints
@router.post("/auth/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """User login with username and password."""
    user = await auth_service.authenticate(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    access_token, refresh_token = auth_service.create_tokens(user.id, user.username)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/auth/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """User logout."""
    return {"message": "Logged out successfully"}


@router.post("/auth/refresh", response_model=TokenResponse)
async def refresh(request: RefreshRequest):
    """Refresh access token."""
    result = auth_service.refresh_access_token(request.refresh_token)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    access_token, refresh_token = result
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


# Department endpoints
@router.post("/departments", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    request: DepartmentCreate,
    current_user: User = Depends(get_current_user),
):
    """Create a new department."""
    department = await department_service.create_department(
        name=request.name,
        parent_id=request.parent_id,
        sort=request.sort,
    )
    return DepartmentResponse(
        id=department.id,
        name=department.name,
        parent_id=department.parent_id,
        level=department.level,
        sort=department.sort,
        status=department.status,
        created_at=department.created_at,
        updated_at=department.updated_at,
    )


@router.get("/departments", response_model=list[DepartmentResponse])
async def list_departments(current_user: User = Depends(get_current_user)):
    """List all departments (flat)."""
    departments = await department_service.list_departments()
    return [
        DepartmentResponse(
            id=d.id,
            name=d.name,
            parent_id=d.parent_id,
            level=d.level,
            sort=d.sort,
            status=d.status,
            created_at=d.created_at,
            updated_at=d.updated_at,
        )
        for d in departments
    ]


@router.get("/departments/tree")
async def get_department_tree(current_user: User = Depends(get_current_user)):
    """Get department tree structure."""
    return await department_service.get_department_tree()


@router.get("/departments/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: int,
    current_user: User = Depends(get_current_user),
):
    """Get department by ID."""
    department = await department_service.get_department_by_id(department_id)
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return DepartmentResponse(
        id=department.id,
        name=department.name,
        parent_id=department.parent_id,
        level=department.level,
        sort=department.sort,
        status=department.status,
        created_at=department.created_at,
        updated_at=department.updated_at,
    )


@router.patch("/departments/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: int,
    request: DepartmentUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update department."""
    department = await department_service.update_department(
        department_id,
        name=request.name,
        parent_id=request.parent_id,
        sort=request.sort,
        status=request.status,
    )
    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department not found")
    return DepartmentResponse(
        id=department.id,
        name=department.name,
        parent_id=department.parent_id,
        level=department.level,
        sort=department.sort,
        status=department.status,
        created_at=department.created_at,
        updated_at=department.updated_at,
    )


@router.delete("/departments/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: int,
    current_user: User = Depends(get_current_user),
):
    """Delete department."""
    success = await department_service.delete_department(department_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete department with children or users",
        )


# Position endpoints
@router.post("/positions", response_model=PositionResponse, status_code=status.HTTP_201_CREATED)
async def create_position(
    request: PositionCreate,
    current_user: User = Depends(get_current_user),
):
    """Create a new position."""
    try:
        position = await position_service.create_position(name=request.name, code=request.code)
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Position code already exists")
    return PositionResponse(
        id=position.id,
        name=position.name,
        code=position.code,
        status=position.status,
        created_at=position.created_at,
        updated_at=position.updated_at,
    )


@router.get("/positions", response_model=list[PositionResponse])
async def list_positions(
    status: Optional[int] = None,
    current_user: User = Depends(get_current_user),
):
    """List positions."""
    positions = await position_service.list_positions(status=status)
    return [
        PositionResponse(
            id=p.id,
            name=p.name,
            code=p.code,
            status=p.status,
            created_at=p.created_at,
            updated_at=p.updated_at,
        )
        for p in positions
    ]


@router.get("/positions/{position_id}", response_model=PositionResponse)
async def get_position(
    position_id: int,
    current_user: User = Depends(get_current_user),
):
    """Get position by ID."""
    position = await position_service.get_position_by_id(position_id)
    if not position:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")
    return PositionResponse(
        id=position.id,
        name=position.name,
        code=position.code,
        status=position.status,
        created_at=position.created_at,
        updated_at=position.updated_at,
    )


@router.patch("/positions/{position_id}", response_model=PositionResponse)
async def update_position(
    position_id: int,
    request: PositionUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update position."""
    position = await position_service.update_position(
        position_id,
        name=request.name,
        status=request.status,
    )
    if not position:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Position not found")
    return PositionResponse(
        id=position.id,
        name=position.name,
        code=position.code,
        status=position.status,
        created_at=position.created_at,
        updated_at=position.updated_at,
    )


@router.delete("/positions/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_position(
    position_id: int,
    current_user: User = Depends(get_current_user),
):
    """Delete position."""
    success = await position_service.delete_position(position_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete position with assigned users",
        )


# Role endpoints
@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    request: RoleCreate,
    current_user: User = Depends(get_current_user),
):
    """Create a new role."""
    try:
        role = await role_service.create_role(
            name=request.name,
            code=request.code,
            description=request.description,
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Role code already exists")
    return RoleResponse(
        id=role.id,
        name=role.name,
        code=role.code,
        description=role.description,
        status=role.status,
        created_at=role.created_at,
        updated_at=role.updated_at,
    )


@router.get("/roles", response_model=list[RoleResponse])
async def list_roles(
    status: Optional[int] = None,
    current_user: User = Depends(get_current_user),
):
    """List roles."""
    roles = await role_service.list_roles(status=status)
    return [
        RoleResponse(
            id=r.id,
            name=r.name,
            code=r.code,
            description=r.description,
            status=r.status,
            created_at=r.created_at,
            updated_at=r.updated_at,
        )
        for r in roles
    ]


@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    current_user: User = Depends(get_current_user),
):
    """Get role by ID."""
    role = await role_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return RoleResponse(
        id=role.id,
        name=role.name,
        code=role.code,
        description=role.description,
        status=role.status,
        created_at=role.created_at,
        updated_at=role.updated_at,
    )


@router.patch("/roles/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    request: RoleUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update role."""
    role = await role_service.update_role(
        role_id,
        name=request.name,
        description=request.description,
        status=request.status,
    )
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return RoleResponse(
        id=role.id,
        name=role.name,
        code=role.code,
        description=role.description,
        status=role.status,
        created_at=role.created_at,
        updated_at=role.updated_at,
    )


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    current_user: User = Depends(get_current_user),
):
    """Delete role."""
    success = await role_service.delete_role(role_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete role with assigned positions",
        )


# Menu endpoints
@router.post("/menus", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
async def create_menu(
    request: MenuCreate,
    current_user: User = Depends(get_current_user),
):
    """Create a new menu."""
    menu = await menu_service.create_menu(
        name=request.name,
        path=request.path,
        icon=request.icon,
        parent_id=request.parent_id,
        sort=request.sort,
    )
    return MenuResponse(
        id=menu.id,
        name=menu.name,
        path=menu.path,
        icon=menu.icon,
        parent_id=menu.parent_id,
        sort=menu.sort,
        status=menu.status,
        created_at=menu.created_at,
        updated_at=menu.updated_at,
    )


@router.get("/menus", response_model=list[MenuResponse])
async def list_menus(current_user: User = Depends(get_current_user)):
    """List all menus (flat)."""
    menus = await menu_service.list_menus()
    return [
        MenuResponse(
            id=m.id,
            name=m.name,
            path=m.path,
            icon=m.icon,
            parent_id=m.parent_id,
            sort=m.sort,
            status=m.status,
            created_at=m.created_at,
            updated_at=m.updated_at,
        )
        for m in menus
    ]


@router.get("/menus/tree")
async def get_menu_tree(current_user: User = Depends(get_current_user)):
    """Get menu tree structure."""
    return await menu_service.get_menu_tree()


@router.get("/menus/user")
async def get_user_menus(current_user: User = Depends(get_current_user)):
    """Get menus accessible by current user's role."""
    return await menu_service.get_user_menus(current_user)


@router.patch("/menus/{menu_id}", response_model=MenuResponse)
async def update_menu(
    menu_id: int,
    request: MenuUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update menu."""
    menu = await menu_service.update_menu(
        menu_id,
        name=request.name,
        path=request.path,
        icon=request.icon,
        parent_id=request.parent_id,
        sort=request.sort,
        status=request.status,
    )
    if not menu:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
    return MenuResponse(
        id=menu.id,
        name=menu.name,
        path=menu.path,
        icon=menu.icon,
        parent_id=menu.parent_id,
        sort=menu.sort,
        status=menu.status,
        created_at=menu.created_at,
        updated_at=menu.updated_at,
    )


@router.delete("/menus/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_menu(
    menu_id: int,
    current_user: User = Depends(get_current_user),
):
    """Delete menu."""
    success = await menu_service.delete_menu(menu_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete menu with child menus",
        )


# Permission endpoints
@router.post("/permissions", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(
    request: PermissionCreate,
    current_user: User = Depends(get_current_user),
):
    """Create a new permission."""
    try:
        permission = await permission_service.create_permission(
            name=request.name,
            code=request.code,
            api_path=request.api_path,
            method=request.method,
            menu_id=request.menu_id,
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Permission code already exists")
    return PermissionResponse(
        id=permission.id,
        name=permission.name,
        code=permission.code,
        api_path=permission.api_path,
        method=permission.method,
        menu_id=permission.menu_id,
        status=permission.status,
        created_at=permission.created_at,
        updated_at=permission.updated_at,
    )


@router.get("/permissions", response_model=list[PermissionResponse])
async def list_permissions(
    menu_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
):
    """List permissions."""
    permissions = await permission_service.list_permissions(menu_id=menu_id)
    return [
        PermissionResponse(
            id=p.id,
            name=p.name,
            code=p.code,
            api_path=p.api_path,
            method=p.method,
            menu_id=p.menu_id,
            status=p.status,
            created_at=p.created_at,
            updated_at=p.updated_at,
        )
        for p in permissions
    ]


@router.patch("/permissions/{permission_id}", response_model=PermissionResponse)
async def update_permission(
    permission_id: int,
    request: PermissionUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update permission."""
    permission = await permission_service.update_permission(
        permission_id,
        name=request.name,
        api_path=request.api_path,
        method=request.method,
        menu_id=request.menu_id,
        status=request.status,
    )
    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return PermissionResponse(
        id=permission.id,
        name=permission.name,
        code=permission.code,
        api_path=permission.api_path,
        method=permission.method,
        menu_id=permission.menu_id,
        status=permission.status,
        created_at=permission.created_at,
        updated_at=permission.updated_at,
    )


@router.delete("/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission(
    permission_id: int,
    current_user: User = Depends(get_current_user),
):
    """Delete permission."""
    success = await permission_service.delete_permission(permission_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")


# User endpoints
@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: UserCreate,
    current_user: User = Depends(get_current_user),
):
    """Create a new user (admin only)."""
    try:
        user = await user_service.create_user(
            username=request.username,
            password=request.password,
            real_name=request.real_name,
            email=request.email,
            phone=request.phone,
            department_id=request.department_id,
            position_id=request.position_id,
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    return UserResponse(
        id=user.id,
        username=user.username,
        real_name=user.real_name,
        email=user.email,
        phone=user.phone,
        department_id=user.department_id,
        position_id=user.position_id,
        status=user.status,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.get("/users", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 20,
    department_id: Optional[int] = None,
    position_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
):
    """List users."""
    users = await user_service.list_users(
        skip=skip,
        limit=limit,
        department_id=department_id,
        position_id=position_id,
    )
    return [
        UserResponse(
            id=u.id,
            username=u.username,
            real_name=u.real_name,
            email=u.email,
            phone=u.phone,
            department_id=u.department_id,
            position_id=u.position_id,
            status=u.status,
            created_at=u.created_at,
            updated_at=u.updated_at,
        )
        for u in users
    ]


@router.get("/users/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user info."""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        real_name=current_user.real_name,
        email=current_user.email,
        phone=current_user.phone,
        department_id=current_user.department_id,
        position_id=current_user.position_id,
        status=current_user.status,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
):
    """Get user by ID."""
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse(
        id=user.id,
        username=user.username,
        real_name=user.real_name,
        email=user.email,
        phone=user.phone,
        department_id=user.department_id,
        position_id=user.position_id,
        status=user.status,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    request: UserUpdate,
    current_user: User = Depends(get_current_user),
):
    """Update user."""
    user = await user_service.update_user(
        user_id,
        real_name=request.real_name,
        email=request.email,
        phone=request.phone,
        department_id=request.department_id,
        position_id=request.position_id,
        status=request.status,
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse(
        id=user.id,
        username=user.username,
        real_name=user.real_name,
        email=user.email,
        phone=user.phone,
        department_id=user.department_id,
        position_id=user.position_id,
        status=user.status,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
):
    """Delete user."""
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
