# B4VC 本地开发说明

## 技术栈

- 前端：`Vue 3 + TypeScript + Vite + Pinia + Vue Router`
- 后端：`FastAPI`
- AI 能力：统一 Provider 抽象，当前默认使用 Mock Provider

## 启动后端

在 `backend/` 目录执行：

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

默认地址：`http://127.0.0.1:8000`

## 启动前端

在 `frontend/` 目录执行：

```bash
npm install
npm run dev
```

默认地址：`http://127.0.0.1:5173`

## 当前 MVP 已实现

1. 项目创建
2. 项目工作台
3. 需求澄清问答流
4. 文档中心
5. 单篇文档详情页
6. Mock 文档生成

## 当前后端接口

- `GET /api/health`
- `GET /api/projects`
- `POST /api/projects`
- `GET /api/projects/{projectId}`
- `POST /api/projects/{projectId}/clarification/answers`
- `POST /api/projects/{projectId}/documents/generate`
- `GET /api/projects/{projectId}/documents`
- `GET /api/projects/{projectId}/documents/{kind}`
