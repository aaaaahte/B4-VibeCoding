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

async function confirmReview() {
  await projectStore.confirmReview(projectId.value)
}
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
        </div>
        <StatusBadge :status="project.status" />
      </section>

      <section class="dashboard-grid">
        <article class="surface card">
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
        </article>

        <article class="surface card">
          <h2>下一步建议</h2>
          <ul class="list">
            <li>先完成需求澄清问答，沉淀结构化摘要。</li>
            <li>确认摘要无误后，生成 4 份开发文档。</li>
            <li>在文档中心查看 PRD、架构、API 和任务清单。</li>
          </ul>
          <div class="button-row">
            <RouterLink class="button" :to="`/projects/${project.id}/clarification`">
              继续需求澄清
            </RouterLink>
            <RouterLink class="button button-secondary" :to="`/projects/${project.id}/documents`">
              查看文档中心
            </RouterLink>
            <button
              v-if="project.stage === 'documents' && project.status === 'pending_review'"
              class="button"
              type="button"
              :disabled="projectStore.loading"
              @click="confirmReview"
            >
              {{ projectStore.loading ? '确认中...' : '确认文档评审完成' }}
            </button>
          </div>
          <p v-if="projectStore.error" class="error-text">{{ projectStore.error }}</p>
        </article>
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
