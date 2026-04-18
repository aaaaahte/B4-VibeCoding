<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import StatusBadge from '../components/StatusBadge.vue'
import { useProjectStore } from '../stores/projectStore'

const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()

const draftAnswer = ref('')
const projectId = computed(() => String(route.params.projectId))
const project = computed(() => projectStore.currentProject)
const clarification = computed(() => project.value?.clarification)

onMounted(() => {
  void projectStore.loadProject(projectId.value)
})

async function submitAnswer() {
  if (!draftAnswer.value.trim()) {
    return
  }

  await projectStore.submitClarificationAnswer(projectId.value, draftAnswer.value)
  draftAnswer.value = ''
}

async function generateProjectDocuments() {
  await projectStore.createDocuments(projectId.value)
  await router.push(`/projects/${projectId.value}/documents`)
}
</script>

<template>
  <section v-if="projectStore.loading && !project" class="surface empty-state">
    正在加载需求澄清...
  </section>

  <template v-else-if="project && clarification">
    <section class="page-header">
      <div>
        <p class="eyebrow">需求澄清</p>
        <h1>{{ project.name }}</h1>
        <p class="page-description">通过逐轮问答把模糊 idea 沉淀成结构化需求摘要。</p>
      </div>
      <StatusBadge :status="clarification.status" />
    </section>

    <section class="two-column-layout">
      <article class="surface card">
        <div class="card-header">
          <div>
            <h2>对话区</h2>
            <p class="muted">每次回答当前问题，系统会自动更新摘要。</p>
          </div>
        </div>

        <div v-if="clarification.current_question" class="question-box">
          <p class="eyebrow">当前问题</p>
          <p class="question-text">{{ clarification.current_question }}</p>
        </div>

        <div v-else class="question-box question-box-complete">
          <p class="question-text">当前问题已全部完成，可以生成文档。</p>
        </div>

        <form class="stack" @submit.prevent="submitAnswer">
          <label>
            你的回答
            <textarea
              v-model.trim="draftAnswer"
              :disabled="!clarification.current_question || projectStore.loading"
              rows="5"
              placeholder="请尽量具体描述，这会直接影响后续文档质量。"
            />
          </label>
          <div class="button-row">
            <button
              class="button"
              type="submit"
              :disabled="!clarification.current_question || projectStore.loading"
            >
              {{ projectStore.loading ? '提交中...' : '提交回答' }}
            </button>
            <button
              class="button button-secondary"
              type="button"
              :disabled="clarification.turns.length === 0 || projectStore.loading"
              @click="generateProjectDocuments"
            >
              生成文档
            </button>
          </div>
          <p v-if="projectStore.error" class="error-text">{{ projectStore.error }}</p>
        </form>

        <div class="stack">
          <h3>历史问答</h3>
          <article
            v-for="(turn, index) in clarification.turns"
            :key="`${turn.created_at}-${index}`"
            class="history-item"
          >
            <p><strong>Q{{ index + 1 }}：</strong>{{ turn.question }}</p>
            <p><strong>A：</strong>{{ turn.answer }}</p>
          </article>
          <p v-if="clarification.turns.length === 0" class="muted">还没有历史问答。</p>
        </div>
      </article>

      <article class="surface card">
        <h2>结构化摘要</h2>

        <section class="summary-block">
          <h3>已确认</h3>
          <ul class="list">
            <li v-for="item in clarification.summary.confirmed_points" :key="item">{{ item }}</li>
          </ul>
        </section>

        <section class="summary-block">
          <h3>待确认</h3>
          <ul class="list">
            <li v-for="item in clarification.summary.pending_points" :key="item">{{ item }}</li>
          </ul>
        </section>

        <section class="summary-block">
          <h3>缺失信息</h3>
          <ul class="list">
            <li v-for="item in clarification.summary.missing_points" :key="item">{{ item }}</li>
          </ul>
        </section>
      </article>
    </section>
  </template>

  <section v-else class="surface empty-state">
    <h2>未找到项目</h2>
    <RouterLink class="button" to="/">返回项目列表</RouterLink>
  </section>
</template>
