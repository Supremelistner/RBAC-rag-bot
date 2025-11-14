from pydantic import BaseModel, Field
from typing import Optional
class SignUpBody(BaseModel):
    username: str 
    role : str
    password: str
class LoginBody(BaseModel):
    username: str 
    password: str
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str

class InnerDB(BaseModel):
    username: str 
    role : str
    hashed_password: str
