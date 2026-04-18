<script lang="ts">
import { computed, defineComponent, type PropType } from 'vue'

import type { WorkflowStatus } from '../types/domain'

export default defineComponent({
  name: 'StatusBadge',
  props: {
    status: {
      type: String as PropType<WorkflowStatus>,
      required: true,
    },
  },
  setup(props) {
    const label = computed(() => {
      const map: Record<WorkflowStatus, string> = {
        not_started: '未开始',
        in_progress: '进行中',
        pending_review: '待确认',
        completed: '已完成',
      }

      return map[props.status]
    })

    return {
      label,
    }
  },
})
</script>

<template>
  <span class="status-badge" :data-status="status">
    {{ label }}
  </span>
</template>
