import { createRouter, createWebHistory } from 'vue-router'

import ClarificationView from '../views/ClarificationView.vue'
import DocumentDetailView from '../views/DocumentDetailView.vue'
import DocumentsView from '../views/DocumentsView.vue'
import ProjectCreateView from '../views/ProjectCreateView.vue'
import ProjectListView from '../views/ProjectListView.vue'
import ProjectWorkspaceView from '../views/ProjectWorkspaceView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'projects',
      component: ProjectListView,
    },
    {
      path: '/projects/new',
      name: 'project-create',
      component: ProjectCreateView,
    },
    {
      path: '/projects/:projectId',
      name: 'project-workspace',
      component: ProjectWorkspaceView,
      props: true,
    },
    {
      path: '/projects/:projectId/clarification',
      name: 'project-clarification',
      component: ClarificationView,
      props: true,
    },
    {
      path: '/projects/:projectId/documents',
      name: 'project-documents',
      component: DocumentsView,
      props: true,
    },
    {
      path: '/projects/:projectId/documents/:kind',
      name: 'document-detail',
      component: DocumentDetailView,
      props: true,
    },
  ],
})

export default router
