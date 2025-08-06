<template>
  <div class="dashboard-wrapper">
<UserNavbar v-if="user && user.username" :username="user.username" />

    <div class="scroll-area">
      <div v-if="loading" class="loader-container">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="loader-text">Loading reservations…</p>
      </div>

      <div v-else-if="error" class="alert alert-danger text-center mt-4">
        {{ error }}
      </div>

      <section v-else>
        <h2 class="section-title">Your Reservations</h2>

        <!-- Active Reservations -->
        <h4 class="sub-title">Active Reservations</h4>
        <div v-if="activeReservations.length" class="cards-grid">
          <div
            v-for="r in activeReservations"
            :key="r.reservation_id"
            class="reservation-card"
          >
            <div class="card-header">
              <div class="header-text">
                <h5 class="lot-name">{{ r.lot_name }}</h5>
                <small class="lot-address">{{ r.lot_address }}</small>
              </div>
              <button
                class="btn btn-sm btn-warning"
                @click="releaseSpot(r.reservation_id)"
              >
                Release
              </button>
            </div>
            <div class="card-body">
              <div class="info"><strong>Spot:</strong> #{{ r.spot_number }}</div>
              <div class="info"><strong>Vehicle:</strong> {{ r.vehicle_number }}</div>
              <div class="info"><strong>Start:</strong> {{ formatDateIST(r.start_time) }}</div>
              <div class="info">
                <strong>End:</strong>
                {{ r.end_time ? formatDateIST(r.end_time) : 'Ongoing' }}
              </div>
            </div>
          </div>
        </div>
        <p v-else class="no-reservations">
          You have no active reservations.
        </p>

        <!-- Parked Out Reservations -->
        <h4 class="sub-title mt-4">Parked Out</h4>
        <div v-if="parkedOutReservations.length" class="cards-grid">
          <div
            v-for="r in parkedOutReservations"
            :key="r.reservation_id"
            class="reservation-card parked-out"
          >
            <div class="card-header">
              <div class="header-text">
                <h5 class="lot-name">{{ r.lot_name }}</h5>
                <small class="lot-address">{{ r.lot_address }}</small>
              </div>
            </div>
            <div class="card-body">
              <div class="info"><strong>Spot:</strong> #{{ r.spot_number }}</div>
              <div class="info"><strong>Vehicle:</strong> {{ r.vehicle_number }}</div>
              <div class="info"><strong>Start:</strong> {{ formatDateIST(r.start_time) }}</div>
              <div class="info"><strong>End:</strong> {{ formatDateIST(r.end_time) }}</div>
            </div>
          </div>
        </div>
        <p v-else class="no-reservations">
          You have no past reservations.
        </p>
      </section>
    </div>

    <!-- Release Modal -->
    <div
      class="release-modal"
      v-if="showReleaseModal"
      @click.self="showReleaseModal = false"
    >
      <div class="modal-dialog">
        <div class="modal-content shadow rounded-4">
          <div class="modal-header bg-dark text-white px-4 py-3">
            <h5 class="modal-title fw-semibold">Release Reservation</h5>
            <button
              type="button"
              class="btn-close btn-close-white"
              @click="showReleaseModal = false"
            ></button>
          </div>

          <div class="modal-body px-4 py-3">
            <div class="mb-3">
              <div
                class="d-flex justify-content-between align-items-center mb-2"
              >
                <span class="text-muted">Parking Lot</span>
                <strong>{{ activeReservation.lot_name }}</strong>
              </div>
              <div
                class="d-flex justify-content-between align-items-center mb-2"
              >
                <span class="text-muted">Spot Number</span>
                <strong>#{{ activeReservation.spot_number }}</strong>
              </div>
              <div
                class="d-flex justify-content-between align-items-center mb-2"
              >
                <span class="text-muted">Vehicle Number</span>
                <strong>{{ activeReservation.vehicle_number }}</strong>
              </div>
              <div
                class="d-flex justify-content-between align-items-center mb-2"
              >
                <span class="text-muted">Start Time</span>
                <strong>{{ formatDateIST(activeReservation.start_time) }}</strong>
              </div>
              <div
                class="d-flex justify-content-between align-items-center mb-2"
              >
                <span class="text-muted">Release Time</span>
                <strong>{{ currentIST }}</strong>
              </div>
              <div
                class="d-flex justify-content-between align-items-center mb-0"
              >
                <span class="text-muted">Estimated Cost</span>
                <strong class="text-success">
                  {{ formattedCost }}
                  <small v-if="releaseResult.cost !== null">(actual)</small>
                  <small v-else>(est.)</small>
                </strong>
              </div>
            </div>
          </div>

          <div
            class="modal-footer bg-light px-4 py-3 d-flex justify-content-between"
          >
            <button
              class="btn btn-outline-dark"
              @click="showReleaseModal = false"
            >
              Cancel
            </button>
            <button
              class="btn btn-warning px-4"
              @click="confirmRelease"
            >
              Release
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showReleaseModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import axios from 'axios'
import UserNavbar from '../components/UserNavbar.vue'
import { DateTime } from 'luxon'

export default {
  name: 'UserReservations',
  components: { UserNavbar },

  data() {
    return {
      user: { username: '' },
      loading: true,
      error: '',
      showReleaseModal: false,
      activeReservation: null,
      releaseResult: {
        cost: null,
        duration: null
      }
    }
  },

  computed: {
    currentIST() {
      return DateTime.now()
        .setZone('Asia/Kolkata')
        .toFormat('M/d/yyyy, h:mm a')
    },

    // Raw estimate: at least 1 hour × price_per_hour
    estimatedCostRaw() {
      if (!this.activeReservation) return 0
      const startUTC = DateTime.fromISO(this.activeReservation.start_time, {
        zone: 'utc'
      })
      const nowUTC = DateTime.now().toUTC()
      const diffHours = nowUTC.diff(startUTC, 'hours').hours
      const billedHrs = Math.ceil(diffHours)
      return billedHrs * this.activeReservation.price_per_hour
    },

    // Display actual cost if available, else estimate, formatted as ₹
    formattedCost() {
      const raw = this.releaseResult.cost != null
        ? this.releaseResult.cost
        : this.estimatedCostRaw

      return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0
      }).format(raw)
    },

    activeReservations() {
      return this.user?.reservations?.filter(r => !r.end_time) || []
    },

    parkedOutReservations() {
      return this.user?.reservations?.filter(r => r.end_time) || []
    }
  },

  methods: {
    async fetchReservations() {
      this.loading = true
      try {
        const res = await axios.get(
          'http://localhost:5000/user/dashboard',
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem(
                'token'
              )}`
            }
          }
        )
        this.user = res.data
      } catch (err) {
        console.error(err)
        if (err.response?.status === 401) {
          this.error = 'Session expired. Please log in again.'
          localStorage.clear()
          this.$router.push('/login')
        } else {
          this.error = 'Failed to load reservations.'
        }
      } finally {
        this.loading = false
      }
    },

    formatDateIST(dateStr) {
      if (!dateStr) return 'Ongoing'
      return DateTime.fromISO(dateStr, { zone: 'utc' })
        .setZone('Asia/Kolkata')
        .toFormat('M/d/yyyy, h:mm a')
    },

    releaseSpot(reservationId) {
      const reservation = this.user.reservations.find(
        r => r.reservation_id === reservationId
      )
      if (reservation) {
        this.activeReservation = {
          ...reservation,
          price_per_hour: reservation.price_per_hour || 0
        }
        this.releaseResult = { cost: null, duration: null }
        this.showReleaseModal = true
      }
    },

    async confirmRelease() {
      try {
        const endTimeUTC = DateTime.now().toUTC().toISO()
        const res = await axios.post(
          'http://localhost:5000/user/release',
          {
            reservation_id: this.activeReservation.reservation_id,
            end_time: endTimeUTC
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem(
                'token'
              )}`
            }
          }
        )

        this.releaseResult.cost = res.data.cost
        this.releaseResult.duration = res.data.duration

        // Optionally keep modal open to show actual cost, or close and refresh
        this.showReleaseModal = false
        await this.fetchReservations()
      } catch (err) {
        console.error(err)
        alert(err.response?.data?.msg || 'Failed to release spot.')
      }
    }
  },

  mounted() {
    this.fetchReservations()
  }
}
</script>



<style scoped>
.dashboard-wrapper {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg);
  color: var(--text);
}

.scroll-area {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1.5rem 2rem;
}

/* Section Title */
.section-title {
  position: relative;
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--primary);
  text-align: center;
  margin-bottom: 1.5rem;
}

.section-title::after {
  content: '';
  display: block;
  width: 60px;
  height: 4px;
  margin: 8px auto 0;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  border-radius: 2px;
}

/* Sub-title */
.sub-title {
  position: relative;
  font-size: 1.25rem;
  margin-bottom: 1rem;
  padding-left: 12px;
  color: var(--text);
}

.sub-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 4px;
  width: 4px;
  height: calc(100% - 8px);
  background: var(--primary);
  border-radius: 2px;
}

/* Loader */
.loader-container {
  text-align: center;
  margin-top: 2rem;
}

.loader-text {
  margin-top: 0.75rem;
  font-size: 0.95rem;
  color: var(--secondary);
}

/* Card Grid */
.cards-grid {
  display: grid;
  gap: 1rem;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  margin-bottom: 2rem;
}

/* Reservation Card */
.reservation-card {
  background: #fff;
  border-left: 4px solid var(--primary);
  border-radius: 0.5rem;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.reservation-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
}

.reservation-card.parked-out {
  border-left-color: var(--secondary);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(0, 0, 0, 0.03);
  padding: 1rem;
  border-bottom: 1px solid #e9ecef;
}

.header-text h5 {
  margin: 0;
  font-size: 1.125rem;
}

.header-text small {
  color: #6c757d;
}

.card-body {
  padding: 1rem;
}

.info {
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.btn-warning {
  background-color: #ffc107;
  border: none;
}

.btn-warning:hover {
  background-color: #e0a800;
}

/* Add this to your styles */
.dashboard-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  overflow-x: hidden; /* Prevent horizontal scroll during transitions */
}

.scroll-area {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem 2rem;
  width: 100%; /* Ensure consistent width */
}

.no-reservations {
  text-align: center;
  color: #6c757d;
  font-size: 1rem;
  margin-top: 3rem;
}

/* Modal Overlay */
.release-modal {
  position: fixed;
  inset: 0;
  z-index: 2000;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.release-modal .modal-dialog {
  max-width: 500px;
  width: 100%;
  margin: 0;
  border-radius: 1rem;
  overflow: hidden;
  /* Ensure radius is respected */
  background-color: transparent;
}

.release-modal .modal-content {
  border: none;
  background-color: #111;
  /* Make header + body background uniform */
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
}

.release-modal .modal-header {
  padding: 1rem 1.5rem;
  background-color: inherit;
  /* Match .modal-content */
  color: #fff;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin: 0;
}

.release-modal .modal-body {
  padding: 1.25rem 1.5rem;
  background-color: #fff;
  color: #000;
  border-top: none;
}

.release-modal .modal-footer {
  background-color: #f8f9fa;
  border-top: 1px solid #dee2e6;
  padding: 1rem 1.5rem;
}


/* Fade animation */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.96);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
