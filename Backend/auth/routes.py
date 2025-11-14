from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict

from Backend.Model.user_model import SignUpBody, LoginBody, TokenResponse, InnerDB
from .auth_handler import get_password_hash, verify_password, create_access_token, decode_access_token
from .role_assigner import allowed_docs as allowed_collections_for_role

router = APIRouter(prefix="/auth", tags=["auth"])

_users_db: Dict[str, InnerDB] = {}


@router.post("/signup", response_model=dict)
def signup(payload: SignUpBody):
    username = payload.username
    if username in _users_db:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = get_password_hash(payload.password)
    user = InnerDB(username=username, hashed_password=hashed, role=payload.role)
    _users_db[username] = user
    return {"msg": f"user {username} created with role {payload.role}"}


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginBody):
    user = _users_db.get(payload.username)
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(subject=user.username, role=user.role)
    return TokenResponse(
    access_token=token,
    role=user.role,
    token_type="bearer"
)



security = HTTPBearer()

def get_current_user_role(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    data = decode_access_token(token)
    if not data or "sub" not in data:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return {"username": data["sub"], "role": data.get("role")}

@router.get("/me/collections")
def my_collections(user=Depends(get_current_user_role)):
    role = user["role"]
    collections = allowed_collections_for_role(role)
    return {"username": user["username"], "role": role, "allowed_collections": collections}
