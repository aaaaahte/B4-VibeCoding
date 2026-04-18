<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import StatusBadge from '../components/StatusBadge.vue'
import { useProjectStore } from '../stores/projectStore'
import type { DocumentKind } from '../types/domain'
import { exportDocumentAsMarkdown } from '../utils/markdownExport'

const route = useRoute()
const projectStore = useProjectStore()

const projectId = computed(() => String(route.params.projectId))
const kind = computed(() => String(route.params.kind) as DocumentKind)
const project = computed(() => projectStore.currentProject)

onMounted(async () => {
  await projectStore.loadProject(projectId.value)
  await projectStore.loadDocument(projectId.value, kind.value)
})

async function confirmReview() {
  await projectStore.confirmReview(projectId.value)
}

function exportCurrentDocument() {
  if (!project.value || !projectStore.currentDocument) {
    return
  }

  exportDocumentAsMarkdown(project.value.name, projectStore.currentDocument)
}
</script>

<template>
  <div>
    <section v-if="projectStore.loading && !projectStore.currentDocument" class="surface empty-state">
      正在加载文档详情...
    </section>

    <template v-else-if="projectStore.currentDocument">
      <section class="page-header">
        <div>
          <p class="eyebrow">文档详情</p>
          <h1>{{ projectStore.currentDocument.title }}</h1>
          <p class="page-description">当前以 Markdown 原文形式展示，便于后续直接导出与复用。</p>
        </div>
        <StatusBadge :status="projectStore.currentDocument.status" />
      </section>

      <section class="surface card">
        <div class="button-row">
          <button
            class="button"
            type="button"
            :disabled="!projectStore.currentDocument.content"
            @click="exportCurrentDocument"
          >
            导出 MD
          </button>
          <button
            v-if="project?.stage === 'documents' && project?.status === 'pending_review'"
            class="button"
            type="button"
            :disabled="projectStore.loading"
            @click="confirmReview"
          >
            {{ projectStore.loading ? '确认中...' : '确认文档评审完成' }}
          </button>
          <RouterLink class="button button-secondary" :to="`/projects/${projectId}/documents`">
            返回文档中心
          </RouterLink>
        </div>
        <p v-if="projectStore.error" class="error-text">{{ projectStore.error }}</p>
        <pre class="markdown-preview">{{ projectStore.currentDocument.content || '文档尚未生成。' }}</pre>
      </section>
    </template>

    <section v-else class="surface empty-state">
      <h2>文档不存在</h2>
      <RouterLink class="button" :to="`/projects/${projectId}/documents`">返回文档中心</RouterLink>
    </section>
  </div>
</template>
