<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import StatusBadge from '../components/StatusBadge.vue'
import { useProjectStore } from '../stores/projectStore'

const route = useRoute()
const projectStore = useProjectStore()

const projectId = computed(() => String(route.params.projectId))
const project = computed(() => projectStore.currentProject)

onMounted(() => {
  void projectStore.loadProject(projectId.value)
})
</script>

<template>
  <div>
    <section v-if="projectStore.loading && !project" class="surface empty-state">
      正在加载项目工作台...
    </section>

    <template v-else-if="project">
      <section class="page-header">
        <div>
          <p class="eyebrow">项目工作台</p>
          <h1>{{ project.name }}</h1>
          <p class="page-description">{{ project.idea }}</p>
          <div class="button-row workspace-actions">
            <RouterLink class="button" :to="`/projects/${project.id}/clarification`">
              继续需求澄清
            </RouterLink>
            <RouterLink class="button button-secondary" :to="`/projects/${project.id}/documents`">
              查看文档中心
            </RouterLink>
          </div>
          <p v-if="projectStore.error" class="error-text">{{ projectStore.error }}</p>
        </div>
        <StatusBadge :status="project.status" />
      </section>

      <section class="surface card">
        <h2>项目概要</h2>
        <dl class="stacked-meta">
          <div>
            <dt>当前阶段</dt>
            <dd>{{ project.stage }}</dd>
          </div>
          <div>
            <dt>目标用户</dt>
            <dd>{{ project.target_users || '待补充' }}</dd>
          </div>
          <div>
            <dt>使用场景</dt>
            <dd>{{ project.scenario || '待补充' }}</dd>
          </div>
        </dl>
      </section>

      <section class="surface card">
        <div class="card-header">
          <div>
            <h2>文档状态</h2>
            <p class="muted">当前项目已维护 4 份标准文档对象。</p>
          </div>
        </div>
        <div class="status-grid">
          <article v-for="document in project.documents" :key="document.kind" class="status-tile">
            <h3>{{ document.title }}</h3>
            <StatusBadge :status="document.status" />
          </article>
        </div>
      </section>
    </template>

    <section v-else class="surface empty-state">
      <h2>未找到项目</h2>
      <RouterLink class="button" to="/">返回项目列表</RouterLink>
    </section>
  </div>
</template>

<style scoped>
.workspace-actions {
  margin-top: 1rem;
}
</style>
