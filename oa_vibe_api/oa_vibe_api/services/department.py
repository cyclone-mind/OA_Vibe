"""Department service."""
from typing import Optional, List
from oa_vibe_api.db.models import Department


class DepartmentService:
    """Service for department operations."""

    @staticmethod
    async def create_department(
        name: str,
        parent_id: Optional[int] = None,
        sort: int = 0,
    ) -> Department:
        """Create a new department."""
        level = 1
        if parent_id:
            parent = await Department.filter(id=parent_id).first()
            if parent:
                level = parent.level + 1

        department = Department(
            name=name,
            parent_id=parent_id,
            level=level,
            sort=sort,
        )
        await department.save()
        return department

    @staticmethod
    async def get_department_by_id(department_id: int) -> Optional[Department]:
        """Get department by ID."""
        return await Department.filter(id=department_id).first()

    @staticmethod
    async def list_departments() -> List[Department]:
        """List all active departments."""
        return await Department.filter(status=1).order_by("sort", "id")

    @staticmethod
    async def get_department_tree() -> List[dict]:
        """Get department tree structure."""
        departments = await Department.filter(status=1).order_by("sort", "id")
        return DepartmentService._build_tree(departments)

    @staticmethod
    def _build_tree(departments: List[Department]) -> List[dict]:
        """Build tree structure from flat department list."""
        dept_dict = {d.id: {"id": d.id, "name": d.name, "parent_id": d.parent_id, "level": d.level, "sort": d.sort, "children": []} for d in departments}
        tree = []
        for d in departments:
            node = dept_dict[d.id]
            if d.parent_id and d.parent_id in dept_dict:
                dept_dict[d.parent_id]["children"].append(node)
            else:
                tree.append(node)
        return tree

    @staticmethod
    async def update_department(
        department_id: int,
        name: Optional[str] = None,
        parent_id: Optional[int] = None,
        sort: Optional[int] = None,
        status: Optional[int] = None,
    ) -> Optional[Department]:
        """Update department information."""
        department = await Department.filter(id=department_id).first()
        if not department:
            return None

        if name is not None:
            department.name = name
        if sort is not None:
            department.sort = sort
        if status is not None:
            department.status = status
        if parent_id is not None and parent_id != department.parent_id:
            department.parent_id = parent_id
            level = 1
            if parent_id:
                parent = await Department.filter(id=parent_id).first()
                if parent:
                    level = parent.level + 1
            department.level = level
            await DepartmentService._update_children_levels(department_id, level)

        await department.save()
        return department

    @staticmethod
    async def _update_children_levels(parent_id: int, parent_level: int):
        """Update levels of all child departments."""
        children = await Department.filter(parent_id=parent_id)
        for child in children:
            child.level = parent_level + 1
            await child.save()
            await DepartmentService._update_children_levels(child.id, child.level)

    @staticmethod
    async def delete_department(department_id: int) -> bool:
        """Soft delete a department."""
        department = await Department.filter(id=department_id).first()
        if not department:
            return False

        # Check for children
        children = await Department.filter(parent_id=department_id, status=1)
        if children:
            return False

        department.status = 0
        await department.save()
        return True


department_service = DepartmentService()
