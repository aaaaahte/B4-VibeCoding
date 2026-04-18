from __future__ import annotations

import json
from pathlib import Path

from app.models.domain import Project


class ProjectRepository:
    def __init__(self, storage_path: Path) -> None:
        self.storage_path = storage_path
        self._ensure_storage()

    def _ensure_storage(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self.storage_path.write_text("[]", encoding="utf-8")

    def list_projects(self) -> list[Project]:
        self._ensure_storage()
        raw_text = self.storage_path.read_text(encoding="utf-8").strip()
        if not raw_text:
            self.storage_path.write_text("[]", encoding="utf-8")
            raw_text = "[]"

        try:
            raw_items = json.loads(raw_text)
        except json.JSONDecodeError:
            self.storage_path.write_text("[]", encoding="utf-8")
            raw_items = []

        return [Project.model_validate(item) for item in raw_items]

    def get_project(self, project_id: str) -> Project | None:
        for project in self.list_projects():
            if project.id == project_id:
                return project
        return None

    def save_project(self, project: Project) -> Project:
        self._ensure_storage()
        projects = self.list_projects()
        updated = False
        for index, existing_project in enumerate(projects):
            if existing_project.id == project.id:
                projects[index] = project
                updated = True
                break

        if not updated:
            projects.append(project)

        self.storage_path.write_text(
            json.dumps(
                [item.model_dump(mode="json") for item in projects],
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        return project
