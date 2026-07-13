import { defineConfig, loadEnv } from 'vite'
import path from 'path'

export default defineConfig(({ mode }) => {
  const envDir = path.resolve(__dirname, '..')
  const env = loadEnv(mode, envDir)
  const apiUrl = env.VITE_API_URL || `http://${env.DB_HOST || 'localhost'}:${env.BACKEND_PORT || '5000'}`

  return {
    envDir,
    define: {
      'import.meta.env.VITE_API_URL': JSON.stringify(apiUrl),
    },
    server: {
      port: Number(env.VITE_PORT || env.FRONTEND_PORT) || 4173,
    },
  }
})
