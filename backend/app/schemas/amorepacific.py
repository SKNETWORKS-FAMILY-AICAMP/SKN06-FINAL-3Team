from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class PagingModel(BaseModel):
    current_page: Optional[int] = None
    item_per_page: Optional[int] = None

class BrandRequest(PagingModel):
    brand_ctgry: Optional[str] = None

class BrandResponse(BaseModel):
    brand_id: int
    brand_ctgry: str
    brand_kor: str
    brand_eng: str
    brand_subtitle: Optional[str] = None
    image_url: Optional[str] = None
    ceo: Optional[str] = None
    company_id: Optional[int] = None
    brand_site_url: Optional[str] = None
    founded_year: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
    