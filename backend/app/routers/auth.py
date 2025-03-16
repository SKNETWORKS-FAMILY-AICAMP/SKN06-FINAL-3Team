import os
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import  OAuth2PasswordBearer, OAuth2PasswordRequestForm
from core.security import verify_password, create_access_token, decode_access_token
from sqlalchemy.orm import Session
from db.session import get_session
from schemas.response import BaseResponse
from schemas.member import MyPageResponse
from model import Member 

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    member = db.query(Member).filter(Member.emp_no == form_data.username).first()
    if not member:
        return BaseResponse(
            code=1,
            msg="아이디 또는 비밀번호를 확인해 주세요."
        )

    if not verify_password(form_data.password, member.password):
        return BaseResponse(code=1, msg="아이디 또는 비밀번호를 확인해 주세요.")

    me_data = MyPageResponse.model_validate(member, from_attributes=True)

    access_token = create_access_token(data=me_data.model_dump())
    
    db.commit()
    
    return BaseResponse(code=0, msg="로그인되었습니다.", result={"access_token": access_token, "token_type": "bearer"})

@router.get("/me")
def read_member_me(token: str= Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        
        return BaseResponse(result= payload, code= 0, msg='성공')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="아이디 또는 비밀번호를 확인해 주세요.")
    except jwt.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 토큰입니다.")