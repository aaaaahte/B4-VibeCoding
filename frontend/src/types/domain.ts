export type WorkflowStatus =
  | 'not_started'
  | 'in_progress'
  | 'pending_review'
  | 'completed'

export type ProjectStage = 'draft' | 'clarification' | 'documents'

export type DocumentKind = 'prd' | 'architecture' | 'api' | 'tasks'

export interface ClarificationTurn {
  question: string
  answer: string
  created_at: string
}

export interface StructuredSummary {
  confirmed_points: string[]
  pending_points: string[]
  missing_points: string[]
}

export interface ClarificationSession {
  questions: string[]
  turns: ClarificationTurn[]
  current_question_index: number
  current_question: string | null
  summary: StructuredSummary
  status: WorkflowStatus
  updated_at: string
}

export interface ProjectDocument {
  kind: DocumentKind
  title: string
  status: WorkflowStatus
  content: string
  updated_at: string
}

export interface Project {
  id: string
  name: string
  idea: string
  target_users: string
  scenario: string
  references: string
  constraints: string
  tech_preferences: string
  stage: ProjectStage
  status: WorkflowStatus
  created_at: string
  updated_at: string
  clarification: ClarificationSession
  documents: ProjectDocument[]
}

export interface ProjectCreatePayload {
  name: string
  idea: string
  target_users?: string
  scenario?: string
  references?: string
  constraints?: string
  tech_preferences?: string
}

export interface GenerateDocumentsResponse {
  message: string
  project: Project
}
