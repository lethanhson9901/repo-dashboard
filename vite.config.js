import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/repo-dashboard/',
  server: {
    proxy: {
      '/chat': {
        target: 'https://ec2-13-229-209-181.ap-southeast-1.compute.amazonaws.com',
        changeOrigin: true,
        secure: false
      }
    }
  }
})
