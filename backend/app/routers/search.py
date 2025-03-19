from fastapi import APIRouter, Query
from typing import Optional
from db.connection import get_connection 
from schemas.response import BaseResponse
from fastapi.responses import StreamingResponse
from core.llm import AISearch, IntegrationSearch

import asyncio
router = APIRouter()

@router.get("/brand")
async def search_brand(brand_kor:str, query: str ):
    try:
        question = rf"""
            너는 아모레퍼시픽의 전문 AI 컨설턴트입니다. 나는 아모레퍼시픽 직원입니다.
            {brand_kor}에 대해서 질문할 내용이 있습니다. {query}. 

            대답을 할 때에는:
            - **소개는 생략**해 주세요.
            - **모든 줄바꿈(`\n`)을 반드시 `<br/>`로 변환**해 주세요. 
            - `\n`이 **1개일 때는 `<br/>` 1개**,  
            - `\n`이 **2개 연속되면 `<br/><br/>`**,  
            - **연속된 개수만큼 `<br/>`을 삽입해야 합니다.**
            - **굵게 강조할 부분은 `<b></b>`로 감싸 주세요.**
            - **`"`(큰따옴표)와 `\`(백슬래시) 등의 특수 문자가 포함되지 않도록 해주세요.**

            **🚨 중요: 절대 `\n`이 포함되지 않도록 하세요.** 반드시 `<br/>`만을 사용해야 합니다.
        """
        return StreamingResponse(AISearch.search(question), media_type="text/plain")
    
    except:
        return BaseResponse(code=1, msg="조회 실패")
    
    
@router.get("/ai")
async def search_ai(query: str):
    """FastAPI 엔드포인트: AI 검색 실행"""
    try:
        return StreamingResponse(IntegrationSearch.search(query), media_type="application/json")

    except Exception as e:
        return BaseResponse(code=1, msg="조회 실패")
    
    