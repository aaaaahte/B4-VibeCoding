<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'

import { useProjectStore } from '../stores/projectStore'

const router = useRouter()
const projectStore = useProjectStore()

const form = reactive({
  name: '',
  idea: '',
})

async function submitForm() {
  const project = await projectStore.createNewProject(form)
  await router.push(`/projects/${project.id}/clarification`)
}
</script>

<template>
  <div class="project-create-page stack">
    <section class="page-header">
      <div>
        <p class="eyebrow">项目初始化</p>
        <h1>新建项目</h1>
        <p class="page-description">
          只需要输入项目名称和一句话 idea，其他需求细节将由系统在后续问答中逐步补齐。
        </p>
      </div>
    </section>

    <form class="surface form-layout project-create-form" @submit.prevent="submitForm">
      <label class="form-field">
        <span class="field-label">项目名称</span>
        <input v-model.trim="form.name" required placeholder="例如：B4VC Web MVP" />
      </label>

      <label class="form-field">
        <span class="field-label">一句话 idea</span>
        <textarea
          v-model.trim="form.idea"
          required
          rows="5"
          placeholder="例如：一个帮助零基础用户把 idea 变成开发文档的 AI 产品。"
        />
      </label>



      <div class="actions project-create-actions">
        <button class="button" type="submit" :disabled="projectStore.loading">
          {{ projectStore.loading ? '创建中...' : '创建并开始需求澄清' }}
        </button>
        <p v-if="projectStore.error" class="error-text">{{ projectStore.error }}</p>
      </div>
    </form>
  </div>
</template>

<style scoped>
.project-create-page {
  max-width: 900px;
  margin: 0 auto;
  gap: 1.5rem;
}

.project-create-form {
  padding: 1.75rem;
  gap: 1.25rem;
}

.form-field {
  display: grid;
  gap: 0.55rem;
}

.field-label {
  font-weight: 600;
}

.project-create-grid {
  gap: 1.25rem;
}

.project-create-form textarea {
  min-height: 8.5rem;
}

.create-hint {
  padding: 1.25rem;
  background: var(--muted-bg);
  border-radius: 16px;
  border: 1px dashed var(--border);
}

.create-hint h2 {
  margin: 0 0 0.75rem;
  font-size: 1rem;
}

.project-create-actions {
  margin-top: 0.5rem;
  padding-top: 0.5rem;
}

@media (max-width: 900px) {
  .project-create-form {
    padding: 1.25rem;
  }
}
</style>
