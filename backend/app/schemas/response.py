from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T") 

class BaseResponse(BaseModel, Generic[T]):
    msg: str = "성공"  
    code: int = 0      
    result: Optional[T] = None  
    
    class Config:
        from_attributes = True 
         
class ListResponse(BaseResponse, Generic[T]):
    paging: Optional[T] = None  

    class Config:
        from_attributes = True  
