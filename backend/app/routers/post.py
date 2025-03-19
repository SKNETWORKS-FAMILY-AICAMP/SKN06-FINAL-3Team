from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from db.connection import get_connection 
from schemas.response import BaseResponse, ListResponse
from fastapi.security import  OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()
            
@router.get("/internal")
def get_boards(
    post_type: str = Query(None), 
    post_ctgry: Optional[str] = Query(None), 
    query: Optional[str] = Query(None), 
    current_page: Optional[int] = Query(1), 
    item_per_page: Optional[int] = Query(8)
):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            # BRAND 유형의 게시글 조회
            if post_type == "BRAND":
                sql = "SELECT * FROM brand WHERE brand_kor != '아모레퍼시픽'"
                params = []

                if post_ctgry:
                    sql += " AND brand_ctgry = %s"
                    params.append(post_ctgry)

                cursor.execute(sql, params)
                brands = cursor.fetchall()

                return BaseResponse(code=0, msg="조회 성공", result=brands)

            # 일반 게시글 (post) 조회
            else:
                sql = ''
                if post_type=='NEWS':
                    sql += """
                    SELECT p.*, pi.image_url,
                        CASE 
                            WHEN f.target_id IS NOT NULL THEN 1 
                            ELSE 0 
                        END AS is_favorite
                    FROM post p
                    LEFT JOIN post_image pi ON p.post_id = pi.post_id AND pi.image_type = 'THUMBNAIL'
                    LEFT JOIN (SELECT target_id FROM favorites WHERE scope = 'INTERNAL' AND favorite_type = 'NEWS') f ON p.post_id = f.target_id 
                    WHERE 1=1
                    """
                elif post_type=='REPORT':
                    sql += """
                    SELECT p.post_ctgry, p.post_id, p.post_type, p.title, p.created_at, company_id,
                        d.original_file_url, d.summary as summary,
                        CASE 
                            WHEN f.target_id IS NOT NULL THEN 1 
                            ELSE 0 
                        END AS is_favorite
                    FROM post p 
                    LEFT JOIN document d ON p.document_id = d.document_id 
                    LEFT JOIN (SELECT target_id FROM favorites WHERE scope = 'INTERNAL' AND favorite_type = 'REPORT') f ON p.post_id = f.target_id 
                    WHERE 1=1
                    """
                else:
                    sql = "SELECT * FROM post WHERE 1=1 JOIN (SELECT target_id FROM favorites WHERE scope='INTERNAL' AND favorite_type != 'NEWS' AND favorite_type != 'JOURNAL') ON post.post_id = favorites.target_id  "
                    
                count_sql = "SELECT COUNT(*) FROM post WHERE 1=1"
                params = []

                if post_type:
                    sql += " AND post_type = %s"
                    count_sql += " AND post_type = %s"
                    params.append(post_type)

                if post_ctgry:
                    sql += " AND p.post_ctgry = %s"
                    count_sql += " AND post_ctgry = %s"
                    params.append(post_ctgry)

                if query:
                    sql += " AND (title LIKE %s OR content LIKE %s)"
                    count_sql += " AND (title LIKE %s OR content LIKE %s)"
                    params.extend([f"%{query}%", f"%{query}%"])
                
                cursor.execute(count_sql, params) 
                total_count = cursor.fetchone()["COUNT(*)"]

                sql += " ORDER BY p.created_at DESC"
                
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

    return ListResponse(code=1, msg="조회 실패")



@router.get("/external")
def get_external_boards(
    post_type: str = Query(None), 
    source_name: Optional[str] = Query(None), 
    query: Optional[str] = Query(None), 
    current_page: int = Query(1), 
    item_per_page: int = Query(10)
):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            
            sql=''
            params = []
            count_sql = "SELECT COUNT(*) FROM post_external WHERE 1=1"
            
            if post_type =='JOURNAL':
                sql = """
                    SELECT post_external.*,
                        CASE 
                            WHEN f.target_id IS NOT NULL THEN 1 
                            ELSE 0 
                        END AS is_favorite
                    FROM post_external
                    LEFT JOIN document ON post_external.document_id = document.document_id 
                    JOIN (SELECT target_id FROM favorites WHERE scope = 'EXTERNAL' AND favorite_type = 'JOURNAL') f ON post_external.post_id = f.target_id 
                    WHERE 1=1
                """
            elif post_type == 'NEWS':
                sql = """
                    SELECT post_external.*,
                        CASE 
                            WHEN f.target_id IS NOT NULL THEN 1 
                            ELSE 0 
                        END AS is_favorite
                    FROM post_external
                    LEFT JOIN (SELECT target_id FROM favorites WHERE scope = 'EXTERNAL' AND favorite_type = 'NEWS') f ON post_external.post_id = f.target_id 
                    WHERE 1=1
                """
                
            if post_type:
                sql += " AND post_type = %s"
                count_sql += " AND post_type = %s"
                params.append(post_type)

            if source_name:
                sql += " AND source_name = %s"
                count_sql += " AND source_name = %s"
                params.append(source_name)

            if query:
                sql += " AND (title LIKE %s OR content LIKE %s)"
                count_sql += " AND (title LIKE %s OR content LIKE %s)"
                params.extend([f"%{query}%", f"%{query}%"])
            
            cursor.execute(count_sql, params) 
            total_count = cursor.fetchone()["COUNT(*)"]

            sql += " ORDER BY post_external.created_at DESC"
            
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
