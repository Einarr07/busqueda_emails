from enum import Enum as PyEnum


class IsActiveEnum(str, PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
