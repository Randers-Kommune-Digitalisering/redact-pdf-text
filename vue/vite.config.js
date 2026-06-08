import { fileURLToPath, URL } from 'node:url'
const path = require('path')

const VUE_PORT = process.env.VUE_PORT || 3000
const BACKEND_PORT = process.env.BACKEND_PORT || 8080

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://router.vuejs.org/guide/essentials/navigation.html
// https://vueschool.io/lessons/the-scaffolded-codebase-vite-only

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    port: VUE_PORT,
    watch: {
      usePolling: process.env.CHOKIDAR_USEPOLLING === 'true',
    },
    proxy: {
      '/api/': {
        target: 'http://localhost:' + BACKEND_PORT + '/',
        changeOrigin: true
      }
    }
  },
  preview: {
    port: VUE_PORT,
    host: true,
    proxy: {
      '/api/': {
        target: 'http://localhost:' + BACKEND_PORT + '/',
        changeOrigin: true
      }
    }
  },
  plugins: [
    vue(),
  ],
  define: {
    APP_VERSION: JSON.stringify(process.env.npm_package_version),
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})