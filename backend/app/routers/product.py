from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from db.connection import get_connection 
from schemas.response import BaseResponse, ListResponse
from fastapi.security import  OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

@router.get("/products")
def get_products(
    scope: str = Query(None), 
    brand: Optional[str] = Query(None), 
    brand_ids: Any = Query(None),
    category_1: Optional[str] = Query(None), 
    query: Optional[str] = Query(None), 
    current_page: int = Query(1), 
    item_per_page: int = Query(12)
):
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            sql = ''
            count_sql = ''
            
            if scope == "INTERNAL":
                sql += """
                    SELECT cosmetic.*, brand.brand_kor as brand_kor,  
                        CASE 
                            WHEN f.target_id IS NOT NULL THEN 1 
                            ELSE 0 
                        END AS is_favorite
                    FROM cosmetic 
                    JOIN brand ON cosmetic.brand_id = brand.brand_id 
                    LEFT JOIN 
                        (SELECT * FROM favorites WHERE scope = 'INTERNAL' AND favorite_type = 'COSMETIC') f
                    ON f.target_id = cosmetic.cosmetic_id 
                    WHERE 1=1
                """
                count_sql += "SELECT COUNT(*) FROM cosmetic WHERE 1=1"
                params = []
                
                if brand_ids is not None and brand_ids != "":  
                    brand_id = list(map(int, brand_ids.split(","))) 
                    sql += " AND cosmetic.brand_id IN (" + ",".join(["%s"] * len(brand_id)) + ")"
                    count_sql += " AND cosmetic.brand_id IN (" + ",".join(["%s"] * len(brand_id)) + ")"
                    params.extend(brand_id)


            else:
                sql += "SELECT * from cosmetic_external WHERE 1=1"
                count_sql = "SELECT COUNT(*) FROM cosmetic_external WHERE 1=1"
                params = []
                
                if brand:
                    sql += " AND brand = %s"
                    count_sql += " AND brand = %s"
                    params.append(brand)
            
            if category_1:
                sql += " AND category_1 = %s"
                count_sql += " AND category_1 = %s"
                params.append(category_1)

            if query:
                sql += " AND (title LIKE %s OR content LIKE %s)"
                count_sql += " AND (title LIKE %s OR content LIKE %s)"
                params.extend([f"%{query}%", f"%{query}%"])
            
            cursor.execute(count_sql, params) 
            total_count = cursor.fetchone()["COUNT(*)"]

            if scope == "INTERNAL":
                if brand_ids is not None and brand_ids != "": 
                    sql += f" ORDER BY FIELD(cosmetic.brand_id, {brand_ids}), product_name "
                else:  
                    sql += f" ORDER BY cosmetic.product_name, cosmetic.created_at DESC"
            else : 
                sql += " ORDER BY product_name, created_at DESC"

            
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
