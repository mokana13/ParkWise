<template>
  <div class="d-flex vh-100">
    <!-- Sidebar -->
    <Sidebar :username="username" @change-view="changeView" @logout="logout" />

    <!-- Main Content Pane -->
    <div class="main-content flex-grow-1 bg-light overflow-auto">

      <!-- Profile / Edit in one pane -->
      <div v-if="currentView === 'profile'" class="d-flex justify-content-center align-items-center" style="height:100%">
        <div class="card profile-card p-4 shadow-sm">
          <h4 class="mb-4 text-center">Admin Profile</h4>
          <form @submit.prevent="saveProfile">
            <div class="mb-3">
              <label class="form-label">Email</label>
              <input v-model="profileForm.email" type="email" class="form-control" disabled />
            </div>
            <div class="mb-3 position-relative">
              <label class="form-label">Password</label>
              <input :type="showPassword ? 'text' : 'password'" v-model="profileForm.password" class="form-control"
                placeholder="Password" />
              <i :class="showPassword ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'" class="password-eye"
                @click="showPassword = !showPassword"></i>
            </div>
            <div class="d-flex justify-content-between">
              <button type="button" class="btn btn-outline-secondary" @click="changeView('dashboard')">
                <i class="bi bi-arrow-left me-1"></i>Back
              </button>
              <button type="submit" class="btn btn-primary">Save Changes</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Dashboard View -->
<div v-else-if="currentView === 'dashboard'" class="p-3" style="max-height: 100vh; overflow-y: auto;">

  <!-- STATS CARDS -->
  <div class="row g-3 mb-3 text-center">
    <div
      class="col-6 col-md-3 col-lg-1-7"
      v-for="(label, key) in {
        'Total Lots': 'totalLots',
        'Total Spots': 'totalSpots',
        Available: 'availableSpots',
        Reserved: 'reservedSpots',
        'Total Users': 'totalUsers',
        'Total Revenue': 'totalRevenue',
        'Monthly Revenue': 'monthlyRevenue'
      }"
      :key="key"
    >
      <div class="card shadow-sm border-0 h-100">
        <div class="card-body py-2 px-2">
          <h6 class="card-subtitle mb-1 text-muted small">{{ key }}</h6>
          <h6
            class="card-title mb-0 fw-bold small"
            :class="{
              'text-primary': key === 'Total Lots',
              'text-success': key === 'Total Spots',
              'text-info': key === 'Available',
              'text-danger': key === 'Reserved',
              'text-dark': key === 'Total Users',
              'text-warning': key === 'Total Revenue',
              'text-success': key === 'Monthly Revenue'
            }"
          >
            {{
              key === 'Total Users'
                ? totalUsers
                : key === 'Total Revenue'
                ? '₹ ' + totalRevenue.toFixed(2)
                : key === 'Monthly Revenue'
                ? '₹ ' + monthlyRevenue.toFixed(2)
                : stats[label]
            }}
          </h6>
        </div>
      </div>
    </div>
  </div>

  <!-- CHARTS ROW: Availability + Revenue Pie -->
  <div class="row g-3 mb-3">
    <div class="col-md-6">
      <div class="card shadow-sm border-0 h-100">
        <div class="card-body p-2">
          <h6 class="card-title mb-2 small">Availability Summary</h6>
          <div class="chart-container" style="height: 240px;">
            <canvas ref="availabilityChart" style="width:100%; height:100%;"></canvas>
          </div>
        </div>
      </div>
    </div>

    <div class="col-md-6">
      <div class="card shadow-sm border-0 h-100">
        <div class="card-body p-2">
          <h6 class="card-title mb-2 small">Revenue by Lot</h6>
          <div class="chart-container" style="height: 240px;">
            <canvas ref="revenuePieChart" style="width:100%; height:100%;"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- MONTHLY REVENUE FULL-WIDTH -->
  <div class="row g-3">
    <div class="col-12">
      <div class="card shadow-sm border-0 h-100">
        <div class="card-body p-2">
          <h6 class="card-title mb-2 small">Monthly Revenue</h6>
          <div class="chart-container" style="height: 240px;">
            <canvas ref="monthlyRevenueChart" style="width:100%; height:100%;"></canvas>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>


      <!-- Bookings View -->
      <div v-else-if="currentView === 'bookings'" class="p-4">
        <div class="card shadow-sm border-0 p-4">
          <h4 class="fw-bold text-primary text-center mb-4">Booking History</h4>

          <div class="table-responsive">
            <table class="table table-hover align-middle table-borderless">
              <thead class="table-dark">
                <tr>
                  <th>ID</th>
                  <th>User</th>
                  <th>Lot</th>
                  <th>Spot</th>
                  <th>Start</th>
                  <th>End</th>
                  <th>Cost</th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="(b, idx) in bookings" :key="b.id">
                  <td class="fw-semibold text-muted">{{ idx + 1 }}</td>

                  <td>
                    <div class="fw-semibold">{{ b.user.fullname }}</div>
                    <small class="text-muted">{{ b.user.email }}</small>
                  </td>

                  <td>{{ b.lot.name }}</td>
                  <td><span class="badge bg-secondary">{{ b.spot_number }}</span></td>

                  <td>
                    <span class="text-nowrap">{{ formatDateIST(b.start_time) }}</span>
                  </td>

                  <td>
                    <span v-if="b.end_time" class="text-nowrap">{{ formatDateIST(b.end_time) }}</span>
                    <span v-else class="text-warning fst-italic">In Progress</span>
                  </td>

                  <td>
                    <span v-if="b.cost" class="fw-bold text-success">₹ {{ b.cost }}</span>
                    <span v-else class="text-muted">—</span>
                  </td>
                </tr>

                <tr v-if="!bookings.length">
                  <td colspan="7" class="text-center text-muted py-4">
                    🚫 No bookings found
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>



      <!-- Home View -->
      <div v-if="currentView === 'home'" class="p-4">
        <!-- Add Lot Button -->
        <div class="d-flex justify-content-center mb-4">
          <button class="btn btn-sm btn-outline-primary d-flex align-items-center gap-1"
            @click="showNewLotModal = true">
            <i class="bi bi-plus-circle"></i>
            Add Lot
          </button>

        </div>

        <!-- Search Bar -->
        <div class="d-flex align-items-center mb-4">
          <!-- Dropdown for search-by field -->
          <select v-model="searchBy" class="form-select me-3" style="width: 130px; font-size: 1rem; height: 45px;">
            <option value="userId">User</option>
            <option value="location">Location</option>
            <option value="pincode">Pincode</option>
          </select>

          <!-- Text input for search query -->
          <input v-model="searchQuery" type="text" placeholder="Enter search term" class="form-control me-3"
            style="font-size: 1rem; height: 45px; max-width: 820px;" />

          <!-- Search button -->
          <button class="btn btn-primary me-2 px-4" style="height: 40px;" @click="performSearch()">
            Search
          </button>

          <!-- Clear search -->
          <button class="btn btn-outline-secondary px-4" style="height: 40px;" @click="clearSearch()">
            Clear
          </button>
        </div>


        <!-- Parking Lots List -->
        <div v-if="parkingLots.length">
          <div v-for="lot in parkingLots" :key="lot.id"
            class="card mb-3 shadow-sm border-0 p-3 d-flex flex-md-row flex-column justify-content-between align-items-md-center align-items-start">
            <div>
              <h5 class="mb-1">{{ lot.name }}</h5>
              <small class="text-muted">
                Occupied: {{lot.spots.filter(s => !s.is_available).length}} /
                {{ lot.spots.length }}
              </small>
            </div>

            <div class="btn-group btn-group-sm mt-2 mt-md-0">
              <button class="btn btn-outline-secondary" @click="openEditLot(lot)">
                <i class="bi bi-pencil-square me-1"></i>Edit
              </button>
              <button class="btn btn-outline-primary" @click="viewLot(lot)">
                View
              </button>
              <button class="btn btn-outline-danger" :disabled="lot.spots.some(s => !s.is_available)"
                @click="deleteLot(lot.id)">
                <i class="bi bi-trash"></i>
              </button>

            </div>
          </div>
        </div>
        <div v-else class="text-muted text-center py-5">🚫 No parking lots yet.</div>
        <!-- 2) New Parking Modal -->
        <div v-if="showNewLotModal" class="modal-backdrop" @click.self="showNewLotModal = false">
          <div class="modal-content p-3 shadow" style="max-width: 600px; margin: auto;">
            <h5 class="mb-3">Add New Parking Lot</h5>

            <div class="row g-2">
              <div class="col-12">
                <label class="form-label">Location Name</label>
                <input v-model="newLot.name" class="form-control" placeholder="e.g., Marina Lot" />
              </div>

              <div class="col-md-8">
                <label class="form-label">Address</label>
                <input v-model="newLot.address" class="form-control" />
              </div>

              <div class="col-md-4">
                <label class="form-label">Pincode</label>
                <input v-model="newLot.pincode" class="form-control" />
              </div>

              <div class="col-md-6">
                <label class="form-label">Price (per hour)</label>
                <input v-model="newLot.price" type="number" class="form-control" />
              </div>

              <div class="col-md-6">
                <label class="form-label">Max Spots</label>
                <input v-model="newLot.maxSpots" type="number" class="form-control" />
              </div>
            </div>

            <div class="text-end mt-3">
              <button class="btn btn-sm btn-outline-secondary me-2" @click="showNewLotModal = false">Cancel</button>
              <button class="btn btn-sm btn-primary" @click="addNewLot">Add</button>
            </div>
          </div>
        </div>

        <!-- Lot Details Modal -->
        <div v-if="showLotDetails" class="modal-backdrop" @click.self="showLotDetails = false">
          <div class="modal-content p-4 shadow">
            <h5 class="mb-3">{{ selectedLot.name }}</h5>
            <p class="mb-1"><strong>Address:</strong> {{ selectedLot.location }}</p>
            <p class="mb-1"><strong>Pincode:</strong> {{ selectedLot.pincode }}</p>
            <p class="mb-1"><strong>Price/hr:</strong> ₹ {{ selectedLot.price_per_hour }}</p>
            <p class="mb-3"><strong>Spots:</strong> {{ selectedLot.spots.length }}</p>

            <div class="d-flex flex-wrap gap-2">
              <div v-for="spot in selectedLot.spots" :key="spot.id" class="badge text-bg-light p-3 rounded-2"
                :class="spot.is_available ? 'bg-success' : 'bg-danger'" style="cursor: pointer;"
                @click="onSpotClick(spot)">
                {{ spot.number }}
              </div>
            </div>

            <div class="text-end mt-4">
              <button class="btn btn-secondary" @click="showLotDetails = false">Close</button>
            </div>
          </div>
        </div>

        <!-- Edit Lot Modal -->
        <div v-if="showEditLotModal" class="modal-backdrop" @click.self="showEditLotModal = false">
          <div class="modal-content p-4 shadow">
            <h5>Edit Parking Lot</h5>
            <div class="mb-2">
              <label class="form-label">Name</label>
              <input v-model="editLotForm.name" class="form-control" />
            </div>
            <div class="mb-2">
              <label class="form-label">Location</label>
              <input v-model="editLotForm.location" class="form-control" />
            </div>
            <div class="mb-2">
              <label class="form-label">Pincode</label>
              <input v-model="editLotForm.pincode" class="form-control" />
            </div>
            <div class="mb-2">
              <label class="form-label">Price/hr</label>
              <input v-model="editLotForm.price_per_hour" type="number" class="form-control" />
            </div>
            <div class="text-end">
              <button class="btn btn-secondary me-2" @click="showEditLotModal = false">Cancel</button>
              <button class="btn btn-primary" @click="saveEditedLot">Save</button>
            </div>
          </div>
        </div>
      </div>


      <!-- Users View -->
      <div v-else-if="currentView === 'users'" class="p-4 bg-users-view">
        <div class="card shadow border-0 p-4 glass-table-card">
          <h4 class="mb-4 fw-bold text-primary text-center">Registered Users</h4>

          <div class="table-responsive">
            <table class="table table-hover align-middle text-white table-borderless custom-table">
              <thead class="table-dark">
                <tr>
                  <th scope="col">ID</th>
                  <th scope="col">Email</th>
                  <th scope="col">Full Name</th>
                  <th scope="col">Address</th>
                  <th scope="col">Pincode</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(u, idx) in users" :key="u.id" class="table-row">
                  <td>{{ idx + 1 }}</td>
                  <td>{{ u.email }}</td>
                  <td>{{ u.fullname }}</td>
                  <td>{{ u.address }}</td>
                  <td>{{ u.pincode }}</td>
                </tr>
                <tr v-if="!users.length">
                  <td colspan="5" class="text-center text-muted py-4">🚫 No users found.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>


      <!-- Spot Details Modal -->
      <div v-if="showSpotModal" class="modal-backdrop" @click.self="showSpotModal = false">
        <div class="modal-content p-4 shadow">
          <h5>
            Spot #{{ selectedSpot.number }} –
            <span v-if="selectedSpot.is_available">Available</span>
            <span v-else>Occupied</span>
          </h5>

          <!-- Available Spot -->
          <template v-if="selectedSpot.is_available">
            <p>Status: Available</p>
            <div class="text-end">
              <button class="btn btn-danger me-2" @click="deleteSpot(selectedLot.id, selectedSpot.id)">
                Delete Spot
              </button>

              <button class="btn btn-secondary" @click="showSpotModal = false">
                Close
              </button>
            </div>
          </template>

          <!-- Occupied Spot -->
          <template v-else>
            <ul class="list-unstyled mb-3">
              <li><strong>Full Name:</strong> {{ spotDetails.fullname }}</li>
              <li><strong>Email:</strong> {{ spotDetails.email }}</li>
              <li><strong>Vehicle No:</strong> {{ spotDetails.vehicle_no }}</li>
              <li>
                <strong>Start Time:</strong>
                {{
                  new Date(spotDetails.start_time)
                    .toLocaleString('en-IN', {
                      timeZone: 'Asia/Kolkata',
                      day: 'numeric',
                      month: 'short',
                      year: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit',
                      hour12: true
                    })
                }} IST
              </li>

              <li><strong>Estimated Cost:</strong> ₹{{ spotDetails.est_cost.toFixed(2) }}</li>
            </ul>

            <div class="text-end">
              <button class="btn btn-secondary" @click="showSpotModal = false">
                Close
              </button>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Sidebar from '../components/Sidebar.vue'
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);
import { DateTime } from 'luxon'


import axios from 'axios'


export default {
  components: { Sidebar },
  data() {
    return {
      username: '',
      parkingLots: [],
      allParkingLots: [],
      users: [],
      currentView: 'dashboard',
      form: { name: '', location: '', spot: '' },
      newSpots: {},
      stats: {
        totalLots: 0,
        totalSpots: 0,
        availableSpots: 0,
        reservedSpots: 0,
        lotSummary: []
      },
      bookings: [],
      totalUsers: 0,
      totalRevenue: 0,
      monthlyRevenue: 0,
      monthlyRevenueData: {
        labels: [],
        data: []
      },
      showPassword: false,
      profileForm: {
        email: 'admin@example.com',
        password: localStorage.getItem('password') || ''
      },

      // ← NEW STATE for Home view
      showNewLotModal: false,
      newLot: {
        name: '',
        address: '',
        pincode: '',
        price: null,
        maxSpots: null
      },
      showLotDetails: false,
      selectedLot: null,
      searchBy: 'location',

      searchQuery: '',
      showSpotModal: false,

      selectedSpot: null,

      spotDetails: null,

      showEditLotModal: false,

      editLotForm: {
        id: null,
        name: '',
        location: '',
        pincode: '',
        price_per_hour: null,
        maxSpots: null
      }
    }
  },

  watch: {
    currentView(newView) {
      if (newView === 'dashboard') {
        // Wait until the Dashboard block has been rendered
        this.$nextTick(() => {
          // Verify your refs are found
          console.log('avail ref →', this.$refs.availabilityChart)
          console.log('pie   ref →', this.$refs.revenuePieChart)
          this.renderCharts()
        })
      }
    }
  },

  methods: {
    changeView(view) {
      this.currentView = view
      if (view === 'users') this.fetchUsers()
      if (view === 'dashboard') this.fetchLots()
      this.currentView = view;
      if (view === 'bookings') {
        this.fetchBookings();
      }
    },
    async saveProfile() {
      try {
        await axios.put(
          'http://127.0.0.1:5000/admin/profile',
          { password: this.profileForm.password },
          { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
        )
        // sync the new password locally so Profile View shows it
        localStorage.setItem('password', this.profileForm.password)
        alert('Password updated!')
      } catch (err) {
        alert('Update failed: ' + (err.response?.data?.msg || err.message))
      }
    },

    performSearch() {
      const q = this.searchQuery.trim().toLowerCase();
      if (!q) {
        this.parkingLots = this.allParkingLots;
        return;
      }

      this.parkingLots = this.allParkingLots.filter(lot => {
        if (this.searchBy === 'location') {
          return lot.location.toLowerCase().includes(q);
        }
        if (this.searchBy === 'pincode') {
          return lot.pincode.toLowerCase().includes(q);
        }
        if (this.searchBy === 'userId') {
          return lot.spots.some(spot => {
            if (!spot.is_available && spot.reservation_details) {
              const fullname = (spot.reservation_details.fullname || '').toLowerCase();
              const email = (spot.reservation_details.email || '').toLowerCase();
              // Require exact match for either full name or email
              return fullname === q || email === q;
            }
            return false;
          });
        }
        return false;
      });
    },

    calculateRevenues() {
      // Get all completed bookings with costs
      const completedBookings = this.bookings.filter(b => b.cost && b.end_time)

      // Calculate total revenue (sum of all completed bookings)
      this.totalRevenue = completedBookings.reduce((sum, b) => sum + parseFloat(b.cost), 0)

      // Calculate current month's revenue
      const currentMonth = new Date().getMonth()
      const currentYear = new Date().getFullYear()

      this.monthlyRevenue = completedBookings
        .filter(b => {
          const endDate = new Date(b.end_time)
          return endDate.getMonth() === currentMonth &&
            endDate.getFullYear() === currentYear
        })
        .reduce((sum, b) => sum + parseFloat(b.cost), 0)

      // Prepare data for monthly chart
      this.prepareMonthlyRevenueData()

      console.log('Revenue calculated:', {
        total: this.totalRevenue,
        monthly: this.monthlyRevenue,
        bookingsCount: completedBookings.length
      })
    },

prepareMonthlyRevenueData() {
  const months = [];
  const revenue = [];
  const now = new Date();
  const currentYear = now.getFullYear();

  for (let i = 5; i >= 0; i--) {
    const date = new Date(now);
    date.setMonth(date.getMonth() - i);

    const monthName = date.toLocaleString('default', { month: 'short' });
    const year = date.getFullYear();
    const label = year === currentYear ? monthName : `${monthName} ${year}`;
    months.push(label);

    const monthRevenue = this.bookings
      .filter(
        b =>
          b.cost &&
          b.end_time &&
          new Date(b.end_time).getMonth() === date.getMonth() &&
          new Date(b.end_time).getFullYear() === date.getFullYear()
      )
      .reduce((sum, b) => sum + parseFloat(b.cost), 0);

    revenue.push(monthRevenue);
  }

  const labels = [...new Set(months)];
  const data = labels.map(m => revenue[months.indexOf(m)]);

  this.monthlyRevenueData = { labels, data };
},

    // 2.1) Format any ISO UTC string into IST display
    formatDateIST(dateStr) {
      if (!dateStr) return '— in progress —'
      const dtUtc = DateTime.fromISO(dateStr, { zone: 'utc' })
      const dtIst = dtUtc.setZone('Asia/Kolkata')
      return dtIst.toFormat("dd LLL yyyy, hh:mm a 'IST'")
    },

    // 2.2) Compute Est Cost from start time + rate, min 1 hour
    calculateEstCost(startStr, rate) {
      const startUtc = DateTime.fromISO(startStr, { zone: 'utc' })
      const nowIst = DateTime.now().setZone('Asia/Kolkata')
      let hours = nowIst.diff(startUtc, 'hours').hours
      hours = Math.max(hours, 1)    // enforce 1-hour minimum
      return (hours * rate).toFixed(2)
    },


    async fetchBookings() {
      try {
        const token = localStorage.getItem('token')
        const res = await fetch('http://127.0.0.1:5000/admin/bookings', {
          headers: { Authorization: `Bearer ${token}` }
        })
        const payload = await res.json()
        this.bookings = payload.bookings

        // Add validation
        if (!this.bookings.every(b => typeof b.cost === 'number')) {
          console.warn('Some bookings have invalid cost values:', this.bookings)
        }

        this.calculateRevenues()
      } catch (err) {
        alert('Failed to load bookings: ' + err.message)
      }
    },

    async deleteSpot(lotId, spotId) {
      try {
        // 1. Optimistically remove from UI
        const lot = this.parkingLots.find(l => l.id === lotId);
        if (lot) {
          lot.spots = lot.spots.filter(s => s.id !== spotId);
        }

        // 2. Close modal IMMEDIATELY (before API call)
        this.showSpotModal = false;  // This is the key line you're missing

        // 3. Make API call in background
        const token = localStorage.getItem('token');
        await axios.delete(
          `http://localhost:5000/admin/lots/${lotId}/spots/${spotId}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );

      } catch (err) {
        // If error occurs, refresh data
        this.fetchLots();
        console.error('Delete failed:', err);
      }
    },
    clearSearch() {
      this.searchQuery = '';
      this.parkingLots = this.allParkingLots;
    },

    async addNewLot() {
      try {
        const token = localStorage.getItem('token')
        // POST to your new-lot endpoint
        const res = await axios.post(
          'http://127.0.0.1:5000/admin/lots',
          {
            name: this.newLot.name,
            address: this.newLot.address,
            pincode: this.newLot.pincode,
            price: this.newLot.price,
            maxSpots: this.newLot.maxSpots
          },
          { headers: { Authorization: `Bearer ${token}` } }
        )

        // on success: close modal, reset form, re-fetch server data
        this.showNewLotModal = false
        this.newLot = { name: '', address: '', pincode: '', price: null, maxSpots: null }
        await this.fetchLots()

        alert('Lot created successfully!')
      } catch (err) {
        alert('Failed to create lot: ' + (err.response?.data?.msg || err.message))
      }
    },




    // ← NEW: Show a lot’s detail modal
    viewLot(lot) {
      this.selectedLot = lot
      this.showLotDetails = true
    },

    async fetchUsers() {
      // 1) Clear out any old rows
      this.users = []

      try {
        const token = localStorage.getItem('token')
        const res = await fetch('http://127.0.0.1:5000/admin/users', {
          headers: { Authorization: `Bearer ${token}` }
        })
        const payload = await res.json()
        if (!res.ok) throw new Error(payload.msg || 'Failed to fetch users')

        // 2) Deduplicate by id
        const uniqueById = [
          ...new Map(payload.users.map(u => [u.id, u])).values()
        ]

        // 3) Assign the clean list
        this.users = uniqueById

      } catch (err) {
        alert('Could not load users: ' + err.message)
      }
    },




    async fetchLots() {
      try {
        const token = localStorage.getItem('token')
        const res = await fetch('http://127.0.0.1:5000/admin/dashboard', {
          headers: { Authorization: `Bearer ${token}` }
        })
        const data = await res.json()
        console.log('🚀 DASHBOARD PAYLOAD:', data)
        if (!res.ok) throw new Error(data.msg || 'Unauthorized')

        // Map in the new fields (REMOVE totalRevenue from here)
        this.parkingLots = data.parking_lots.map(lot => ({
          id: lot.id,
          name: lot.name,
          location: lot.location,
          pincode: lot.pincode,
          price_per_hour: lot.price_per_hour,
          spots: lot.spots.map(spot => ({
            ...spot,
            reservation_details: spot.reservation_details || null
          }))
        }))

        this.allParkingLots = this.parkingLots
        this.username = data.username || ''

        this.stats = {
          totalLots: data.total_lots,
          totalSpots: data.total_spots,
          availableSpots: data.available_spots,
          reservedSpots: data.reserved_spots,
          lotSummary: data.lot_summary
        }

        this.totalUsers = data.total_users
        // REMOVE this line: this.totalRevenue = data.total_revenue

        this.$nextTick(() => this.renderCharts())
      }
      catch (err) {
        alert(err.message)
        this.$router.push('/login')
      }
    },
    // Called by pencil icon
    openEditLot(lot) {
      this.editLotForm = {
        id: lot.id,
        name: lot.name,
        location: lot.location,
        pincode: lot.pincode,
        price_per_hour: lot.price_per_hour,
        maxSpots: lot.spots.length
      }
      this.showEditLotModal = true
    },

    // PUT back to server and refresh
    async saveEditedLot() {
      try {
        const token = localStorage.getItem('token')
        await axios.put(
          `http://127.0.0.1:5000/admin/lots/${this.editLotForm.id}`,
          this.editLotForm,
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.showEditLotModal = false
        await this.fetchLots()
      } catch (err) {
        alert('Couldn’t save changes: ' + err.message)
      }
    },

    async createLot() {
      try {
        const token = localStorage.getItem('token')
        const lotRes = await fetch('http://localhost:5000/admin/lots', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`
          },
          body: JSON.stringify({
            name: this.form.name,
            location: this.form.location
          })
        })
        const lotData = await lotRes.json()
        if (!lotRes.ok) return alert(lotData.msg)

        const spotCount = parseInt(this.form.spot)
        if (!spotCount || spotCount < 1)
          return alert('Enter valid number of spots')

        const spotRes = await fetch(
          `http://localhost:5000/admin/lots/${lotData.lot_id}/spots`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ number: spotCount })
          }
        )
        const spotData = await spotRes.json()
        if (!spotRes.ok) return alert(spotData.msg)

        alert('Lot created!')
        this.form = { name: '', location: '', spot: '' }
        this.currentView = 'lots'
        this.fetchLots()
      } catch {
        alert('Error creating lot')
      }
    },



    async addSpot(lotId) {
      const token = localStorage.getItem('token')
      const number = parseInt(this.newSpots[lotId])
      if (!number || number < 1) return alert('Enter valid spots')
      try {
        const res = await fetch(
          `http://localhost:5000/admin/lots/${lotId}/spots`,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ number })
          }
        )
        const data = await res.json()
        if (!res.ok) return alert(data.msg)
        this.newSpots[lotId] = ''
        this.fetchLots()
      } catch {
        alert('Error adding spots')
      }
    },

    async deleteLot(lotId) {
      // 1) Confirm in the UI
      if (!confirm('Delete this empty lot for good?')) return;

      // 2) Grab token
      const token = localStorage.getItem('token');
      if (!token) {
        return alert('Not authenticated');
      }

      try {
        // 3) Call DELETE endpoint
        const res = await fetch(
          `http://127.0.0.1:5000/admin/lots/${lotId}`,
          {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
            }
          }
        );

        // 4) Read back the payload
        const data = await res.json();
        console.log('DELETE /admin/lots response →', res.status, data);

        // 5) Handle errors
        if (!res.ok) {
          return alert(data.msg || `Delete failed (${res.status})`);
        }

        // 6) Success—refresh your list
        alert('Lot deleted successfully');
        this.fetchLots();
      }
      catch (err) {
        console.error('Network or parsing error:', err);
        alert('Unexpected error, check console for details');
      }
    },


    promptEditSpot(lotId, spotId, currentNumber) {
      const input = prompt('Enter new spot number:', currentNumber)
      if (input === null) return
      const newNum = parseInt(input)
      if (!newNum || newNum < 1) {
        return alert('Please enter a valid number')
      }
      this.editSpot(lotId, spotId, newNum)
    },

    async editSpot(lotId, spotId, newNumber) {
      try {
        const token = localStorage.getItem('token')
        const res = await fetch(
          `http://localhost:5000/admin/lots/${lotId}/spots/${spotId}`,
          {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`
            },
            body: JSON.stringify({ number: newNumber })
          }
        )
        const data = await res.json()
        if (!res.ok) throw new Error(data.msg || 'Failed to update spot')
        this.fetchLots()
      } catch (err) {
        alert(err.message)
      }
    },

    confirmDeleteSpot(lotId, spotId) {
      if (!confirm('Delete this spot?')) return
      this.deleteSpot(lotId, spotId)
    },


    confirmDelete(id, name) {
      if (confirm(`Delete "${name}" and all its spots?`)) {
        this.deleteLot(id)
      }
    },

    async onSpotClick(spot) {
      // 1) Remember which spot was clicked
      this.selectedSpot = spot;

      // 2) Available spot → just show modal with no details
      if (spot.is_available) {
        this.spotDetails = null;
        this.showSpotModal = true;
        return;
      }

      // 3) Occupied spot → fetch reservation info first
      try {
        const token = localStorage.getItem('token');
        const res = await axios.get(
          `http://127.0.0.1:5000/admin/lots/${this.selectedLot.id}/spot/${spot.id}`,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        this.spotDetails = res.data;
        this.showSpotModal = true;
      } catch (err) {
        alert('Failed to load spot details: ' + err.message);
      }
    },

    renderCharts() {
      // 1) Availability Bar Chart
      const availCanvas = this.$refs.availabilityChart;


      if (!availCanvas) {
        console.error('availabilityChart ref not found');
        return;
      }
      const availCtx = availCanvas.getContext('2d');
      if (this._availabilityChart) this._availabilityChart.destroy();
      this._availabilityChart = new Chart(availCtx, {
        type: 'bar',
        data: {
          labels: ['Available', 'Occupied'],
          datasets: [{
            label: 'Spots',
            data: [this.stats.availableSpots, this.stats.reservedSpots],
            backgroundColor: ['#28a745', '#dc3545']
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: { beginAtZero: true }
          }
        }
      });

      // Monthly Revenue Bar Chart
      const monthlyRevCanvas = this.$refs.monthlyRevenueChart;
      if (monthlyRevCanvas) {
        const ctx = monthlyRevCanvas.getContext('2d');
        if (this._monthlyRevenueChart) this._monthlyRevenueChart.destroy();

        this._monthlyRevenueChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: this.monthlyRevenueData.labels,
            datasets: [{
              label: 'Monthly Revenue (₹)',
              data: this.monthlyRevenueData.data,
              backgroundColor: '#4e73df'
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  callback: function (value) {
                    return '₹' + value;
                  }
                }
              }
            },
            plugins: {
              tooltip: {
                callbacks: {
                  label: function (context) {
                    return '₹' + context.raw.toFixed(2);
                  }
                }
              }
            }
          }
        });
      }


      // 2) Revenue Pie Chart
      const pieCanvas = this.$refs.revenuePieChart;
      if (!pieCanvas) {
        console.error('revenuePieChart ref not found');
        return;
      }
      const pieCtx = pieCanvas.getContext('2d');
      if (this._revenuePieChart) this._revenuePieChart.destroy();

      // optional color palette
      const palette = [
        '#FF6384', '#36A2EB', '#FFCE56',
        '#4BC0C0', '#9966FF', '#FF9F40'
      ];
      const bgColors = this.stats.lotSummary.map(
        (_, i) => palette[i % palette.length]
      );



      this._revenuePieChart = new Chart(pieCtx, {
        type: 'pie',
        data: {
          labels: this.stats.lotSummary.map(l => l.name),
          datasets: [{
            data: this.stats.lotSummary.map(l => l.revenue),
            backgroundColor: bgColors
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
    },

    logout() {
      localStorage.removeItem('token')
      this.$router.push('/login')
    }
  },

  mounted() {
    this.fetchLots();
    this.fetchBookings(); // This will trigger calculateRevenues()
  }
}
</script>


<style scoped>
.main-content {
  margin-left: 260px;
  height: 100vh;
  /* keep full height */
  overflow-y: auto;
  /* scroll if content overflows */
}

.profile-card {
  max-width: 380px;
}

/* Add this to your global styles or scoped section */
.col-lg-1-7 {
  flex: 0 0 14.2857%;
  max-width: 14.2857%;
}

/* Eye icon inside password field */
.password-eye {
  position: absolute;
  top: 70%;
  right: 0.75rem;
  transform: translateY(-50%);
  cursor: pointer;
  color: #6c757d;
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #fff;
  border-radius: 4px;
  width: 360px;
}

.spot-box {
  width: 36px;
  height: 36px;
  color: #fff;
  font-weight: bold;
  border-radius: 4px;
}

/* Layout Tweaks */
.main-content {
  padding: 1.5rem;
  background-color: #f8f9fa;
}

/* Profile Card */
.profile-card {
  width: 100%;
  max-width: 400px;
  border-radius: 12px;
  background-color: #ffffff;
}

/* Password toggle eye icon */
.password-eye {
  position: absolute;
  top: 75%;
  right: 12px;
  transform: translateY(-50%);
  cursor: pointer;
  color: #6c757d;
}

/* Stat Box */
.stat-box {
  transition: box-shadow 0.3s ease;
  border-radius: 12px;
}

.stat-box:hover {
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.1);
}

.stat-title {
  font-size: 0.9rem;
  color: #6c757d;
}

.stat-value {
  font-size: 1.6rem;
  font-weight: bold;
}

/* Charts */
.chart-container {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 1rem;
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
  padding: 1rem;
}

.modal-content {
  width: 100%;
  max-width: 500px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 0.75rem 2rem rgba(0, 0, 0, 0.15);
  animation: fadeIn 0.25s ease-in-out;
}

/* Lot Cards */
.lot-card {
  border-radius: 8px;
  transition: transform 0.2s ease;
}

.lot-card:hover {
  transform: scale(1.01);
}

/* Spot Boxes */
.spot-box {
  width: 48px;
  height: 48px;
  font-weight: 600;
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.spot-box:hover {
  transform: scale(1.1);
}

/* Table */
.table th,
.table td {
  vertical-align: middle;
}

/* Button enhancements */
.btn {
  border-radius: 6px;
}

/* Responsive padding fix for smaller screens */
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.97);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
