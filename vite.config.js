import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import path from 'node:path'

export default defineConfig(({ command }) => {
  const isBuild = command === 'build'

  return {
    base: isBuild ? '/static/' : '/',
    plugins: [vue(), vueDevTools()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./monobit/web', import.meta.url)),
      },
    },
    build: {
      outDir: path.resolve(__dirname, 'monobit/static/monobit'),
      assetsDir: '', // keep flat inside monobit folder
      manifest: true,
      emptyOutDir: true,
    },
  }
})
