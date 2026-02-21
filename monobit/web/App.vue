<script setup>
import { RouterLink, RouterView } from 'vue-router'
const theme = {
  token: {
    borderRadius: 4,
    fontFamily: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, 'Helvetica Neue', Arial, sans-serif`,
  },
}
</script>

<template>
  <a-config-provider :theme="theme">
    <RouterView />
  </a-config-provider>
</template>

<style scoped></style>
