<script setup lang="ts">
import { reactive } from 'vue'
import { useRouter } from 'vue-router'

import { useProjectStore } from '../stores/projectStore'

const router = useRouter()
const projectStore = useProjectStore()

const form = reactive({
  name: '',
  idea: '',
  target_users: '',
  scenario: '',
  references: '',
  constraints: '',
  tech_preferences: '',
})

async function submitForm() {
  const project = await projectStore.createNewProject(form)
  await router.push(`/projects/${project.id}/clarification`)
}
</script>

<template>
  <section class="page-header">
    <div>
      <p class="eyebrow">项目初始化</p>
      <h1>新建项目</h1>
      <p class="page-description">先填写最小必要信息，系统会基于这些内容发起第一轮需求澄清。</p>
    </div>
  </section>

  <form class="surface form-layout" @submit.prevent="submitForm">
    <label>
      项目名称
      <input v-model.trim="form.name" required placeholder="例如：B4VC Web MVP" />
    </label>

    <label>
      一句话 idea
      <textarea
        v-model.trim="form.idea"
        required
        rows="4"
        placeholder="例如：一个帮助零基础用户把 idea 变成开发文档的 AI 产品。"
      />
    </label>

    <div class="form-grid">
      <label>
        目标用户
        <input v-model.trim="form.target_users" placeholder="独立开发者、产品经理、Vibe Coding 用户" />
      </label>

      <label>
        使用场景
        <input v-model.trim="form.scenario" placeholder="项目前期规划、需求整理、交付开发任务" />
      </label>
    </div>

    <label>
      参考产品
      <input v-model.trim="form.references" placeholder="可选，例如 Notion AI / v0 / Cursor" />
    </label>

    <div class="form-grid">
      <label>
        时间或预算约束
        <input v-model.trim="form.constraints" placeholder="例如：2 周内做出可演示版" />
      </label>

      <label>
        技术偏好
        <input v-model.trim="form.tech_preferences" placeholder="例如：前端 Vue，后端 Python" />
      </label>
    </div>

    <div class="actions">
      <button class="button" type="submit" :disabled="projectStore.loading">
        {{ projectStore.loading ? '创建中...' : '创建并开始需求澄清' }}
      </button>
      <p v-if="projectStore.error" class="error-text">{{ projectStore.error }}</p>
    </div>
  </form>
</template>
