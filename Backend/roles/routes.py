# Backend/roles/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Backend.Database.connections import get_db
from Backend.Database import models
from .schemas import RoleCreate, RoleResponse

router = APIRouter(prefix="/roles", tags=["Roles"])

# CREATE ROLE
@router.post("/", response_model=RoleResponse)
def create_role(payload: RoleCreate, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.name == payload.name).first()
    if role:
        raise HTTPException(status_code=400, detail="Role already exists")
    new_role = models.Role(name=payload.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

# READ ALL ROLES
@router.get("/", response_model=list[RoleResponse])
def get_roles(db: Session = Depends(get_db)):
    return db.query(models.Role).all()

# READ ROLE BY ID
@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

# UPDATE ROLE
@router.put("/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, payload: RoleCreate, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    role.name = payload.name
    db.commit()
    db.refresh(role)
    return role

# DELETE ROLE
@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    return None
