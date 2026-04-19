<script setup lang="ts">
import { onMounted } from 'vue'

import StatusBadge from '../components/StatusBadge.vue'
import { useProjectStore } from '../stores/projectStore'

const projectStore = useProjectStore()

onMounted(() => {
  void projectStore.loadProjects()
})
</script>

<template>
  <div class="stack">
    <section class="page-hero">
      <div>
        <p class="eyebrow">B4VC Web</p>
        <h1>把想法变成可执行的开发文档</h1>
        <p class="page-description">
          从一个模糊 idea 出发，完成需求澄清、文档生成与任务拆解，为 Coding Agent 提供开发入口。
        </p>
      </div>
      <RouterLink class="button" to="/projects/new">新建项目</RouterLink>
    </section>

    <section v-if="projectStore.loading" class="surface empty-state">
      正在加载项目列表...
    </section>

    <section v-else-if="projectStore.projects.length === 0" class="surface empty-state">
      <h2>还没有项目</h2>
      <p class="muted">先创建一个项目，开始你的第一轮需求澄清。</p>
      <RouterLink class="button" to="/projects/new">创建第一个项目</RouterLink>
    </section>

    <section v-else class="card-grid">
      <article v-for="project in projectStore.projects" :key="project.id" class="surface card">
        <div class="card-header">
          <div>
            <h2>{{ project.name }}</h2>
            <p class="muted">{{ project.idea }}</p>
          </div>
          <StatusBadge :status="project.status" />
        </div>
        <dl class="meta-grid">
          <div>
            <dt>阶段</dt>
            <dd>{{ project.stage }}</dd>
          </div>
          <div>
            <dt>最近更新</dt>
            <dd>{{ new Date(project.updated_at).toLocaleString() }}</dd>
          </div>
        </dl>
        <RouterLink class="button button-secondary" :to="`/projects/${project.id}`">
          进入工作台
        </RouterLink>
      </article>
    </section>
  </div>
</template>
