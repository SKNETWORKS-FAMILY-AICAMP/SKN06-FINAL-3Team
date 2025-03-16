from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db.session import get_session 
from db.connection import get_connection 
from schemas.response import BaseResponse, ListResponse
from schemas.admin import  MemberCreate, MemberUpdate
from core.security import hash_password, decode_access_token
from model import Member 
from fastapi.security import  OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter()

# 회원 생성
@router.post("/member")
def add_member(
    member: MemberCreate, 
    token: str= Depends(oauth2_scheme),
    db: Session = Depends(get_session)
    ):
    user = decode_access_token(token)
    if user.get("role") < 2 or user.get('department') != 'HR':
        return BaseResponse(code=1, msg="권한 없음")
    try:
        new_member = Member(
            name=member.name,
            emp_no=member.emp_no,
            phone=member.phone,
            company_affiliation=member.company_affiliation,
            position=member.position,
            employment_status=member.employment_status,
            department=member.department,
            role=member.role,
            birth_date=member.birth_date,
            hire_date=member.hire_date,
            password= hash_password(member.password)
        )

        db.add(new_member)
        db.commit()
        db.refresh(new_member)

        return BaseResponse(code=0, msg="등록되었습니다.")
          
    except IntegrityError as e:
        db.rollback()  
        return BaseResponse(code=1, msg="이미 등록된 사원번호입니다.")

    except Exception as e:
        db.rollback() 
        return BaseResponse(code=9, msg="서버 오류 발생")


# 회원 수정
@router.put("/member")
def update_member(
    member: MemberUpdate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_session)
):
    user = decode_access_token(token)
    if user.get("role") < 2 or user.get('department') != 'HR':
        return BaseResponse(code=1, msg="권한 없음")

    db_member = db.query(Member).filter(Member.member_id == member.member_id).first()
    if not db_member:
        return BaseResponse(code=1, msg="회원 정보가 없습니다.")

    update_data = member.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if(key =='password'):
            setattr(db_member, key, hash_password(value))
        else:
            setattr(db_member, key, value)
    
    try:
        db.commit()
        db.refresh(db_member)
        return BaseResponse(code=0, msg="수정되었습니다.")
    
    except IntegrityError:
        db.rollback()
        return BaseResponse(code=9, msg="서버 오류 발생")

    except Exception as e:
        db.rollback()
        return BaseResponse(code=9, msg="서버 오류 발생")

# 모든 회원 조회
@router.get("/members",)
def get_members(
    employment_status: str,
    current_page: int = Query(1), 
    item_per_page: int = Query(12),
    token: str= Depends(oauth2_scheme),
):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            member = decode_access_token(token)
            
            if member.get('role') < 2 or member.get('department') != 'HR':
                return BaseResponse(
                    code=0,
                    msg="권한 없음",
                )
            sql = "SELECT * FROM member WHERE role != 3"
            count_sql = "SELECT COUNT(*) FROM member WHERE role != 3"
            params = []
            
            if employment_status == '':
                sql += " AND employment_status != '퇴직'"
                count_sql += " AND employment_status != '퇴직'"
            else:
                sql += " AND employment_status =  %s"
                count_sql += " AND employment_status = %s"
                params.append(employment_status)
                
            cursor.execute(count_sql, params) 
            total_count = cursor.fetchone()["COUNT(*)"]

            sql += " ORDER BY created_at DESC"
            
            offset = (current_page - 1) * item_per_page
            sql += " LIMIT %s OFFSET %s"
            params.extend([item_per_page, offset])

            cursor.execute(sql, params)
            result = cursor.fetchall()

            return ListResponse(
                code=0,
                msg="조회 성공",
                result=result,
                paging={
                    "total_rows": total_count,
                    "current_page": current_page,
                }
            )
    finally:
        conn.close()

    return BaseResponse(code=1, msg="조회 실패")
