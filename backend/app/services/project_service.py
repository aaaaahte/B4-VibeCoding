from __future__ import annotations

from datetime import UTC, datetime

from fastapi import HTTPException, status

from app.models.domain import (
    ClarificationSession,
    Document,
    DocumentGenerationResponse,
    DocumentKind,
    Project,
    ProjectCreate,
    ProjectStage,
    StructuredSummary,
    WorkflowStatus,
)
from app.repositories.project_repository import ProjectRepository
from app.services.mock_ai import MockAIProvider, answer_current_question


DOCUMENT_TITLES: dict[DocumentKind, str] = {
    DocumentKind.PRD: "需求文档（PRD）",
    DocumentKind.ARCHITECTURE: "技术架构设计",
    DocumentKind.API: "API 接口设计",
    DocumentKind.TASKS: "任务清单",
}


class ProjectService:
    def __init__(self, repository: ProjectRepository, ai_provider: MockAIProvider) -> None:
        self.repository = repository
        self.ai_provider = ai_provider

    def list_projects(self) -> list[Project]:
        return sorted(
            self.repository.list_projects(),
            key=lambda project: project.updated_at,
            reverse=True,
        )

    def create_project(self, payload: ProjectCreate) -> Project:
        project = Project(
            **payload.model_dump(),
            stage=ProjectStage.CLARIFICATION,
            status=WorkflowStatus.IN_PROGRESS,
        )
        project.clarification = self._create_clarification_session(project)
        project.documents = self._build_empty_documents()
        return self.repository.save_project(project)

    def get_project(self, project_id: str) -> Project:
        project = self.repository.get_project(project_id)
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="项目不存在")
        return project

    def answer_clarification(self, project_id: str, answer: str) -> Project:
        project = self.get_project(project_id)
        answer_current_question(project, answer)

        session = project.clarification
        if session.current_question_index >= len(session.questions):
            session.current_question = None
            session.status = WorkflowStatus.COMPLETED
            project.status = WorkflowStatus.PENDING_REVIEW
        else:
            session.current_question = session.questions[session.current_question_index]
            session.status = WorkflowStatus.IN_PROGRESS
            project.status = WorkflowStatus.IN_PROGRESS

        session.summary = self.ai_provider.build_summary(project, session)
        project.updated_at = datetime.now(UTC)
        return self.repository.save_project(project)

    def generate_documents(self, project_id: str) -> DocumentGenerationResponse:
        project = self.get_project(project_id)
        if not project.clarification.turns:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="请先完成至少一轮需求澄清",
            )

        project.documents = self.ai_provider.generate_documents(project)
        project.stage = ProjectStage.DOCUMENTS
        project.status = WorkflowStatus.PENDING_REVIEW
        project.updated_at = datetime.now(UTC)
        saved_project = self.repository.save_project(project)
        return DocumentGenerationResponse(message="文档生成完成", project=saved_project)

    def confirm_project_review(self, project_id: str) -> Project:
        project = self.get_project(project_id)
        if project.stage != ProjectStage.DOCUMENTS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="当前项目还未进入文档确认阶段",
            )

        project.status = WorkflowStatus.COMPLETED
        project.updated_at = datetime.now(UTC)
        return self.repository.save_project(project)

    def list_documents(self, project_id: str) -> list[Document]:
        project = self.get_project(project_id)
        return project.documents

    def get_document(self, project_id: str, kind: DocumentKind) -> Document:
        project = self.get_project(project_id)
        for document in project.documents:
            if document.kind == kind:
                return document
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="文档不存在")

    def _create_clarification_session(self, project: Project) -> ClarificationSession:
        questions = self.ai_provider.generate_questions(project)
        session = ClarificationSession(
            questions=questions,
            current_question=questions[0] if questions else None,
            summary=StructuredSummary(
                confirmed_points=[
                    f"项目名称：{project.name}",
                    f"初始 idea：{project.idea}",
                ],
                pending_points=[f"当前待回答：{questions[0]}"] if questions else [],
                missing_points=questions[1:] if len(questions) > 1 else [],
            ),
        )
        return session

    def _build_empty_documents(self) -> list[Document]:
        return [
            Document(
                kind=kind,
                title=title,
                status=WorkflowStatus.NOT_STARTED,
                content="",
            )
            for kind, title in DOCUMENT_TITLES.items()
        ]
