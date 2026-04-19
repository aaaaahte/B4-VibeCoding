from __future__ import annotations

from datetime import UTC, datetime

from app.models.domain import (
    ClarificationSession,
    ClarificationTurn,
    Document,
    DocumentKind,
    Project,
    StructuredSummary,
    WorkflowStatus,
)


class MockAIProvider:
    def generate_questions(self, project: Project) -> list[str]:
        return [
            f"这个项目最核心要解决的用户问题是什么？请结合「{project.idea}」描述一下。",
            "目标用户是谁？他们现在通常用什么方式解决这个问题？",
            "第一版必须上线的 3 个核心功能是什么？哪些可以后置？",
            "这个产品最关键的业务流程是什么？请按步骤描述。",
            "你目前有哪些约束条件？例如时间、预算、技术、人力或数据来源。",
        ]

    def build_summary(self, project: Project, session: ClarificationSession) -> StructuredSummary:
        confirmed_points = [
            f"项目名称：{project.name}",
            f"初始 idea：{project.idea}",
        ]
        if project.target_users:
            confirmed_points.append(f"目标用户：{project.target_users}")
        if project.scenario:
            confirmed_points.append(f"使用场景：{project.scenario}")

        confirmed_points.extend(
            f"{index + 1}. Q: {turn.question}\nA: {turn.answer}"
            for index, turn in enumerate(session.turns)
        )

        pending_points = []
        if session.current_question:
            pending_points.append(f"当前待回答：{session.current_question}")

        missing_points = [
            question
            for question in session.questions[session.current_question_index + 1 :]
            if question != session.current_question
        ]

        if not session.turns:
            missing_points = session.questions

        return StructuredSummary(
            confirmed_points=confirmed_points,
            pending_points=pending_points,
            missing_points=missing_points,
        )

    def generate_documents(self, project: Project) -> list[Document]:
        timestamp = datetime.now(UTC)
        summary_lines = "\n".join(f"- {item}" for item in project.clarification.summary.confirmed_points)
        docs = [
            Document(
                kind=DocumentKind.PRD,
                title="需求文档（PRD）",
                status=WorkflowStatus.PENDING_REVIEW,
                updated_at=timestamp,
                content=self._build_prd(project, summary_lines),
            ),
            Document(
                kind=DocumentKind.ARCHITECTURE,
                title="技术架构设计",
                status=WorkflowStatus.PENDING_REVIEW,
                updated_at=timestamp,
                content=self._build_architecture(project, summary_lines),
            ),
            Document(
                kind=DocumentKind.API,
                title="API 接口设计",
                status=WorkflowStatus.PENDING_REVIEW,
                updated_at=timestamp,
                content=self._build_api(project),
            ),
            Document(
                kind=DocumentKind.TASKS,
                title="任务清单",
                status=WorkflowStatus.PENDING_REVIEW,
                updated_at=timestamp,
                content=self._build_tasks(project),
            ),
        ]
        return docs

    def _build_prd(self, project: Project, summary_lines: str) -> str:
        return f"""# {project.name} PRD

## 项目背景
{project.idea}

## 目标用户
{project.target_users or "待进一步明确"}

## 使用场景
{project.scenario or "待进一步明确"}

## 需求澄清摘要
{summary_lines}

## MVP 功能范围
- 项目创建与基础信息录入
- AI 需求澄清与结构化摘要
- 文档中心与单篇文档查看
- 任务清单生成与阅读

## 暂不纳入首版
- 多人协作
- 真实模型接入
- 高级权限与版本历史
"""

    def _build_architecture(self, project: Project, summary_lines: str) -> str:
        return f"""# {project.name} 技术架构设计

## 技术选型
- 前端：Vue 3 + TypeScript + Vite + Pinia + Vue Router
- 后端：FastAPI
- 存储：本地 JSON 仓储抽象层（后续可切换 SQLite/PostgreSQL）
- AI：Provider 抽象层，当前使用 Mock Provider

## 系统模块
- 项目管理模块
- 需求澄清模块
- 文档生成模块
- 文档中心模块

## 数据要点
{summary_lines}

## 演进方向
- 将 Mock Provider 替换为真实 LLM 接口
- 引入数据库与认证系统
- 增加文档导出和版本管理
"""

    def _build_api(self, project: Project) -> str:
        return f"""# {project.name} API 接口设计

## 项目接口
- `GET /api/projects`：获取项目列表
- `POST /api/projects`：创建项目
- `GET /api/projects/{{projectId}}`：获取项目详情

## 需求澄清接口
- `POST /api/projects/{{projectId}}/clarification/answers`：提交当前问题回答

## 文档接口
- `POST /api/projects/{{projectId}}/documents/generate`：生成 4 份文档
- `GET /api/projects/{{projectId}}/documents`：获取文档列表
- `GET /api/projects/{{projectId}}/documents/{{kind}}`：获取单篇文档
"""

    def _build_tasks(self, project: Project) -> str:
        return f"""# {project.name} 任务清单

## P0
1. 完成项目创建与列表管理
2. 完成需求澄清问答流与结构化摘要
3. 完成 4 份文档对象生成
4. 完成文档中心与文档详情页

## P1
1. 补充文档编辑与局部重写
2. 增加真实 AI Provider
3. 增加导出与交付能力

## 验收建议
- 可以从 idea 创建项目
- 可以完成至少一轮澄清问答
- 可以阅读生成后的 Markdown 文档
"""


def answer_current_question(project: Project, answer: str) -> Project:
    session = project.clarification
    current_question = session.current_question
    if not current_question:
        return project

    session.turns.append(
        ClarificationTurn(
            question=current_question,
            answer=answer.strip(),
        )
    )
    session.current_question_index += 1
    session.updated_at = datetime.now(UTC)
    return project
