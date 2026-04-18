from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


def now_utc() -> datetime:
    return datetime.now(UTC)


class WorkflowStatus(StrEnum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PENDING_REVIEW = "pending_review"
    COMPLETED = "completed"


class ProjectStage(StrEnum):
    DRAFT = "draft"
    CLARIFICATION = "clarification"
    DOCUMENTS = "documents"


class DocumentKind(StrEnum):
    PRD = "prd"
    ARCHITECTURE = "architecture"
    API = "api"
    TASKS = "tasks"


class ClarificationTurn(BaseModel):
    question: str
    answer: str
    created_at: datetime = Field(default_factory=now_utc)


class StructuredSummary(BaseModel):
    confirmed_points: list[str] = Field(default_factory=list)
    pending_points: list[str] = Field(default_factory=list)
    missing_points: list[str] = Field(default_factory=list)


class ClarificationSession(BaseModel):
    questions: list[str] = Field(default_factory=list)
    turns: list[ClarificationTurn] = Field(default_factory=list)
    current_question_index: int = 0
    current_question: str | None = None
    summary: StructuredSummary = Field(default_factory=StructuredSummary)
    status: WorkflowStatus = WorkflowStatus.IN_PROGRESS
    updated_at: datetime = Field(default_factory=now_utc)


class Document(BaseModel):
    kind: DocumentKind
    title: str
    status: WorkflowStatus = WorkflowStatus.NOT_STARTED
    content: str = ""
    updated_at: datetime = Field(default_factory=now_utc)


class Project(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    idea: str
    target_users: str = ""
    scenario: str = ""
    references: str = ""
    constraints: str = ""
    tech_preferences: str = ""
    stage: ProjectStage = ProjectStage.DRAFT
    status: WorkflowStatus = WorkflowStatus.NOT_STARTED
    created_at: datetime = Field(default_factory=now_utc)
    updated_at: datetime = Field(default_factory=now_utc)
    clarification: ClarificationSession = Field(default_factory=ClarificationSession)
    documents: list[Document] = Field(default_factory=list)


class ProjectCreate(BaseModel):
    name: str
    idea: str
    target_users: str = ""
    scenario: str = ""
    references: str = ""
    constraints: str = ""
    tech_preferences: str = ""


class ClarificationAnswerRequest(BaseModel):
    answer: str = Field(min_length=1)


class DocumentGenerationResponse(BaseModel):
    message: str
    project: Project


DocumentKindLiteral = Literal["prd", "architecture", "api", "tasks"]
