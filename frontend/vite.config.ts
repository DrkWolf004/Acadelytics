import { defineConfig, loadEnv } from 'vite'
import path from 'path'

export default defineConfig(({ mode }) => {
  const envDir = path.resolve(__dirname, '..')
  const env = loadEnv(mode, envDir)

  return {
    envDir,
    server: {
      port: Number(env.VITE_PORT || env.FRONTEND_PORT) || 4173,
    },
  }
})
