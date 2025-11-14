# Backend/permissions/schemas.py
from pydantic import BaseModel

class PermissionBase(BaseModel):
    name: str

class PermissionCreate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: int

    class Config:
        from_attributes = True  # ✅ for Pydantic v2
