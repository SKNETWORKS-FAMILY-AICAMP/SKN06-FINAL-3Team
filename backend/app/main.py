from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, admin, member, amorepacific, post, product, search

app = FastAPI()

    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(member.router, prefix="/api/member", tags=["member"])
app.include_router(amorepacific.router, prefix="/api/amorepacific", tags=["amorepacific"])
app.include_router(post.router, prefix="/api/post", tags=["post"])
app.include_router(product.router, prefix="/api/product", tags=["product"])
app.include_router(search.router, prefix="/api/search", tags=["search"])