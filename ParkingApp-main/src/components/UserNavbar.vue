<template>
  <nav class="navbar navbar-expand-md bg-white shadow-sm py-2 px-3 sticky-top modern-navbar">
    <!-- Brand -->
    <router-link :to="dashboardRoute" class="navbar-brand d-flex align-items-center gap-2 text-dark fw-bold">
      <img src="/images/parkwisee.png" alt="Parkwise Logo" class="logo-img" />
    </router-link>

    <!-- Toggle button for mobile -->
    <button class="navbar-toggler border-0" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
      <i class="bi bi-list fs-3 text-dark"></i>
    </button>

    <!-- Nav Links -->
    <div class="collapse navbar-collapse justify-content-center" id="navbarNav">
      <ul class="navbar-nav gap-3">
        <li class="nav-item">
          <router-link to="/user/dashboard" class="nav-link modern-link">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/user/reservations" class="nav-link modern-link">Reservations</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/user/summary" class="nav-link modern-link">Summary</router-link>
        </li>
      </ul>
    </div>

    <!-- User Dropdown -->
    <div v-if="username" class="dropdown ms-auto">
      <button class="btn btn-outline-light d-flex align-items-center gap-2 rounded-pill px-3 shadow-sm user-button"
        type="button" data-bs-toggle="dropdown">
        <i class="bi bi-person-circle fs-5 text-primary"></i>
        <span class="fw-semibold text-dark d-none d-sm-inline username-placeholder">
          {{ username || '&nbsp;' }}
        </span>
      </button>
      <ul class="dropdown-menu dropdown-menu-end shadow-sm rounded-3 mt-2">
        <li>
          <router-link to="/user/profile" class="dropdown-item">
            <i class="bi bi-person me-2"></i> Profile
          </router-link>
        </li>
        <li>
          <hr class="dropdown-divider" />
        </li>
        <li>
          <a class="dropdown-item text-danger" href="#" @click.prevent="logout">
            <i class="bi bi-box-arrow-right me-2"></i> Logout
          </a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'UserNavbar',
  props: ['username'],
  computed: {
    dashboardRoute() {
      const role = localStorage.getItem('role');
      return role === 'admin' ? '/admin-dashboard' : '/user/dashboard';
    }
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.logo-img {
  height: 32px;
  object-fit: contain;
}

.modern-navbar {
  backdrop-filter: blur(8px);
  background-color: rgba(255, 255, 255, 0.85);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  z-index: 1050;
}

.modern-link {
  font-weight: 500;
  font-size: 0.95rem;
  color: #212529 !important;
  position: relative;
  transition: color 0.2s ease;
}

.modern-link::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0%;
  height: 2px;
  background-color: #0d6efd;
  transition: width 0.3s ease;
}

.modern-link:hover::after {
  width: 100%;
}

.username-placeholder {
  display: inline-block;
  min-width: 80px;
  text-align: left;
}


.user-button:hover {
  background-color: #f8f9fa;
}

.dropdown-menu {
  font-size: 0.9rem;
}
</style>
