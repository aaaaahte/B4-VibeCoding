<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import DocumentCard from '../components/DocumentCard.vue'
import { useProjectStore } from '../stores/projectStore'
import { exportAllDocumentsAsMarkdown } from '../utils/markdownExport'

const route = useRoute()
const projectStore = useProjectStore()

const projectId = computed(() => String(route.params.projectId))
const project = computed(() => projectStore.currentProject)

onMounted(() => {
  void projectStore.loadProject(projectId.value)
})

async function confirmReview() {
  await projectStore.confirmReview(projectId.value)
}

function exportAllDocuments() {
  if (!project.value) {
    return
  }

  exportAllDocumentsAsMarkdown(project.value.name, project.value.documents)
}
</script>

<template>
  <div>
    <section v-if="projectStore.loading && !project" class="surface empty-state">
      正在加载文档中心...
    </section>

    <template v-else-if="project">
      <section class="page-header">
        <div>
          <p class="eyebrow">文档中心</p>
          <h1>{{ project.name }}</h1>
          <p class="page-description">统一查看 PRD、技术架构、API 接口与任务清单。</p>
        </div>
        <div class="button-row">
          <button
            class="button"
            type="button"
            :disabled="!project.documents.some((document) => document.content)"
            @click="exportAllDocuments"
          >
            导出全部 MD
          </button>
          <button
            v-if="project.stage === 'documents' && project.status === 'pending_review'"
            class="button"
            type="button"
            :disabled="projectStore.loading"
            @click="confirmReview"
          >
            {{ projectStore.loading ? '确认中...' : '确认文档评审完成' }}
          </button>
          <RouterLink class="button button-secondary" :to="`/projects/${project.id}`">
            返回工作台
          </RouterLink>
        </div>
      </section>

      <p v-if="projectStore.error" class="error-text">{{ projectStore.error }}</p>

      <section class="card-grid">
        <DocumentCard
          v-for="document in project.documents"
          :key="document.kind"
          :project-id="project.id"
          :project-name="project.name"
          :document="document"
        />
      </section>
    </template>

    <section v-else class="surface empty-state">
      <h2>未找到项目</h2>
      <RouterLink class="button" to="/">返回项目列表</RouterLink>
    </section>
  </div>
</template>
