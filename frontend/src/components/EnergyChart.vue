<template>
  <div class="chart-container mt-6" aria-label="Gráfico de consumo de energia dos últimos meses" tabindex="0">
    <table class="sr-only">
      <caption>Consumo de Energia por Mês</caption>
      <thead>
        <tr>
          <th scope="col">Mês</th>
          <th scope="col">Consumo em kWh</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="data in chartData" :key="data.month">
          <td>{{ data.month }}</td>
          <td>{{ data.value }}</td>
        </tr>
      </tbody>
    </table>
    
    <canvas ref="chartCanvas" aria-hidden="true"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useConsumptionStore } from '../stores/consumption'
import Chart from 'chart.js/auto'

const chartCanvas = ref(null)
let chartInstance = null
const consumptionStore = useConsumptionStore()

// Computa os dados diretamente vindos da API através do Pinia
const chartData = computed(() => {
  return consumptionStore.dashboardData?.chart_data || []
})

const renderChart = () => {
  if (chartInstance) {
    chartInstance.destroy() // Destrói o gráfico antigo antes de redesenhar com novos dados
  }
  
  if (!chartCanvas.value || chartData.value.length === 0) return

  chartInstance = new Chart(chartCanvas.value, {
    type: 'bar',
    data: {
      labels: chartData.value.map(d => d.month),
      datasets: [{
        label: 'Consumo (kWh)',
        data: chartData.value.map(d => d.value),
        backgroundColor: '#4CAF50',
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } }
    }
  })
}

// Fica de olho se os dados da API mudaram para re-renderizar o gráfico na tela
watch(chartData, () => {
  renderChart()
}, { deep: true })

onMounted(() => {
  renderChart()
})
</script>

<style scoped>
.sr-only {
  position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; 
  overflow: hidden; clip: rect(0, 0, 0, 0); border: 0;
}
.chart-container:focus-visible {
  outline: 3px solid #FF9800;
  outline-offset: 4px;
  border-radius: 8px;
}
</style>