import os
import asyncio
import chromadb
import json
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentType, initialize_agent
from langchain.tools import tool
from langchain.schema import SystemMessage
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM_MODEL = "gpt-4"
COLLECTION_NAME_POST = "posts"
COLLECTION_NAME_BRAND = "brand"
COLLECTION_NAME_COSMETIC = "cosmetic"
COLLECTION_NAME_INGREDIENT = "ingredient"
COLLECTION_NAME_LAW = "law"

def get_fresh_llm():
    """매번 새로운 LLM 인스턴스를 생성하여 초기화"""
    return ChatOpenAI(model_name=LLM_MODEL, openai_api_key=OPENAI_API_KEY, temperature=0, cache=False)

embedding_function = OpenAIEmbeddings(
    base_url="https://76mqtyy2wie64y-10050.proxy.runpod.net/v1",
    model="multilingual-e5-large",
    api_key="team3",
    tiktoken_enabled=False,
    embedding_ctx_length=502
)

client = chromadb.HttpClient(host="3.35.104.197", port=10090)

collections = {
    "post": client.get_collection(COLLECTION_NAME_POST),
    "brand": client.get_collection(COLLECTION_NAME_BRAND),
    "cosmetic": client.get_collection(COLLECTION_NAME_COSMETIC),
    "ingredient": client.get_collection(COLLECTION_NAME_INGREDIENT),
    # "law": client.get_collection(COLLECTION_NAME_LAW),  # 일단 법률 쪽은 collection 안만듦! 추후 고도화 예정
}

classification_prompt = PromptTemplate(
    template="""당신은 아모레퍼시픽 전문가입니다. 다음 질문을 적절한 카테고리로 분류하세요.
    
    아모레퍼시픽의 자사브랜드: 
    카테고리: BEAUTY_CARE, 브랜드명(한글):설화수, 브랜드명(영어) sulwhasoo
    카테고리: BEAUTY_CARE, 브랜드명(한글):라네즈, 브랜드명(영어) laneige
    카테고리: BEAUTY_CARE, 브랜드명(한글):이니스프리, 브랜드명(영어) innisfree
    카테고리: BEAUTY_CARE, 브랜드명(한글):에이피뷰티, 브랜드명(영어) ap
    카테고리: BEAUTY_CARE, 브랜드명(한글):헤라, 브랜드명(영어) hera
    카테고리: BEAUTY_CARE, 브랜드명(한글):프리메라, 브랜드명(영어) primera
    카테고리: BEAUTY_CARE, 브랜드명(한글):아이오페, 브랜드명(영어) iope
    카테고리: BEAUTY_CARE, 브랜드명(한글):마몽드, 브랜드명(영어) mamonde
    카테고리: BEAUTY_CARE, 브랜드명(한글):한율, 브랜드명(영어) hanyul
    카테고리: MEDICAL_BEAUTY, 브랜드명(한글):에스트라, 브랜드명(영어) aestura
    카테고리: BEAUTY_CARE, 브랜드명(한글):에스쁘아, 브랜드명(영어) espoir
    카테고리: BEAUTY_CARE, 브랜드명(한글):에뛰드, 브랜드명(영어) etude
    카테고리: HAIR, 브랜드명(한글):려, 브랜드명(영어) ryo
    카테고리: HAIR, 브랜드명(한글):미쟝센, 브랜드명(영어) mise en scene
    카테고리: HAIR, 브랜드명(한글):라보에이치, 브랜드명(영어) laboh
    카테고리: HAIR, 브랜드명(한글):아윤채, 브랜드명(영어) ayunche
    카테고리: HAIR, 브랜드명(한글):아모스프로페셔널, 브랜드명(영어) amos professional
    카테고리: HAIR, 브랜드명(한글):롱테이크, 브랜드명(영어) longtake
    카테고리: BODY, 브랜드명(한글):일리윤, 브랜드명(영어) illiyoon
    카테고리: BODY, 브랜드명(한글):해피바스, 브랜드명(영어) happybath
    카테고리: BODY, 브랜드명(한글):스킨유, 브랜드명(영어) skin u
    카테고리: ORAL_CARE, 브랜드명(한글):메디안, 브랜드명(영어) median
    카테고리: ORAL_CARE, 브랜드명(한글):젠티스트, 브랜드명(영어) gentist
    카테고리: PERFUME, 브랜드명(한글):구딸, 브랜드명(영어) goutal
    카테고리: INNER_BEAUTY, 브랜드명(한글):바이탈뷰티, 브랜드명(영어) vital beauty
    카테고리: TEA_CULTURE, 브랜드명(한글):오설록, 브랜드명(영어) osulloc
    카테고리: BEAUTY_DEVICE, 브랜드명(한글):메이크온, 브랜드명(영어) makeon
    카테고리: BEAUTY_CARE, 브랜드명(한글):오딧세이, 브랜드명(영어) odyssey
    카테고리: BEAUTY_CARE, 브랜드명(한글):비레디, 브랜드명(영어) bready
    카테고리: BEAUTY_CARE, 브랜드명(한글):홀리추얼, 브랜드명(영어) holitual

    질문: "{question}"
    
    가능한 카테고리:
    - "ingredient" (성분, 화장품 기능 관련 질문)
    - "amore_cosmetic" (자사 화장품 검색 질문)
    - "other_cosmetic" (타사 화장품 검색 질문)
    - "cosmetic" (브랜드 구별 없이 화장품에 관한 질문질문)
    - "company" (회사 전반적인 질문)
    - "news" (최신 뉴스나 기사 관련 질문)

    반드시 위의 카테고리 중 하나만 출력하세요.
    
    카테고리:""",
    input_variables=["question"],
)

@tool
def classify_question(question: str) -> str:
    """질문을 적절한 카테고리로 분류합니다."""
    llm = get_fresh_llm() 
    response = llm.invoke(classification_prompt.format(question=question))
    return response.content.strip().replace('"', '')

@tool
def multi_collection_retriever(input_data: str) -> str:
    """
    사용자의 질문을 기반으로 적절한 ChromaDB 컬렉션에서 검색 후 JSON 형식의 결과를 반환합니다.
    input_data는 JSON 문자열이며, 'query'와 'category'를 포함해야 합니다.
    """
    data = json.loads(input_data) 
    query = data["query"]
    category = data["category"]  

    retrieved_docs = {} 
    query_embedding = embedding_function.embed_query(query)

    search_collections = []
    metadata_filter = None 

    if category == "ingredient":
        search_collections = ["ingredient", "cosmetic"]
    elif category == "amore_cosmetic":
        search_collections = ["cosmetic"]
        metadata_filter = {"scope": "자사"}
    elif category == "other_cosmetic":
        search_collections = ["cosmetic"]
        metadata_filter = {"scope": "타사"} 
    elif category == "cosmetic":
        search_collections = ["cosmetic", "ingredient"] 
    elif category == "company":
        search_collections = ["brand", "posts"]
    elif category == "news":
        search_collections = ["posts"]

    for collection_name in search_collections:
        if metadata_filter:
            results = collections[collection_name].query(
                query_embeddings=[query_embedding], 
                n_results=5,
                where=metadata_filter 
            )
        else:
            results = collections[collection_name].query(
                query_embeddings=[query_embedding], 
                n_results=5
            )

        retrieved_docs[collection_name] = [
            {"content": results['documents'][0][i], "metadata": results['metadatas'][0][i]}
            for i in range(len(results['ids'][0]))
        ]

    return json.dumps(retrieved_docs, ensure_ascii=False)

response_prompt = PromptTemplate(
    template="""당신은 아모레퍼시픽 전문가입니다.

    질문: {question}

    아래 정보를 참고하여 답변을 생성하세요.

    {context}

    답변:""",
    input_variables=["question", "context"],
)

@tool
def generate_response(input_data: str) -> str:
    """
    검색된 데이터를 바탕으로 LLM이 최종 응답을 생성합니다.
    input_data는 JSON 형식으로 전달되며, 'question'과 'retrieved_docs'를 포함합니다.
    """
    llm = get_fresh_llm() 
    data = json.loads(input_data)
    question = data["question"]
    retrieved_docs = data["retrieved_docs"]

    context_sections = []
    for collection_name, docs in retrieved_docs.items():
        if docs:
            doc_texts = "\n".join([doc["content"] for doc in docs])
            context_sections.append(f"### {collection_name.upper()} 관련 정보 ###\n{doc_texts}")

    context = "\n\n".join(context_sections)[:7000]

    response = llm.invoke(response_prompt.format(question=question, context=context))
    return response.content.strip()

tools = [classify_question, multi_collection_retriever, generate_response]

agent = initialize_agent(
    tools=tools,
    llm=get_fresh_llm(), 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def agentic_rag_chain(question: str):
    category = classify_question(question) 
    retrieved_docs = multi_collection_retriever(json.dumps({"query": question, "category": category}, ensure_ascii=False)) 
    response = generate_response(json.dumps({"question": question, "retrieved_docs": json.loads(retrieved_docs)}, ensure_ascii=False))

    return {
        "question": question,
        "category": category,
        "response": response,
        "retrieved_docs": json.loads(retrieved_docs)
    }


class AISearch:
    @staticmethod
    async def search(question: str):
        llm = ChatOpenAI(model=LLM_MODEL, openai_api_key=OPENAI_API_KEY, model_kwargs={"stream": True})
        
        async for chunk in llm.astream(question):
            if chunk.content:
                yield chunk.content  
            await asyncio.sleep(0.1)
    

class IntegrationSearch:
    @staticmethod
    async def search(question: str):
        response = agentic_rag_chain(question)

        for chunk in response.split(" "):
            yield chunk + " "
            await asyncio.sleep(0.1)