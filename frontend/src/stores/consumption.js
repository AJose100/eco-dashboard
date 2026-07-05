import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://localhost:8000'

export const useConsumptionStore = defineStore('consumption', {
  state: () => ({
    dashboardData: null,
    loading: false,
    error: null
  }),
  
  actions: {
    async fetchDashboard(propertyId = 1) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${API_URL}/dashboard/${propertyId}`)
        this.dashboardData = response.data
      } catch (err) {
        this.error = 'Erro ao carregar dados do servidor.'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    
    async addReading(readingData) {
      try {
        await axios.post(`${API_URL}/readings/`, readingData)
        // Recarrega o dashboard para trazer os dados atualizados e checar novos badges
        await this.fetchDashboard()
      } catch (err) {
        console.error('Erro ao enviar nova leitura:', err)
        throw err
      }
    },
    
    async downloadPdfReport() {
      try {
        const response = await axios.get(`${API_URL}/report/download`, { responseType: 'blob' })
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'relatorio_sustentavel.pdf')
        document.body.appendChild(link)
        link.click()
        link.remove()
      } catch (err) {
        console.error('Erro ao baixar o PDF:', err)
      }
    }
  }
})