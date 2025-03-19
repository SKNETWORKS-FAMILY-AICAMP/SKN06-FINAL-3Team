import os
import chromadb
import numpy as np
import aiomysql
import asyncio
import json
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.tools import tool
from langchain_core.messages import SystemMessage
from collections import defaultdict
from typing import AsyncGenerator
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = "Qwen2.5-72B-Instruct"

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": 3306,
    "user": os.getenv("DB_USER"),  
    "password": os.getenv("DB_PASSWD"),
    "db": os.getenv("DB_NAME"),
    "autocommit": True,
}

client = chromadb.HttpClient(host="3.35.104.197", port=10090)

embedding_function = OpenAIEmbeddings(
    base_url="https://76mqtyy2wie64y-10050.proxy.runpod.net/v1",
    model="multilingual-e5-large",
    api_key="team3",
    tiktoken_enabled=False,
    embedding_ctx_length=502
)

ingredient_store = client.get_collection('ingredient')
cosmetic_store = client.get_collection('cosmetic')
brand_store = client.get_collection('brand')
post_store = client.get_collection('posts')

def convert_datetime(obj):
    """datetime 객체를 ISO 포맷 문자열로 변환"""
    if isinstance(obj, datetime):
        return obj.isoformat() 
    raise TypeError("Type not serializable")


def get_fresh_llm():   # gpt-4-turbo 써야 함! gpt-4 쓰니깐 multi로 tool을 쓰지 못함!
    # return ChatOpenAI(model_name=LLM_MODEL,  openai_api_key=OPENAI_API_KEY, temperature=0, cache=False)
    return ChatOpenAI(base_url="https://huyl3xwudrm8sq-10050.proxy.runpod.net/v1", model=LLM_MODEL,api_key="team3", temperature=0, cache=False)
                      
@tool
def retrieve_ingredient(query: str, k: int = 5):
    """
    화장품 성분 정보를 검색하는 도구. 특정 성분의 효능, 사용 가능 여부, 피부 타입에 따른 추천 정보를 제공합니다.
    "예: '미백 효과가 있는 성분은?', '지성 피부에 좋은 성분 추천해줘', '자외선 차단 성분 알려줘'
    """
    try:
        query_embedding = embedding_function.embed_query(query)
        
        results = ingredient_store.query(query_embeddings=query_embedding, n_results=k)
        return results if results['documents'] else "관련 정보를 찾을 수 없습니다."
    except Exception as e:
        return f"Error retrieving ingredients: {str(e)}"

@tool
def retrieve_cosmetic(query: str, k: int = 3):
    """
    화장품 제품 정보를 검색하는 도구. 특정 기능, 브랜드, 피부 타입에 따라 적절한 화장품을 소개합니다.
    자사 브랜드 화장품인지 타사 브랜드의 화장품인지 구분하여 요구한 것이 아니라면 아모레퍼시픽의 자사브랜드 제품을 우선적으로 소개합니다.
    예: '미백 효과가 있는 화장품 추천해줘', '여드름 피부에 좋은 제품 3개 알려줘', '자사 브랜드 제품 소개해줘'
    """
    try:
        query_embedding = embedding_function.embed_query(query)
        
        results = cosmetic_store.query(query_embeddings=query_embedding, n_results=k)
        return results if results['documents'] else "관련 정보를 찾을 수 없습니다."
    except Exception as e:
        return f"Error retrieving products: {str(e)}"

@tool
def retrieve_brand(query: str, k: int = 5):
    """
    화장품 브랜드 정보를 검색하는 도구. 브랜드의 특징, 주요 제품, 철학(예: 비건, 유기농 등)을 제공합니다.
    예: '이니스프리 브랜드 스토리 알려줘', '비건 화장품 브랜드 추천해줘', '헤어 관련 자사 브랜드 알려줘'
    """
    try:
        query_embedding = embedding_function.embed_query(query)
        
        results = brand_store.query(query_embeddings=query_embedding, n_results=k)
        return results if results['documents'] else "관련 정보를 찾을 수 없습니다."
    except Exception as e:
        return f"Error retrieving brands: {str(e)}"

@tool
def retrieve_posts(query: str, k: int = 5):
    """
    최근 화장품 관련 뉴스, 회사 문서, 회사 소식, 트렌드, 연구 논문을 검색하는 도구. 뷰티 업계 최신 소식을 제공합니다. 
    예: '최근 트렌드인 화장품 성분이 뭐야?', '회사 경영실적에 대해 알려줘', '최근 회사 소식에 대해 알려줘', '화장품 관련 연구 논문 2개 찾아줘', '친환경 화장품 트렌드 기사 알려줘'
    """
    try:
        query_embedding = embedding_function.embed_query(query)
        
        results = post_store.query(query_embeddings=query_embedding, n_results=k)
        return results if results['documents'] else "관련 정보를 찾을 수 없습니다."
    except Exception as e:
        return f"Error retrieving posts: {str(e)}"

tool_list = [retrieve_ingredient, retrieve_cosmetic, retrieve_brand, retrieve_posts] 

async def get_retrieved_documents(query: str):
    """LLM과 도구 호출을 비동기적으로 처리하는 함수"""
    messages = [ 
        SystemMessage(content="Analyze the user's query and call **all relevant tools** simultaneously. "
                        "For example, if the user asks for cosmetic, ingredients and research papers, "
                        "you must invoke all the tools at once."),
        HumanMessage(query)
    ]
    
    llm = get_fresh_llm()
    llm_with_tools = llm.bind_tools(tools=tool_list, tool_choice="auto")
    
    if asyncio.iscoroutinefunction(llm_with_tools.invoke):
        ai_msg = await llm_with_tools.invoke(messages)
    else:
        ai_msg = llm_with_tools.invoke(messages)

    tool_outputs = []
    tool_dict = {
        "retrieve_ingredient": retrieve_ingredient,
        "retrieve_cosmetic": retrieve_cosmetic,
        "retrieve_brand": retrieve_brand,
        "retrieve_posts": retrieve_posts
    }
    
    print('⭕ TOOL 개수:', len(ai_msg.tool_calls))
    
    if hasattr(ai_msg, "tool_calls") and ai_msg.tool_calls:
        tasks = []
        for tool_call in ai_msg.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            if tool_name in tool_dict:
                selected_tool = tool_dict[tool_name]

                if asyncio.iscoroutinefunction(selected_tool.invoke):
                    print('비동기')
                    tasks.append(asyncio.create_task(selected_tool.invoke(input=tool_args)))
                else:
                    tool_output = selected_tool.invoke(input=tool_args)
                    tool_outputs.append({"tool_name": tool_name, "output": tool_output})
        

        if tasks:
            results = await asyncio.gather(*tasks)
            for idx, tool_call in enumerate(ai_msg.tool_calls):
                tool_name = tool_call["name"]
                tool_outputs.append({"tool_name": tool_name, "output": results[idx]})
                
    print('⭕ Retrieved 완료')
    return tool_outputs

def generate_context(doc_datas, max_tokens=500):
    """
    검색된 데이터를 정리하여 LLM이 사용할 수 있도록 컨텍스트를 생성하는 함수.

    Parameters:
    - doc_datas (list of dict): (각 항목에 'distance'와 'document' 포함)
    - max_tokens (int): 최대 허용 토큰 수 (기본값 500)

    Returns:
    - final_context (str): 정제된 컨텍스트 문자열
    """
    sorted_data = sorted(doc_datas, key=lambda x: x['distance'])
    
    all_texts = [item['document'] for item in sorted_data]
    full_context = "\n\n".join(all_texts)

    words = full_context.split() 
    if len(words) > max_tokens:
        trimmed_context = " ".join(words[:max_tokens])
    else:
        trimmed_context = full_context

    return trimmed_context

def create_prompt(context, question):
    """
    LLM을 위한 프롬프트를 생성하는 함수.
    
    Parameters:
    - context (str): 정제된 데이터 컨텍스트
    - question (str): 사용자가 물어보는 질문
    
    Returns:
    - prompt (str): LLM을 호출할 최적의 프롬프트
    """
    
    prompt_template = rf"""당신은 아모레퍼시픽 회사의 직원들을 도와주는 전문 비서로서 이름은 AmoreSearch 입니다. 아래 제공된 정보를 참조하여 질문에 답변해 주세요.

    답변시 **절대 중국어로 답변하지 마세요. Do not answer in Chinese or Japanese**

    
    --- [ context ] ---
    {context}
    --------------------

    위 정보를 기반으로 전문가처럼 정확하고 상세하게 답변해 주세요.
    한국어와 영어 외에는 사용하지 말아주세요.

    question:
    {question}    
     """
    
    return prompt_template

async def query_mariadb(query, params=None):
    """
    비동기적으로 MariaDB 쿼리를 실행하고 결과를 반환하는 함수
    """
    result = []
    
    try:
       
        async with aiomysql.connect(**DB_CONFIG) as conn:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                if params is None:
                    params = ()
                
                await cur.execute(query, params)
                result = await cur.fetchall()

        return result if result else [] 

    except aiomysql.Error as e:
        print(f"[MariaDB 에러]: {e}")
        return []
    

async def fetch_mariadb_data(retrieved_collections_docs):
    ingredient_ids = []
    cosmetic_queries = defaultdict(list)
    post_queries = defaultdict(list)

    for collection in retrieved_collections_docs:
        tool_name = collection.get('tool_name')
        metadatas = collection.get('output', {}).get('metadatas', [[]])[0]

        if tool_name == "retrieve_ingredient":
            for meta in metadatas:
                ingredient_id = meta.get('ingred_id')
                if ingredient_id is not None:
                    ingredient_ids.append(int(ingredient_id))
        
        elif tool_name == "retrieve_cosmetic":
            for meta in metadatas:
                scope = meta.get('scope')
                cosmetic_id = meta.get('cosmetic_id')
                if scope and cosmetic_id is not None:
                    cosmetic_queries[scope].append(int(cosmetic_id))
        
        elif tool_name == "retrieve_posts":
            for meta in metadatas:
                scope = meta.get('scope')
                post_id = meta.get('post_id')
                if scope and post_id is not None:
                    post_queries[scope].append(int(post_id))


    ingredient_results = []
    if ingredient_ids:
        ingredient_placeholders = ",".join(["%s"] * len(ingredient_ids))
        ingredient_results = await query_mariadb(
            f"SELECT * FROM ingredient WHERE ingred_id IN ({ingredient_placeholders})",
            tuple(ingredient_ids)
        )
    cosmetic_results = {}
    for scope, cosmetic_ids in cosmetic_queries.items():
        if not cosmetic_ids:
            continue

        table_name = "cosmetic" if scope == '자사' else "cosmetic_external"
        cosmetic_placeholders = ",".join(["%s"] * len(cosmetic_ids))
        cosmetic_results[scope] = await query_mariadb(
            f"SELECT * FROM {table_name} WHERE cosmetic_id IN ({cosmetic_placeholders})",
            tuple(cosmetic_ids)
        )

    post_results = {}
    for scope, post_ids in post_queries.items():
        if not post_ids:
            continue

        table_name = "post" if scope == 'INTERNAL' else "post_external"
        post_placeholders = ",".join(["%s"] * len(post_ids))
        post_results[scope] = await query_mariadb(
            f"SELECT * FROM {table_name} WHERE post_id IN ({post_placeholders})",
            tuple(post_ids)
        )
        
    print('⭕ MariaDB 조회완료')
    
    return {
        "ingredient": ingredient_results,
        "cosmetic": cosmetic_results,
        "post": post_results
    }
        
async def generate_llm_response(query, retrieved_collections_docs):
    """
    LLM을 호출하여 응답을 생성하는 함수 (비동기)
    """
    try:
        flatten_docs = []
        for collection in retrieved_collections_docs:
            distances = collection.get('output', {}).get('distances', [[]])[0]
            documents = collection.get('output', {}).get('documents', [[]])[0]

            for index in range(len(distances)):
                flatten_docs.append({
                    'distance': distances[index],
                    'document': documents[index]
                })

        flatten_docs = sorted(flatten_docs, key=lambda x: x["distance"])

        max_token_limit = 7000
        context = generate_context(flatten_docs, max_token_limit)

        prompt = create_prompt(context, query)

        llm_init = get_fresh_llm()
        async for llm_output in llm_init.astream(prompt):
            yield llm_output 

    except Exception as e:
        print(f"❌ LLM 응답 오류: {e}")
        yield json.dumps({"error": "LLM 응답 생성 중 오류 발생"}, ensure_ascii=False) + "\n"

def relateive_posts(query: str, k: int = 5):
    """
    최근 화장품 관련 뉴스, 트렌드, 연구 논문을 검색하는 도구. 뷰티 업계 최신 소식을 제공합니다. 
    예: '최근 트렌드인 화장품 성분이 뭐야?', '화장품 관련 연구 논문 2개 찾아줘', '친환경 화장품 트렌드 기사 알려줘'
    """
    try:
        query_embedding = embedding_function.embed_query(query) 
        
        results = post_store.query(query_embeddings=query_embedding, n_results=k) 
        print('⭕ post 조회완료')
        
        return results if results['documents'] else "관련 정보를 찾을 수 없습니다."
    except Exception as e:
        return f"Error retrieving posts: {str(e)}"
    
class IntegrationSearch:
    @staticmethod
    async def search(query: str) -> AsyncGenerator[str, None]:
        """AI 검색 기능을 실행하고 JSON 데이터를 스트리밍 형식으로 반환하는 비동기 제너레이터"""
        try:
            retrieved_collections_docs = await get_retrieved_documents(query)

            metadata_response = await fetch_mariadb_data(retrieved_collections_docs)
            yield json.dumps({"type": "metadata", "data": metadata_response}, ensure_ascii=False, default=convert_datetime) + "\n"
            
            async for llm_output in generate_llm_response(query, retrieved_collections_docs):
                yield json.dumps({"type": "message", "data": llm_output.content}, ensure_ascii=False) + "\n"
                await asyncio.sleep(0.05)

        except Exception as e:
            print(f"전체 시스템 오류 발생: {e}")
            yield json.dumps({"type": "error", "message": "서버 오류 발생"}, ensure_ascii=False) + "\n"
            
            
class AISearch:
    @staticmethod
    async def search(question: str):
        llm = ChatOpenAI(model=LLM_MODEL, openai_api_key=OPENAI_API_KEY, model_kwargs={"stream": True})
        
        async for chunk in llm.astream(question):
            if chunk.content:
                yield chunk.content  
            else:
                break  

            await asyncio.sleep(0.1)
        
        return 
    
