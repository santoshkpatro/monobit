import '@/assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import { useConfigStore } from '@/stores/config'
import { useAuthStore } from '@/stores/auth'

async function bootstrap() {
  const app = createApp(App)
  const pinia = createPinia()

  app.use(pinia)
  app.use(router)

  const configStore = useConfigStore()
  const authStore = useAuthStore()

  // Run in parallel for speed
  await Promise.all([configStore.load()])

  app.mount('#app')
}

bootstrap()
