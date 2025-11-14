# Backend/permissions/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Backend.Database.connections import get_db
from Backend.Database import models
from .schema import PermissionCreate, PermissionResponse

router = APIRouter(prefix="/permissions", tags=["Permissions"])

# CREATE Permission
@router.post("/", response_model=PermissionResponse)
def create_permission(payload: PermissionCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Permission).filter(models.Permission.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Permission already exists")
    new_permission = models.Permission(name=payload.name)
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    return new_permission

# READ ALL Permissions
@router.get("/", response_model=list[PermissionResponse])
def get_permissions(db: Session = Depends(get_db)):
    return db.query(models.Permission).all()

# READ by ID
@router.get("/{permission_id}", response_model=PermissionResponse)
def get_permission(permission_id: int, db: Session = Depends(get_db)):
    permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

# DELETE
@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    db.delete(permission)
    db.commit()
    return None

# LINK Permission to Role
@router.post("/assign/{role_id}/{permission_id}")
def assign_permission_to_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()

    if not role or not permission:
        raise HTTPException(status_code=404, detail="Role or Permission not found")

    if permission in role.permissions:
        raise HTTPException(status_code=400, detail="Permission already assigned")

    role.permissions.append(permission)
    db.commit()
    return {"message": f"Permission '{permission.name}' assigned to role '{role.name}'"}

# UNLINK Permission from Role
@router.delete("/unassign/{role_id}/{permission_id}")
def remove_permission_from_role(role_id: int, permission_id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    permission = db.query(models.Permission).filter(models.Permission.id == permission_id).first()

    if not role or not permission:
        raise HTTPException(status_code=404, detail="Role or Permission not found")

    if permission not in role.permissions:
        raise HTTPException(status_code=400, detail="Permission not assigned")

    role.permissions.remove(permission)
    db.commit()
    return {"message": f"Permission '{permission.name}' removed from role '{role.name}'"}
