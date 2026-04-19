from __future__ import annotations

from fastapi import APIRouter

from app.models.domain import (
    ClarificationAnswerRequest,
    DocumentGenerationResponse,
    DocumentKind,
    Project,
    ProjectCreate,
)
from app.services.project_service import ProjectService


def build_router(project_service: ProjectService) -> APIRouter:
    router = APIRouter(prefix="/api")

    @router.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    @router.get("/projects", response_model=list[Project])
    def list_projects() -> list[Project]:
        return project_service.list_projects()

    @router.post("/projects", response_model=Project)
    def create_project(payload: ProjectCreate) -> Project:
        return project_service.create_project(payload)

    @router.get("/projects/{project_id}", response_model=Project)
    def get_project(project_id: str) -> Project:
        return project_service.get_project(project_id)

    @router.post("/projects/{project_id}/clarification/answers", response_model=Project)
    def answer_clarification(project_id: str, payload: ClarificationAnswerRequest) -> Project:
        return project_service.answer_clarification(project_id, payload.answer)

    @router.post(
        "/projects/{project_id}/documents/generate",
        response_model=DocumentGenerationResponse,
    )
    def generate_documents(project_id: str) -> DocumentGenerationResponse:
        return project_service.generate_documents(project_id)

    @router.post("/projects/{project_id}/documents/{kind}/confirm-review", response_model=Project)
    def confirm_document_review(project_id: str, kind: DocumentKind) -> Project:
        return project_service.confirm_document_review(project_id, kind)

    @router.get("/projects/{project_id}/documents")
    def list_documents(project_id: str):
        return project_service.list_documents(project_id)

    @router.get("/projects/{project_id}/documents/{kind}")
    def get_document(project_id: str, kind: DocumentKind):
        return project_service.get_document(project_id, kind)

    return router
