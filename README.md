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
📦 프로젝트 루트
├── 📂 frontend        # 프론트엔드 (Vue.js & Nuxt.js)
│   ├── 📂 assets      # 정적 파일 (CSS, 이미지 등)
│   ├── 📂 components  # Vue 컴포넌트 모음
│   │   ├── 📂 Dialog
│   │   ├── 📂 ListItem
│   │   ├── Lnb.vue
│   │   ├── Paging.vue
│   │   ├── RnbProduct.vue
│   │   ├── SearchInput.vue
│   ├── 📂 composables  # 재사용 가능한 함수 모음
│   │   ├── useApi.ts
│   │   ├── useState.ts
│   ├── 📂 layouts      # 레이아웃 컴포넌트
│   │   ├── default.vue
│   ├── 📂 middleware   # 미들웨어
│   │   ├── valid_admin.ts
│   │   ├── valid_member.global.ts
│   ├── 📂 pages        # 페이지 컴포넌트
│   │   ├── 📂 admin
│   │   │   ├── ai-search.vue
│   │   │   ├── amorestory.vue
│   │   │   ├── dashboard.vue
│   │   │   ├── favorites.vue
│   │   │   ├── index.vue
│   │   │   ├── mypage.vue
│   │   │   ├── news-journal.vue
│   │   │   ├── products.vue
│   ├── 📂 plugins      # 플러그인 모음
│   │   ├── api.ts
│   │   ├── vue-the-mask.js
│   │   ├── vuetify.ts
│   ├── 📂 public       # 공개 정적 파일 (이미지, 폰트 등)
│   │   ├── 📂 img
│   │   │   ├── 📂 icon
│   │   │   ├── 📂 logo
│   │   │   │   ├── logo_symbol_w.svg
│   │   │   │   ├── logo_w.svg
│   │   │   │   ├── logo.svg
│   │   │   ├── product1.webp
│   │   │   ├── product2.webp
│   │   ├── favicon.ico
│   │   ├── robots.txt
│   ├── 📂 utils        # 유틸리티 함수 모음
│   │   ├── common.util.ts
│   │   ├── types.ts
│   │   ├── variable.util.ts
│   ├── app.vue
│   ├── nuxt.config.ts
│   ├── package.json
│   ├── Dockerfile
│
├── 📂 backend         # 백엔드 (FastAPI)
│   ├── 📂 app
│   │   ├── 📂 core
│   │   │   ├── llm.py
│   │   │   ├── security.py
│   │   │   ├── 📂 multilingual-e5-large     # 임베딩 모델 토크나이저
│   │   ├── 📂 db
│   │   │   ├── connection.py
│   │   │   ├── session.py
│   │   ├── 📂 routers
│   │   │   ├── admin.py
│   │   │   ├── amorepacific.py
│   │   │   ├── auth.py
│   │   │   ├── member.py
│   │   │   ├── post.py
│   │   │   ├── product.py
│   │   │   ├── search.py
│   │   ├── 📂 schemas
│   │   │   ├── main.py
│   │   │   ├── model.py
│   ├── Dockerfile
│   ├── requirements.txt
│
├── .gitignore

```

## 🏰️ 시스템 아키텍처 구조
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
