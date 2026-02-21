import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const checked = ref(false)

  const isAuthenticated = computed(() => !!user.value)

  async function checkAuth() {
    try {
      const { data } = await axios.get('/api/auth/me')
      user.value = data
    } catch (e) {
      user.value = null
    } finally {
      checked.value = true
    }
  }

  return {
    user,
    checked,
    isAuthenticated,
    checkAuth,
  }
})
