import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const chatTarget = process.env.VITE_CHAT_TARGET || 'https://ec2-13-229-209-181.ap-southeast-1.compute.amazonaws.com'

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
