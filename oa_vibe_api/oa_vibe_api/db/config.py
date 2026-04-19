from oa_vibe_api.settings import settings

MODELS_MODULES: list[str] = [
    "oa_vibe_api.db.models.department",
    "oa_vibe_api.db.models.menu",
    "oa_vibe_api.db.models.permission",
    "oa_vibe_api.db.models.position",
    "oa_vibe_api.db.models.role",
    "oa_vibe_api.db.models.user",
    "oa_vibe_api.db.models.leave_request",
]

TORTOISE_CONFIG = {
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": [*MODELS_MODULES, "aerich.models"],
            "default_connection": "default",
        },
    },
}
