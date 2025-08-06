<template>
  <!-- 1) Loading State -->
  <div v-if="loading" class="loader-container">
    <div class="spinner-border text-primary" role="status"></div>
    <p class="loader-text">Loading summary…</p>
  </div>

  <!-- 2) Error State -->
  <div v-else-if="error" class="alert alert-danger text-center mt-4">
    {{ error }}
  </div>

  <!-- 3) Main Content -->
  <div v-else class="dashboard-wrapper">
    <UserNavbar :username="displayName" />

    <div class="scroll-area">
      <h2 class="section-title mb-4">Monthly Summary</h2>

      <!-- metrics at top, side by side -->
      <div class="metrics-container">
        <div class="metric-box">
          <p class="metric-value">{{ totalReservations }}</p>
          <p class="metric-label">Total Reservations</p>
        </div>
        <div class="metric-box">
          <p class="metric-value">{{ totalHours.toFixed(1) }}</p>
          <p class="metric-label">Total Hours Parked</p>
        </div>
        <div class="metric-box">
          <p class="metric-value">₹{{ totalCost.toFixed(2) }}</p>
          <p class="metric-label">Total Amount Spent</p>
        </div>
        <div class="metric-box">
          <p class="metric-value">{{ frequentLot || 'N/A' }}</p>
          <p class="metric-label">Most Frequent Lot</p>
        </div>
      </div>

      <!-- chart below -->
      <div class="chart-card">
        <h5 class="chart-title">Times Parked by Lot</h5>
        <div class="chart-container small-chart">
          <canvas ref="timesChart"></canvas>
        </div>
        <div class="text-center mt-4">
          <button class="btn btn-outline-success" @click="exportCSV">
            📦 Download Reservation History (CSV)
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios'
import UserNavbar from '../components/UserNavbar.vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  name: 'UserSummary',
  components: { UserNavbar },

  data() {
    return {
      user: null,
      dataByLot: [],
      chart: null,
      loading: true,
      error: ''
    }
  },

  computed: {
    displayName() {
      return this.user?.fullname
        || this.user?.username
        || this.user?.email
        || 'User'
    },
    totalReservations() {
      return this.dataByLot.reduce((sum, l) => sum + (l.times_parked || 0), 0)
    },
    totalHours() {
      const mins = this.dataByLot.reduce((sum, l) => sum + (l.total_time_minutes || 0), 0)
      return mins / 60
    },
    totalCost() {
      return this.dataByLot.reduce((sum, l) => sum + (l.total_cost || 0), 0)
    },
    frequentLot() {
      if (!this.dataByLot.length) return ''
      return this.dataByLot
        .slice()
        .sort((a, b) => (b.times_parked || 0) - (a.times_parked || 0))[0]
        .lot_name
    }
  },

  watch: {
    dataByLot(newVal) {
      if (newVal.length) this.$nextTick(this.renderChart)
    }
  },

  methods: {

    exportCSV() {
      const token = localStorage.getItem('token') || localStorage.getItem('access_token');
      fetch("http://localhost:5000/user/export-history", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      })
        .then(res => res.json())
        .then(data => {
          alert(data.msg || "Export started. Check your email soon.");
        })
        .catch(err => {
          console.error(err);
          alert("Failed to trigger CSV export.");
        });
    },
    renderChart() {
      const canvas = this.$refs.timesChart
      if (!canvas) return
      const ctx = canvas.getContext('2d')
      if (!ctx) return

      if (this.chart) {
        this.chart.destroy()
        this.chart = null
      }

      const labels = this.dataByLot.map(l => l.lot_name)
      const data = this.dataByLot.map(l => l.times_parked)

      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels,
          datasets: [{
            data,
            backgroundColor: '#0d6efd'
          }]
        },
        options: {
          animation: false,
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              ticks: { precision: 0 }
            }
          },
          plugins: { legend: { display: false } }
        }
      })
    }
  },

  async mounted() {
    const token = localStorage.getItem('token') || localStorage.getItem('access_token')
    if (!token) {
      this.$router.push('/login')
      return
    }

    try {
      const [sumRes, userRes] = await Promise.all([
        axios.get('http://localhost:5000/user/summary', {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get('http://localhost:5000/user/dashboard', {
          headers: { Authorization: `Bearer ${token}` }
        })
      ])

      this.dataByLot = Array.isArray(sumRes.data.summary)
        ? sumRes.data.summary
        : Array.isArray(sumRes.data)
          ? sumRes.data
          : []

      this.user = userRes.data

      if (this.dataByLot.length) this.$nextTick(this.renderChart)
    }
    catch (err) {
      console.error(err)
      if (err.response?.status === 401) {
        localStorage.clear()
        this.$router.push('/login')
      } else {
        this.error = 'Failed to load summary.'
      }
    }
    finally {
      this.loading = false
    }
  }
}
</script>

<style scoped>
.dashboard-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.scroll-area {
  flex: 1;
  overflow-y: auto;
  padding: 2rem 1.5rem;
}

/* Loader */
.loader-container {
  text-align: center;
  margin-top: 4rem;
}

.loader-text {
  margin-top: .75rem;
  font-size: .95rem;
  color: #666;
}

.chart-container.small-chart {
  max-width: 500px;   /* control width */
  height: 250px;      /* control height */
  margin: 0 auto;     /* center it */
}

/* Section Title */
.section-title {
  color: #000;
  font-size: 1.75rem;
  font-weight: 700;
  text-align: left;
  margin-bottom: 1.5rem;
}

/* metrics row */
.metrics-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.metric-box {
  background: #fff;
  border-radius: .5rem;
  border-left: 6px solid #0d6efd;
  padding: 1rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
  text-align: center;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  margin: 0;
}

.metric-label {
  font-size: .9rem;
  color: #555;
  margin: .25rem 0 0;
}

/* Chart Card */
.chart-card {
  background: #fff;
  border-radius: .5rem;
  padding: 1.5rem;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.08);
}

.chart-title {
  margin-bottom: 1rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #333;
}

.chart-container {
  position: relative;
  height: 300px;
}

/* Responsive */
@media (max-width: 768px) {
  .section-title {
    text-align: center;
  }
}
</style>
