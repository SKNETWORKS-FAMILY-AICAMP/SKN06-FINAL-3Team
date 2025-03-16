# 🔎 AmoreSearch
> AmoreSearch는 sLLM을 기반으로 아모레퍼시픽에서 사용할 수 있는 사내 검색 시스템입니다. 

## 📅 프로젝트 기간
📆 2025.01.20 ~ 2025.03.20 

## 👥 팀원 소개
| 역할 | 이름 | GitHub | 담당 업무 |
|------|------|--------|----------|
| 팀원 | 박서윤 | [GitHub](https://github.com/Se0y00n) | |
| 팀원 | 박유나 | [GitHub](https://github.com/yunazz) | |
| 팀장 | 유경상 | [GitHub](https://github.com/kyungsangYu) |  |
| 팀원 | 장예린 | [GitHub](https://github.com/yerin7797) |  |

## 📚 프로젝트 개요
- **목적**: 본 프로젝트의 핵심 목표는 sLLM을 개발하고 파인튜닝하여 최적화된 검색 경험을 제공하는 것입니다.
- **기술 스택**: Nuxt.js, FastAPI, MariaDB, ChromaDB
    - Frontend: Nuxt.js
    - Backend: FastAPI
    - Database: MariaDB, ChromaDB
    - LLM, Embedding Model Deployment: RunPod (llm - '미정', embedding - 'multilingual-e5-large')
    - Server Infrastructure: AWS EC2, S3

- **주요 기능**:

## 📂 디렉토리 구조

```bash
🔎 AmoreSearch
├── 📂 documents           # 산출물
│── 📂 frontend            # 프론트엔드 프로젝트 (Nuxt.js)
│   ├── 📂 assets           # 정적 파일 (이미지, 폰트 등)
│   ├── 📂 components       # 재사용 가능한 Vue 컴포넌트
│   ├── 📂 composables      # Composition API 관련 유틸리티
│   ├── 📂 layouts          # 페이지 레이아웃
│   ├── 📂 middleware       # 미들웨어 인증 관련 로직
│   ├── 📂 pages            # 주요 페이지 파일
│   │   ├── 📂 admin       # 관리자 페이지
│   ├── 📂 plugins         # Vue 플러그인 설정
│   ├── 📂 public          # 정적 파일 (favicon, robots.txt 등)
│   ├── 📂 utils           # 유틸리티 함수 및 설정 파일
│   ├── app.vue          # 메인 Vue 앱 엔트리 파일
│   ├── nuxt.config.ts   # Nuxt.js 설정 파일
│   ├── package.json     # 프로젝트 의존성 및 설정
│
├── 📂 backend             # 백엔드 (FastAPI)
│   ├── 📂 app
│   │   ├── 📂 core          # 핵심 로직 (LLM, 벡터스토어 관리, 보안관리 등)
│   │   │   ├── llm.py
│   │   │   ├── security.py
│   │   │   ├── 📂 multilingual-e5-large     # 임베딩 모델 토크나이저
│   │   ├── 📂 db           # 데이터베이스 연결 및 세션 관리
│   │   ├── 📂 routers      # API 라우터 (각 엔드포인트)
│   │   ├── 📂 schemas      # Pydantic 스키마 정의
│   │   │   ├── main.py     # FastAPI 실행 엔트리포인트
│   │   │   ├── model.py    # Pydantic 모델 정의
│   ├── Dockerfile
│   ├── requirements.txt
├── .gitignore

```

## 🏰️ 시스템 아키텍처 구조 

<img src="https://github.com/SKNETWORKS-FAMILY-AICAMP/SKN06-FINAL-3Team/blob/main/documents/%5BAmoreSearch%5D%20%EC%8B%9C%EC%8A%A4%ED%85%9C%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.png">

- CI/CD: Github Actions
- EC2 인스턴스 1: 프론트엔드(Nuxt.js), 백엔드(FastAPI), MariaDB 배포
- EC2 인스턴스 2: 벡터 스토어(ChromaDB) 배포 및 관리
- LLM, Embedding 모델: RunPod에서 실행하여 검색 성능 최적화
- AWS S3: 데이터 저장 및 관리

## 🚀 주요 기능
### 🔹 1. 기능 제목
- 

### 🔹 2. 기능 제목
- 

## 🏆 핵심 결과 (성과)
- 

## 🛠️ 사용 기술 및 라이브러리
- `Nuxt.js`
- `FastAPI`
- `MariaDB`
- `ChromaDB`
- `Amazon S3`
- `Amazon EC2`

## 📂 실행 방법
1. **백업 실행**
```bash
cd backend
uvicorn main:app --reload
```
2. **프론트엔드 실행**
```bash
cd frontend
pnpm install
pnpm run dev
```

## 📊 데이터셋 및 모델
- 

## 📌 프로젝트 회고 (팀원별)
- **박서윤**: ""  
- **박유나**: ""  
- **유경상**: ""  
- **장예린**: ""  
