from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class MemberUpdate(BaseModel):
    member_id: int
    name: Optional[str] = None
    phone: Optional[str] = None
    company_affiliation: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    employment_status: Optional[str] = None
    role: Optional[int] = None
    birth_date: Optional[date] = None
    hire_date: Optional[date] = None
    resign_date: Optional[date] = None
    resign_reason: Optional[str] = None
    password: Optional[str] = None

class MemberCreate(BaseModel):
    name: str
    emp_no: str
    phone: str
    company_affiliation: str
    department: str
    position: str
    employment_status: str
    role: int
    birth_date: date
    hire_date: date
    password: str
    
class MembersResponse(MemberCreate):
    created_at: datetime

    class Config:
        from_attributes = True

