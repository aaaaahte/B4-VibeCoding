import { defineStore } from 'pinia'

import {
  answerClarification,
  confirmDocumentReview,
  createProject,
  fetchProject,
  fetchProjectDocument,
  fetchProjects,
  generateDocuments,
} from '../api/projects'
import type {
  DocumentKind,
  Project,
  ProjectCreatePayload,
  ProjectDocument,
} from '../types/domain'

interface ProjectState {
  projects: Project[]
  currentProject: Project | null
  currentDocument: ProjectDocument | null
  loading: boolean
  error: string | null
}

export const useProjectStore = defineStore('projects', {
  state: (): ProjectState => ({
    projects: [],
    currentProject: null,
    currentDocument: null,
    loading: false,
    error: null,
  }),

  actions: {
    async runAction<T>(action: () => Promise<T>) {
      this.loading = true
      this.error = null
      try {
        return await action()
      } catch (error) {
        this.error = error instanceof Error ? error.message : '发生未知错误'
        throw error
      } finally {
        this.loading = false
      }
    },

    async loadProjects() {
      const projects = await this.runAction(() => fetchProjects())
      this.projects = projects
      return projects
    },

    async loadProject(projectId: string) {
      const project = await this.runAction(() => fetchProject(projectId))
      this.currentProject = project
      return project
    },

    async createNewProject(payload: ProjectCreatePayload) {
      const project = await this.runAction(() => createProject(payload))
      this.currentProject = project
      this.projects = [project, ...this.projects]
      return project
    },

    async submitClarificationAnswer(projectId: string, answer: string) {
      const project = await this.runAction(() => answerClarification(projectId, answer))
      this.currentProject = project
      this.projects = this.projects.map((item) => (item.id === project.id ? project : item))
      return project
    },

    async createDocuments(projectId: string) {
      const response = await this.runAction(() => generateDocuments(projectId))
      this.currentProject = response.project
      this.projects = this.projects.map((item) =>
        item.id === response.project.id ? response.project : item,
      )
      return response.project
    },

    async confirmReview(projectId: string, kind: DocumentKind) {
      const project = await this.runAction(() => confirmDocumentReview(projectId, kind))
      this.currentProject = project
      this.projects = this.projects.map((item) => (item.id === project.id ? project : item))
      if (this.currentDocument && this.currentDocument.kind === kind) {
        const updatedDocument = project.documents.find((item) => item.kind === kind) ?? null
        this.currentDocument = updatedDocument
      }
      return project
    },

    async loadDocument(projectId: string, kind: DocumentKind) {
      const document = await this.runAction(() => fetchProjectDocument(projectId, kind))
      this.currentDocument = document
      return document
    },
  },
})
