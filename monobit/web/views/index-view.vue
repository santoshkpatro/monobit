<script setup>
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'

const router = useRouter()

onMounted(() => {
  router.push({ name: 'issues-list' })
})
</script>

<template>
  <div>Index</div>
</template>
