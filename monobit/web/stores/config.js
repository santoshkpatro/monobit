import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { configAPI } from '@/api'

export const useConfigStore = defineStore('config', () => {
  const config = ref(null)
  const loaded = ref(false)

  async function load() {
    const { data } = await configAPI()
    config.value = data
    loaded.value = true
  }

  return {
    config,
    loaded,
    load,
  }
})
