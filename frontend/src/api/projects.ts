import { apiRequest } from './client'
import type {
  DocumentKind,
  GenerateDocumentsResponse,
  Project,
  ProjectCreatePayload,
  ProjectDocument,
} from '../types/domain'

export function fetchProjects() {
  return apiRequest<Project[]>('/projects')
}

export function fetchProject(projectId: string) {
  return apiRequest<Project>(`/projects/${projectId}`)
}

export function createProject(payload: ProjectCreatePayload) {
  return apiRequest<Project>('/projects', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
}

export function answerClarification(projectId: string, answer: string) {
  return apiRequest<Project>(`/projects/${projectId}/clarification/answers`, {
    method: 'POST',
    body: JSON.stringify({ answer }),
  })
}

export function generateDocuments(projectId: string) {
  return apiRequest<GenerateDocumentsResponse>(`/projects/${projectId}/documents/generate`, {
    method: 'POST',
  })
}

export function confirmProjectReview(projectId: string) {
  return apiRequest<Project>(`/projects/${projectId}/confirm-review`, {
    method: 'POST',
  })
}

export function fetchProjectDocuments(projectId: string) {
  return apiRequest<ProjectDocument[]>(`/projects/${projectId}/documents`)
}

export function fetchProjectDocument(projectId: string, kind: DocumentKind) {
  return apiRequest<ProjectDocument>(`/projects/${projectId}/documents/${kind}`)
}
