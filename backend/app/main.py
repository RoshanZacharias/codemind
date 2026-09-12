from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.auth import router as auth_router
from .routers.projects import router as projects_router
from .routers.repositories import router as repositories_router
from .routers.ask import router as ask_router


app = FastAPI(
    title="CodeMind API",
    description="AI-Powered Software Engineering Intelligence Platform",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(repositories_router)
app.include_router(ask_router)

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "codemind-api",
    }