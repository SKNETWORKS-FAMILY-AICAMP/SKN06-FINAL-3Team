from pydantic import BaseModel
from typing import Optional
from datetime import date

class MyPageUpdate(BaseModel):
    phone: str 

class MyPageResponse(BaseModel):
    member_id: int
    phone: str 
    emp_no: str
    role: int
    name:str
    company_affiliation:str
    phone: str
    employment_status: str
    position: str
    department: str
    
    class Config:
        from_attributes = True
    
class MyPasswordUpdate(BaseModel):
    password: str
    new_password: str
    
class FavoriteRequest(BaseModel):
    scope: str
    favorite_type: str
    target_id: int
