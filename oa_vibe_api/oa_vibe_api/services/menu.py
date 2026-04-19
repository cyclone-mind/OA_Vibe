"""Menu service."""
from typing import Optional, List
from oa_vibe_api.db.models import Menu


class MenuService:
    """Service for menu operations."""

    @staticmethod
    async def create_menu(
        name: str,
        path: Optional[str] = None,
        icon: Optional[str] = None,
        parent_id: Optional[int] = None,
        sort: int = 0,
    ) -> Menu:
        """Create a new menu."""
        menu = Menu(name=name, path=path, icon=icon, parent_id=parent_id, sort=sort)
        await menu.save()
        return menu

    @staticmethod
    async def get_menu_by_id(menu_id: int) -> Optional[Menu]:
        """Get menu by ID."""
        return await Menu.filter(id=menu_id).first()

    @staticmethod
    async def list_menus() -> List[Menu]:
        """List all active menus."""
        return await Menu.filter(status=1).order_by("sort", "id")

    @staticmethod
    async def get_menu_tree() -> List[dict]:
        """Get menu tree structure."""
        menus = await Menu.filter(status=1).order_by("sort", "id")
        return MenuService._build_tree(menus)

    @staticmethod
    def _build_tree(menus: List[Menu]) -> List[dict]:
        """Build tree structure from flat menu list."""
        menu_dict = {m.id: {"id": m.id, "name": m.name, "path": m.path, "icon": m.icon, "parent_id": m.parent_id, "sort": m.sort, "children": []} for m in menus}
        tree = []
        for m in menus:
            node = menu_dict[m.id]
            if m.parent_id and m.parent_id in menu_dict:
                menu_dict[m.parent_id]["children"].append(node)
            else:
                tree.append(node)
        return tree

    @staticmethod
    async def update_menu(
        menu_id: int,
        name: Optional[str] = None,
        path: Optional[str] = None,
        icon: Optional[str] = None,
        parent_id: Optional[int] = None,
        sort: Optional[int] = None,
        status: Optional[int] = None,
    ) -> Optional[Menu]:
        """Update menu information."""
        menu = await Menu.filter(id=menu_id).first()
        if not menu:
            return None
        if name is not None:
            menu.name = name
        if path is not None:
            menu.path = path
        if icon is not None:
            menu.icon = icon
        if parent_id is not None:
            menu.parent_id = parent_id
        if sort is not None:
            menu.sort = sort
        if status is not None:
            menu.status = status
        await menu.save()
        return menu

    @staticmethod
    async def delete_menu(menu_id: int) -> bool:
        """Soft delete a menu."""
        menu = await Menu.filter(id=menu_id).first()
        if not menu:
            return False

        children = await Menu.filter(parent_id=menu_id, status=1)
        if children:
            return False

        menu.status = 0
        await menu.save()
        return True


menu_service = MenuService()
