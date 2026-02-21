import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/home-view.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresLogin: true },
    },
    {
      path: '/auth/login',
      name: 'login',
      component: () => import('@/views/auth/login-view.vue'),
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  // Only check auth if route requires login
  if (to.meta.requiresLogin) {
    if (!authStore.checked) {
      await authStore.checkAuth()
    }

    if (!authStore.isAuthenticated) {
      return {
        name: 'login',
        query: { redirect: to.fullPath },
      }
    }
  }
})

export default router
