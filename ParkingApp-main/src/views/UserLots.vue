<template>
  <div v-if="loading" class="d-flex flex-column align-items-center justify-content-center min-vh-100 bg-white">
    <div class="spinner-border text-primary" role="status"></div>
    <p class="mt-3 text-muted">Loading parking lots…</p>
  </div>

  <div v-else-if="error" class="alert alert-danger text-center m-4">
    {{ error }}
  </div>

  <div v-else class="bg-light min-vh-100 d-flex flex-column">
    <UserNavbar :username="user.username || user.email" />

    <!-- Booking Modal -->
    <div class="modal fade show d-block" v-if="showModal" tabindex="-1" @click.self="closeModal">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content shadow rounded-4">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">Confirm Parking Spot</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-2 d-flex justify-content-between">
              <span class="text-muted">Parking Lot:</span>
              <strong>{{ bookingData.lotName }}</strong>
            </div>
            <div class="mb-2 d-flex justify-content-between">
              <span class="text-muted">Spot Number:</span>
              <strong>#{{ bookingData.spotNumber }}</strong>
            </div>
            <div class="mb-2 d-flex justify-content-between">
              <span class="text-muted">User ID:</span>
              <strong>{{ bookingData.userId }}</strong>
            </div>
            <div class="mb-2 d-flex justify-content-between">
              <span class="text-muted">Rate per Hour:</span>
              <strong class="text-success">₹{{ bookingData.cost }}</strong>
            </div>
            <small class="text-secondary d-block mb-3">
              Minimum billing unit: 1 hour (you’ll be charged for a full hour even if you leave sooner)
            </small>
            <div class="mb-2 d-flex justify-content-between">
              <span class="text-muted">Start Time:</span>
              <strong>{{ formatDateIST(bookingData.startTime) }}</strong>
            </div>
            <hr />
            <label class="form-label fw-semibold">Enter Vehicle Number</label>
            <input
              v-model="vehicleNumber"
              type="text"
              class="form-control form-control-lg shadow-sm"
              placeholder="e.g. TN01AB1234"
            />
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline-dark" @click="closeModal">Cancel</button>
            <button class="btn btn-success" :disabled="!vehicleNumber" @click="confirmBooking">
              Confirm Booking
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="container-lg flex-grow-1 py-4">
      <!-- Search -->
      <div class="row g-3 align-items-center mb-4">
        <div class="col-auto">
          <select v-model="searchField" class="form-select">
            <option value="name">Lot Name</option>
            <option value="location">Address</option>
            <option value="pincode">Pincode</option>
          </select>
        </div>
        <div class="col">
          <input v-model="searchQuery" type="text" class="form-control shadow-sm" placeholder="Search..." />
        </div>
      </div>

      <!-- Title -->
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4 class="fw-bold">Available Parking Lots</h4>
      </div>

      <!-- Cards -->
      <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
        <div v-for="lot in filteredLots" :key="lot.id" class="col">
          <div class="card h-100 border-0 shadow-sm rounded-4">
            <div class="card-body d-flex flex-column">
              <div class="mb-3">
                <h5 class="card-title mb-1 fw-semibold">{{ lot.name }}</h5>
                <div class="text-muted small">{{ lot.location }}</div>
                <div class="text-muted small mb-2">Pincode: {{ lot.pincode || 'N/A' }}</div>
                <ul class="list-unstyled small">
                  <li><strong>Total Spots:</strong> {{ lot.total_spots }}</li>
                  <li><strong>Available:</strong> {{ lot.available_spots }}</li>
                  <li>
                    <strong>Rate:</strong> ₹{{ lot.price_per_hour }}
                    <small class="text-muted">/hr</small>
                  </li>
                </ul>
              </div>
              <button
                class="btn btn-outline-primary mt-auto"
                :disabled="lot.available_spots === 0"
                @click="openBookingModal(lot)"
              >
                Book Spot
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>


<script>
import axios from 'axios'
import UserNavbar from '../components/UserNavbar.vue'
import { DateTime } from 'luxon'

export default {
  name: 'UserLots',
  components: { UserNavbar },
  data() {
    return {
      user: null,
      lots: [],
      loading: true,
      error: '',
      showModal: false,
      vehicleNumber: '',
      searchField: 'location',
      searchQuery: '',
      bookingData: {
        lotId: null,
        lotName: '',
        spotNumber: null,
        reservationId: null,
        cost: 0,
        userId: null,
        startTime: null
      }
    }
  },
  computed: {
    filteredLots() {
      const q = this.searchQuery.trim().toLowerCase()
      if (!q) return this.lots
      return this.lots.filter(lot => {
        const val = (lot[this.searchField] || '').toString().toLowerCase()
        return val.includes(q)
      })
    }
  },
  methods: {
    async fetchData() {
      this.loading = true
      this.error = ''
      const token = localStorage.getItem('token')
      try {
        const [userRes, lotsRes] = await Promise.all([
          axios.get('http://localhost:5000/user/dashboard', {
            headers: { Authorization: `Bearer ${token}` }
          }),
          axios.get('http://localhost:5000/user/lots', {
            headers: { Authorization: `Bearer ${token}` }
          })
        ])
        this.user = userRes.data
        this.lots = lotsRes.data
      } catch (err) {
        if (err.response?.status === 401) {
          this.error = 'Session expired. Please log in again.'
          localStorage.clear()
          this.$router.push('/login')
        } else {
          this.error = 'Failed to load data.'
        }
      } finally {
        this.loading = false
      }
    },

    async openBookingModal(lot) {
      const token = localStorage.getItem('token')
      try {
        const res = await axios.post(
          'http://localhost:5000/user/assign',
          { lot_id: lot.id },
          { headers: { Authorization: `Bearer ${token}` } }
        )

        // Use current IST time for Start Time
        const nowIST = DateTime.now().setZone('Asia/Kolkata').toISO()

        // Convert DB user_id → your UI index (subtract admin id=1)
        const rawId = res.data.user_id
        const displayId = rawId - 1

        this.bookingData = {
          lotId: lot.id,
          lotName: lot.name,
          spotNumber: res.data.spot_number,
          reservationId: res.data.reservation_id,
          cost: res.data.cost,
          startTime: nowIST,
          userId: displayId
        }

        this.vehicleNumber = ''
        this.showModal = true
      } catch {
        alert('Could not hold a spot.')
      }
    },

    async confirmBooking() {
      const token = localStorage.getItem('token')
      try {
        await axios.post(
          'http://localhost:5000/user/reserve',
          {
            reservation_id: this.bookingData.reservationId,
            vehicle_number: this.vehicleNumber
          },
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.showModal = false
        this.$router.push('/user/reservations')
      } catch {
        alert('Booking failed.')
      }
    },

    closeModal() {
      this.showModal = false
    },

    formatDateIST(dateStr) {
      if (!dateStr) return 'N/A'
      const ist = DateTime.fromISO(dateStr).setZone('Asia/Kolkata')
      return ist.isValid
        ? ist.toFormat("dd LLL yyyy, hh:mm a 'IST'")
        : 'Invalid Date'
    }
  },
  mounted() {
    this.fetchData()
  }
}
</script>


<style scoped>
.loader-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem 0;
}

.loader-text {
  margin-top: 1rem;
  font-size: 1rem;
  color: #555;
}

.dashboard-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1 1 0;
  min-height: 0;
  overflow-y: auto;
  background-color: #f9f9f9;
}

/* Make the search row stretch */
.search-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  width: 100%;
}

/* Ensure the input fills the remaining space */
.search-row .form-control {
  flex: 1 1 auto;
  width: 100%;
  border: 1px solid #000;
  border-radius: 0.5rem;
  padding: 0.5rem 0.75rem;
}

/* Give the dropdown a solid black border on all sides */
.styled-dropdown {
  flex: 0 0 auto;
  border: 1px solid #000 !important;
  border-radius: 0.5rem;
  padding: 0.5rem 1.5rem 0.5rem 0.75rem;
  background-color: #fff;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 140 140' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath fill='%23000' d='M0 20l70 100 70-100z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 0.65rem;
  box-sizing: border-box;
}

/* Keep the black border on focus/open */
.styled-dropdown:focus {
  outline: none;
  border-color: #000 !important;
  box-shadow: 0 0 0 1px #000;
}

.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.card:hover {
  transform: translateY(-4px) scale(1.015);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-weight: 600;
}

.booking-modal {
  position: fixed;
  inset: 0;
  z-index: 2000;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.booking-modal .modal-dialog {
  max-width: 500px;
  width: 100%;
}

.booking-modal .modal-content {
  border: none;
  background-color: #fff;
  animation: fadeIn 0.25s ease-out;
}

.booking-modal .modal-header {
  border-bottom: none;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
}

.booking-modal .modal-footer {
  border-top: none;
  border-bottom-left-radius: 1rem;
  border-bottom-right-radius: 1rem;
}

.booking-modal input.form-control {
  border-radius: 0.5rem;
  font-size: 1rem;
}

.booking-modal .btn {
  border-radius: 0.5rem;
}

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
