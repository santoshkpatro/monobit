import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/home-view.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/auth/login',
      name: 'login',
      component: () => import('@/views/auth/login-view.vue'),
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
      children: [
        {
          name: 'issues-list',
          path: 'issues',
          component: () => import('@/views/issues/issues-list.vue'),
          meta: { requiresLogin: true },
        },
        {
          name: 'projects-new',
          path: 'projects/new',
          component: () => import('@/views/projects/projects-new.vue'),
          meta: { requiresLogin: true },
        },
        {
          name: 'projects-list',
          path: 'projects',
          component: () => import('@/views/projects/projects-list.vue'),
          meta: { requiresLogin: true },
        },
        {
          name: 'index',
          path: '',
          component: () => import('@/views/index-view.vue'),
          meta: { requiresLogin: true },
        },
      ],
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  // Only check auth if route requires login
  if (to.meta.requiresLogin) {
    if (!authStore.isAuthenticated) {
      return {
        name: 'login',
        query: { redirect: to.fullPath },
      }
    }
  }
})

export default router
