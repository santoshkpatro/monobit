import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useConfigStore = defineStore('config', () => {
  const config = ref(null)
  const loaded = ref(false)

  async function load() {
    const { data } = await axios.get('/api/config')
    config.value = data
    loaded.value = true
  }

  return {
    config,
    loaded,
    load,
  }
})
