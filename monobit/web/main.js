import '@/assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import Antd from 'ant-design-vue'

import App from '@/App.vue'
import router from '@/router'

import { useConfigStore } from '@/stores/config'
import { useAuthStore } from '@/stores/auth'

async function bootstrap() {
  const app = createApp(App)
  const pinia = createPinia()

  app.use(pinia)
  app.use(router)
  app.use(Antd)

  const configStore = useConfigStore()
  const authStore = useAuthStore()

  await Promise.all([configStore.load(), authStore.checkAuth()])

  app.mount('#app')
}

bootstrap()
