<script lang="ts">
import { defineComponent, type PropType } from 'vue'

import type { ProjectDocument } from '../types/domain'
import { exportDocumentAsMarkdown } from '../utils/markdownExport'
import StatusBadge from './StatusBadge.vue'

export default defineComponent({
  name: 'DocumentCard',
  components: {
    StatusBadge,
  },
  props: {
    projectId: {
      type: String,
      required: true,
    },
    projectName: {
      type: String,
      required: true,
    },
    document: {
      type: Object as PropType<ProjectDocument>,
      required: true,
    },
  },
  methods: {
    exportMarkdown() {
      exportDocumentAsMarkdown(this.projectName, this.document)
    },
  },
})
</script>

<template>
  <article class="surface card">
    <div class="card-header">
      <div>
        <h3>{{ document.title }}</h3>
        <p class="muted">文档类型：{{ document.kind }}</p>
      </div>
      <StatusBadge :status="document.status" />
    </div>
    <p class="card-content">
      {{
        document.content
          ? '已生成内容，可进入详情页查看。'
          : '尚未生成内容，完成澄清后即可生成。'
      }}
    </p>
    <div class="button-row">
      <button
        class="button"
        type="button"
        :disabled="!document.content"
        @click="exportMarkdown"
      >
        导出 MD
      </button>
      <RouterLink class="button button-secondary" :to="`/projects/${projectId}/documents/${document.kind}`">
        查看详情
      </RouterLink>
    </div>
  </article>
</template>
