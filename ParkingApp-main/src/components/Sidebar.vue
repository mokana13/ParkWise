<template>
  <div class="sidebar d-flex flex-column text-white p-4 shadow">
    <!-- Profile Section -->
    <div class="mb-4">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h5 class="mb-0 fw-bold">Admin</h5>
          <small class="text-white-50">Welcome, {{ username }}!</small>
        </div>
        <div class="dropdown">
          <button class="btn btn-glass dropdown-toggle" type="button" id="profileDropdown"
            data-bs-toggle="dropdown" aria-expanded="false">
            <i class="bi bi-chevron-down"></i>
          </button>
          <ul class="dropdown-menu dropdown-menu-dark shadow-sm" aria-labelledby="profileDropdown">
            <li>
              <button class="dropdown-item" type="button" @click="$emit('change-view', 'profile')">
                <i class="bi bi-person me-2"></i>View Profile
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <div class="mt-4 flex-grow-1">
      <button class="nav-btn" @click="$emit('change-view', 'home')">
        <i class="bi bi-house-door me-2"></i>Home
      </button>
      <button class="nav-btn" @click="$emit('change-view', 'users')">
        <i class="bi bi-people me-2"></i>Users
      </button>
      <button class="nav-btn" @click="$emit('change-view', 'dashboard')">
        <i class="bi bi-speedometer2 me-2"></i>Dashboard
      </button>
      <button class="nav-btn" @click="$emit('change-view', 'bookings')">
        <i class="bi bi-journal-check me-2"></i>Bookings
      </button>
    </div>

    <!-- Logout -->
    <div>
      <button class="btn btn-outline-danger w-100 fw-semibold" @click="$emit('logout')">
        <i class="bi bi-box-arrow-right me-2"></i>Logout
      </button>
    </div>
  </div>
</template>

<script>
export default {
  props: ['username']
}
</script>

<style scoped>
.sidebar {
  width: 275px;
  height: 100vh;
  background: linear-gradient(145deg, #1c1f2b, #2e3242);
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.2);
}

/* Custom Glass Button */
.btn-glass {
  background: rgba(255, 255, 255, 0.08);
  border: none;
  color: #fff;
  padding: 0.4rem 0.6rem;
  border-radius: 6px;
  transition: background 0.2s ease;
}

.btn-glass:hover {
  background: rgba(255, 255, 255, 0.15);
}

/* Navigation Buttons */
.nav-btn {
  width: 100%;
  background: transparent;
  border: none;
  color: #fff;
  text-align: left;
  padding: 0.65rem 1rem;
  margin-bottom: 0.4rem;
  font-weight: 500;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.nav-btn:hover,
.nav-btn:focus {
  background-color: rgba(255, 255, 255, 0.1);
  color: #fff;
}

/* Remove Bootstrap caret */
.dropdown-toggle::after {
  display: none;
}
</style>
