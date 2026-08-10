import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const chatTarget = process.env.VITE_CHAT_TARGET || ''

export default defineConfig({
  plugins: [react()],
  base: '/repo-dashboard/',
  server: {
    proxy: {
      '/chat': {
        target: chatTarget,
        changeOrigin: true,
        secure: true
      }
    }
  }
})
