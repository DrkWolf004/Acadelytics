import { defineConfig, loadEnv } from 'vite'
import path from 'path'

export default defineConfig(({ mode }) => {
  const envDir = path.resolve(__dirname)
  const env = loadEnv(mode, envDir)
  const baseUrl = (env.VITE_BASE_URL || `http://${env.BACKEND_HOST || 'localhost'}:${env.BACKEND_PORT || '5000'}/api`).trim()
  const apiUrl = baseUrl.replace(/\/api\/?$/, '')

  return {
    envDir,
    define: {
      'import.meta.env.VITE_BASE_URL': JSON.stringify(baseUrl),
      'import.meta.env.VITE_API_URL': JSON.stringify(apiUrl),
    },
    server: {
      port: Number(env.VITE_PORT || env.FRONTEND_PORT) || 4173,
    },
  }
})
