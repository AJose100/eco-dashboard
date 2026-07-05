<template>
  <div :class="{ 'dark': isDark }">
    <div class="min-h-screen bg-gray-50 dark:bg-gray-900 text-black dark:text-white p-8 font-sans transition-colors duration-200">
      
      <header class="flex justify-between items-center mb-8 max-w-5xl mx-auto">
        <div>
          <h1 class="text-3xl font-extrabold text-green-700 dark:text-green-400">EcoDashboard</h1>
          <p class="text-sm text-gray-500 dark:text-gray-400" v-if="store.dashboardData">
            Bem-vinda de volta, {{ store.dashboardData.user_name }}!
          </p>
        </div>
        <div class="flex gap-4">
          <button @click="store.downloadPdfReport" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded shadow transition-colors cursor-pointer">
            📥 Baixar PDF
          </button>
          <button @click="toggleDark" class="px-4 py-2 bg-gray-200 dark:bg-gray-700 font-semibold rounded shadow hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors cursor-pointer">
            {{ isDark ? '☀️ Modo Claro' : '🌙 Modo Escuro' }}
          </button>
        </div>
      </header>

      <main class="max-w-5xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- Coluna da Esquerda e Central: Gráficos e Dados -->
        <div class="lg:col-span-2 space-y-6">
          <div v-if="store.loading" class="text-center p-12 bg-white dark:bg-gray-800 rounded-xl shadow-sm">
            <p class="text-xl font-semibold">Carregando dados sustentáveis...</p>
          </div>

          <div v-else-if="store.dashboardData" class="space-y-6">
            <!-- Cards Principais -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="p-6 bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-xl shadow-sm">
                <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Consumo Atual</h3>
                <p class="text-4xl font-bold text-gray-800 dark:text-gray-100">
                  {{ store.dashboardData.total_consumption }} <span class="text-xl font-normal text-gray-500">kWh</span>
                </p>
                <span class="text-xs text-amber-600 bg-amber-50 dark:bg-amber-900/20 px-2 py-0.5 rounded font-medium mt-2 inline-block">
                  Meta estabelecida: {{ store.dashboardData.current_goal }} kWh
                </span>
              </div>
              
              <div class="p-6 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800/60 rounded-xl shadow-sm">
                <h3 class="text-sm font-semibold text-green-800 dark:text-green-400 mb-1">💡 Dica Inteligente da IA</h3>
                <p class="text-sm text-green-900 dark:text-green-200 leading-relaxed">
                  {{ store.dashboardData.ai_tip }}
                </p>
              </div>
            </div>

            <!-- Gráfico -->
            <div class="p-6 bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-xl shadow-sm">
              <h2 class="text-xl font-bold mb-1 text-gray-800 dark:text-gray-100">Histórico de Consumo</h2>
              <PeriodSelector />
              <EnergyChart />
            </div>
          </div>
        </div>

        <!-- Coluna da Direita: Formulário e Conquistas (Gamificação) -->
        <div class="space-y-6">
          <!-- Formulário de Inserção -->
          <div class="p-6 bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-xl shadow-sm">
            <h2 class="text-lg font-bold mb-4 text-gray-800 dark:text-gray-100">Registrar Consumo</h2>
            <form @submit.prevent="handleSubmit" class="space-y-4">
              <div>
                <label class="block text-sm font-medium mb-1 text-gray-600 dark:text-gray-400">Gasto Energético (kWh)</label>
                <input 
                  type="number" 
                  v-model.number="newValue" 
                  step="0.1" 
                  required
                  class="w-full p-2.5 border rounded-lg bg-gray-50 dark:bg-gray-700 dark:border-gray-600 focus:ring-2 focus:ring-green-500 outline-none text-black dark:text-white"
                  placeholder="Ex: 115.5"
                />
              </div>
              <button type="submit" class="w-full bg-green-600 hover:bg-green-700 text-white font-medium py-2.5 px-4 rounded-lg transition-colors cursor-pointer">
                Salvar Registro
              </button>
            </form>
            <p v-if="successMessage" class="mt-2 text-sm text-green-600 font-medium">{{ successMessage }}</p>
          </div>

          <!-- Muro de Badges Conquistados -->
          <div class="p-6 bg-white dark:bg-gray-800 border dark:border-gray-700 rounded-xl shadow-sm" v-if="store.dashboardData">
            <h2 class="text-lg font-bold mb-3 text-gray-800 dark:text-gray-100">🏅 Minhas Conquistas</h2>
            <div class="flex flex-wrap gap-2">
              <div 
                v-for="badge in store.dashboardData.badges" 
                :key="badge" 
                class="badge-item bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300 text-xs font-bold px-3 py-2 rounded-full border border-yellow-300/50 flex items-center gap-1.5"
              >
                <span>🏆</span> {{ badge }}
              </div>
            </div>
          </div>
        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useConsumptionStore } from '../stores/consumption'
import EnergyChart from '../components/EnergyChart.vue'
import PeriodSelector from '../components/PeriodSelector.vue'

const store = useConsumptionStore()
const isDark = ref(false)
const newValue = ref('')
const successMessage = ref('')

const toggleDark = () => {
  isDark.value = !isDark.value
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

const handleSubmit = async () => {
  if (newValue.value <= 0) return
  
  const payload = {
    property_id: 1,
    source_id: 1,
    reading_date: new Date().toISOString().split('T')[0], // Data de hoje no formato YYYY-MM-DD
    value: newValue.value
  }
  
  try {
    await store.addReading(payload)
    successMessage.value = 'Leitura registrada com sucesso!'
    newValue.value = ''
    setTimeout(() => successMessage.value = '', 4000)
  } catch (err) {
    alert('Erro ao registrar dados no servidor.')
  }
}

onMounted(() => {
  // Lendo preferências de tema
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
  }
  
  // Dispara a requisição para buscar os dados reais do back-end
  store.fetchDashboard()
})
</script>

<style scoped>
@keyframes popIn {
  0% { transform: scale(0.8); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
.badge-item {
  animation: popIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) both;
}
</style>