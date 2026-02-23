<script setup>
import { RouterLink, RouterView } from 'vue-router'
const theme = {
  token: {
    borderRadius: 6,
    fontFamily: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, 'Helvetica Neue', Arial, sans-serif`,
    fontSize: 13, // default is 14
    fontSizeLG: 14,
    fontSizeSM: 12,
    lineHeight: 1.4,
  },
  components: {
    Menu: {
      itemHeight: 34, // default is ~40
      itemMarginInline: 8,
      itemBorderRadius: 6,
    },
  },
}
</script>

<template>
  <a-config-provider :theme="theme">
    <RouterView />
  </a-config-provider>
</template>

<style scoped></style>
