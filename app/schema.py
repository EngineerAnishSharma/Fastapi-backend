from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime
    class Config:
        orm_mode = True
        
class Post(PostBase):
    id: int
    created_at:datetime
    owner_id: int
    owner: UserOut
    
    # pydantic model have idea of dict property but dont have idea of sqlalchemy model
    class Config:
        orm_mode =True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
        
class UserLogin(BaseModel):
    email: EmailStr
    password :str
        
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)