<template>
  <div>
    <div v-if="lotSummary.length" class="chart-container">
      <canvas ref="chartCanvas"></canvas>
    </div>
    <p v-else class="text-center text-muted">No reservation data to display.</p>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import Chart from 'chart.js/auto'

export default {
  name: 'AdminChart',
  props: {
    lotSummary: {
      type: Array,
      required: true
    }
  },
  setup(props) {
    const chartCanvas  = ref(null)
    let chartInstance = null

    const renderChart = () => {
      if (!props.lotSummary.length) return
      if (chartInstance) chartInstance.destroy()

      const labels = props.lotSummary.map(i => i.name)
      const data   = props.lotSummary.map(i => i.reserved)

      chartInstance = new Chart(chartCanvas.value.getContext('2d'), {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            data,
            backgroundColor: '#0d6efd'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false }, ticks: { maxRotation: 0 } },
            y: { grid: { color: '#eee' }, ticks: { stepSize: 1 } }
          }
        }
      })
    }

    onMounted(renderChart)
    watch(() => props.lotSummary, renderChart)

    return { chartCanvas }
  }
}
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 250px;        /* cap the height */
  margin-bottom: 1.5rem;
}
</style>
