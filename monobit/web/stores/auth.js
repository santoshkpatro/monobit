import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { authStatusAPI } from '@/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const checked = ref(false)

  const isAuthenticated = computed(() => !!user.value)

  async function checkAuth() {
    try {
      const { data } = await authStatusAPI()
      console.log('Data', data)
      user.value = data.authenticatedUser
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
