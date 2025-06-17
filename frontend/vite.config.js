import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/upload_file': {
        target: 'https://super-duper-winner-7vvjj4p6q756crqwr-8000.app.github.dev',
        changeOrigin: true,
        secure: false,
      },
      '/reports': {
        target: 'https://super-duper-winner-7vvjj4p6q756crqwr-8000.app.github.dev',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})
