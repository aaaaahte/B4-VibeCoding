from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import build_router
from app.repositories.project_repository import ProjectRepository
from app.services.mock_ai import MockAIProvider
from app.services.project_service import ProjectService


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "projects.json"


def create_app() -> FastAPI:
    repository = ProjectRepository(storage_path=DATA_FILE)
    ai_provider = MockAIProvider()
    project_service = ProjectService(repository=repository, ai_provider=ai_provider)

    app = FastAPI(title="B4VC API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(build_router(project_service))
    return app


app = create_app()
