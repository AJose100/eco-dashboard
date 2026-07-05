<template>
  <div :class="{ 'dark': isDark }">
    <div class="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100 p-6 lg:p-8 transition-colors duration-300">
      
      <!-- Cabeçalho -->
      <header class="flex flex-col md:flex-row justify-between items-center mb-10 max-w-6xl mx-auto gap-4">
        <div>
          <h1 class="text-3xl font-extrabold text-green-600 dark:text-green-400">EcoDashboard 🌱</h1>
          <p class="text-sm text-gray-500 dark:text-gray-400 mt-1" v-if="store.dashboardData">
            Painel de Controle Sustentável de {{ store.dashboardData.user_name }}
          </p>
        </div>
        <div class="flex gap-3">
          <button @click="store.downloadPdfReport" class="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg shadow-md transition-all flex items-center gap-2">
            Baixar PDF
          </button>
          <button @click="toggleDark" class="px-5 py-2.5 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:bg-gray-100 dark:hover:bg-gray-700 font-medium rounded-lg shadow-sm transition-all flex items-center gap-2">
            {{ isDark ? '☀️ Claro' : '🌙 Escuro' }}
          </button>
        </div>
      </header>

      <main class="max-w-6xl mx-auto space-y-8">
        
        <!-- PARTE SUPERIOR: Dashboard Original -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div class="lg:col-span-2 space-y-6" v-if="store.dashboardData">
            <!-- Card de Progresso -->
            <div class="p-6 bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl shadow-sm">
              <div class="flex justify-between items-end mb-4">
                <div>
                  <h3 class="text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">Consumo Acumulado</h3>
                  <div class="flex items-baseline gap-2 mt-1">
                    <span class="text-5xl font-black text-gray-800 dark:text-white">{{ store.dashboardData.total_consumption }}</span>
                    <span class="text-xl text-gray-500 font-medium">/ {{ store.dashboardData.current_goal }} kWh</span>
                  </div>
                </div>
                <div class="text-right">
                  <span class="text-sm font-bold" :class="percentual > 100 ? 'text-red-500' : 'text-green-500'">
                    {{ percentual }}% da Meta
                  </span>
                </div>
              </div>
              <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 mb-2 overflow-hidden">
                <div class="h-3 rounded-full transition-all duration-1000 ease-out" 
                     :class="percentual > 100 ? 'bg-red-500' : 'bg-green-500'" 
                     :style="{ width: Math.min(percentual, 100) + '%' }">
                </div>
              </div>
            </div>
            
            <!-- Dica da IA Geral -->
            <div class="p-5 rounded-2xl border flex gap-4 items-start shadow-sm"
                 :class="percentual > 100 ? 'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800' : 'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800'">
              <div class="text-2xl mt-1">💡</div>
              <div>
                <h3 class="font-bold mb-1" :class="percentual > 100 ? 'text-red-800 dark:text-red-400' : 'text-green-800 dark:text-green-400'">Assistente Virtual Inteligente</h3>
                <p class="text-sm leading-relaxed" :class="percentual > 100 ? 'text-red-900 dark:text-red-200' : 'text-green-900 dark:text-green-200'">
                  {{ store.dashboardData.ai_tip }}
                </p>
              </div>
            </div>

            <!-- Gráfico -->
            <div class="p-6 bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl shadow-sm">
              <h2 class="text-lg font-bold mb-4">Histórico Mensal</h2>
              <EnergyChart />
            </div>
          </div>

          <!-- Coluna Direita -->
          <div class="space-y-6">
            <!-- Nova Leitura Geral -->
            <div class="p-6 bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl shadow-sm">
              <h2 class="text-lg font-bold mb-4">⚡ Registrar Fatura Total</h2>
              <form @submit.prevent="handleSubmit" class="space-y-4">
                <input type="number" v-model.number="newValue" step="0.1" required class="w-full p-3 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-xl outline-none" placeholder="Valor em kWh" />
                <button type="submit" class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-xl shadow-md transition-all">Adicionar Leitura</button>
              </form>
            </div>

            <!-- Badges -->
            <div class="p-6 bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl shadow-sm" v-if="store.dashboardData">
              <h2 class="text-lg font-bold mb-4">🏅 Conquistas</h2>
              <div class="flex flex-col gap-3">
                <div v-for="badge in store.dashboardData.badges" :key="badge" class="flex items-center gap-3 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 p-3 rounded-xl">
                  <span class="text-2xl">🏆</span> 
                  <span class="font-bold text-amber-800 dark:text-amber-500">{{ badge }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <hr class="border-gray-200 dark:border-gray-700" />

        <!-- NOVA SEÇÃO: CALCULADORA DE APARELHOS -->
        <div class="space-y-6">
          <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
            <div>
              <h2 class="text-2xl font-bold text-gray-800 dark:text-white">🔌 Calculadora de Aparelhos</h2>
              <p class="text-gray-500 dark:text-gray-400">Descubra quanto cada aparelho custa na sua fatura.</p>
            </div>
            
            <!-- SELETOR DE BANDEIRA TARIFÁRIA -->
            <div class="bg-white dark:bg-gray-800 p-3 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
              <label class="block text-xs font-bold text-gray-500 uppercase tracking-wider mb-1">Bandeira Tarifária do Mês</label>
              <select v-model="tarifaAtual" class="w-full bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg p-2 outline-none font-medium focus:ring-2 focus:ring-green-500">
                <option :value="0.70">🟩 Verde (Tarifa Base ~R$ 0,70/kWh)</option>
                <option :value="0.72">🟨 Amarela (+ R$ 0,018/kWh)</option>
                <option :value="0.75">🟥 Vermelha Patamar 1 (+ R$ 0,044/kWh)</option>
                <option :value="0.78">🟥 Vermelha Patamar 2 (+ R$ 0,078/kWh)</option>
              </select>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Formulário de Aparelho -->
            <div class="lg:col-span-1 p-6 bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl shadow-sm h-fit">
              <h3 class="font-bold mb-4">Adicionar Aparelho</h3>
              <form @submit.prevent="addAppliance" class="space-y-5">
                <div>
                  <label class="block text-sm font-medium mb-1">Nome (Ex: Chuveiro Elétrico)</label>
                  <input type="text" v-model="newAppliance.nome" required class="w-full p-2.5 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg outline-none focus:ring-2 focus:ring-green-500" />
                </div>
                
                <div>
                  <label class="block text-sm font-medium mb-1">Potência em Watts (W)</label>
                  <input type="number" v-model.number="newAppliance.potencia_w" required placeholder="Ex: 5500" class="w-full p-2.5 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg outline-none focus:ring-2 focus:ring-green-500" />
                  <!-- DICA DE COMO ACHAR A POTÊNCIA -->
                  <div class="mt-2 bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg border border-blue-100 dark:border-blue-800">
                    <p class="text-xs text-blue-800 dark:text-blue-300 leading-relaxed">
                      <strong>🔍 Como achar a potência?</strong><br/>
                      Olhe a etiqueta atrás/embaixo do aparelho ou no manual. Procure por um número com <strong>"W"</strong> (Ex: 1500W). <br/>
                      <em>Truque:</em> Se tiver apenas Tensão (V) e Corrente (A), multiplique os dois: <strong>127V x 10A = 1270W</strong>.
                    </p>
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium mb-1">Horas de uso por dia</label>
                  <input type="number" v-model.number="newAppliance.horas_dia" step="0.1" required placeholder="Ex: 0.5 (30 min)" class="w-full p-2.5 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg outline-none focus:ring-2 focus:ring-green-500" />
                </div>
                <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg transition-all shadow-md">Calcular Custo</button>
              </form>
            </div>

            <!-- Lista de Aparelhos Cadastrados -->
            <div class="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-4">
              <div v-if="appliances.length === 0" class="col-span-full p-8 text-center text-gray-500 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-2xl">
                Nenhum aparelho registrado ainda. Adicione o seu primeiro!
              </div>
              
              <div v-for="appliance in appliances" :key="appliance.id" class="p-5 bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-xl shadow-sm relative overflow-hidden">
                <div class="absolute top-0 right-0 bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 text-xs font-bold px-3 py-1 rounded-bl-lg" v-if="appliance.consumo_mensal_kwh > 30">
                  Alto Consumo
                </div>
                
                <h4 class="font-bold text-lg mb-1">{{ appliance.nome }}</h4>
                <div class="text-sm text-gray-500 dark:text-gray-400 mb-3">
                  {{ appliance.potencia_w }}W • {{ appliance.horas_dia }}h/dia
                </div>
                
                <!-- MOSTRADOR DE KWH E PREÇO DINÂMICO -->
                <div class="flex items-baseline gap-2 mb-1">
                  <span class="text-2xl font-black text-gray-800 dark:text-white">{{ appliance.consumo_mensal_kwh }}</span>
                  <span class="text-sm font-medium text-gray-500">kWh/mês</span>
                </div>
                <div class="text-lg font-bold text-green-600 dark:text-green-400 mb-4">
                  💸 Estimativa: R$ {{ (appliance.consumo_mensal_kwh * tarifaAtual).toFixed(2).replace('.', ',') }}
                </div>

                <div class="bg-blue-50 dark:bg-blue-900/20 text-blue-800 dark:text-blue-300 p-3 rounded-lg text-sm border border-blue-100 dark:border-blue-800">
                  {{ appliance.dica }}
                </div>
              </div>
            </div>
          </div>
        </div>

      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useConsumptionStore } from '../stores/consumption'
import EnergyChart from '../components/EnergyChart.vue'

const store = useConsumptionStore()
const isDark = ref(false)
const newValue = ref('')

// Controle de Aparelhos e Tarifa
const appliances = ref([])
const newAppliance = ref({ nome: '', potencia_w: null, horas_dia: null })
const tarifaAtual = ref(0.70) // Começa na Bandeira Verde como padrão

const percentual = computed(() => {
  if (!store.dashboardData) return 0
  return Math.round((store.dashboardData.total_consumption / store.dashboardData.current_goal) * 100)
})

const toggleDark = () => {
  isDark.value = !isDark.value
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

const handleSubmit = async () => {
  if (newValue.value <= 0) return
  await store.addReading({ value: newValue.value })
  newValue.value = ''
  store.fetchDashboard()
}

const fetchAppliances = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/appliances/')
    appliances.value = await res.json()
  } catch (error) {
    console.error("Erro ao buscar aparelhos", error)
  }
}

const addAppliance = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/appliances/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newAppliance.value)
    })
    if (res.ok) {
      newAppliance.value = { nome: '', potencia_w: null, horas_dia: null }
      fetchAppliances() 
    }
  } catch (error) {
    console.error("Erro ao adicionar", error)
  }
}

onMounted(() => {
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
  }
  store.fetchDashboard()
  fetchAppliances() 
})
</script>   