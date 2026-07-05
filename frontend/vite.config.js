import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import { VitePWA } from 'vite-plugin-pwa' // 1. Importação do plugin

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    // 2. Configuração do PWA
    VitePWA({
      registerType: 'autoUpdate',
      manifest: {
        name: 'EcoDashboard Sustentável',
        short_name: 'EcoDashboard',
        description: 'Gerencie seu consumo de energia e reduza custos',
        theme_color: '#059669', // Cor do seu tema verde
        icons: [
          {
            src: '/pwa-192x192.png', // Lembre-se de colocar esses arquivos na pasta 'public'
            sizes: '192x192',
            type: 'image/png'
          },
          {
            src: '/pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png'
          }
        ]
      }
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
