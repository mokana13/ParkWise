<template>
  <div class="bg-light min-vh-100 d-flex flex-column">
    <!-- Navbar -->
    <nav class="navbar bg-white shadow-sm px-4 py-2">
      <router-link
        to="/"
        class="navbar-brand d-flex align-items-center mb-0 text-dark text-decoration-none"
      >
        <img src="/images/parkwisee.png" alt="Parkwise Logo" class="logo-img" />
      </router-link>
    </nav>

    <!-- Centered Login Card -->
    <div class="flex-grow-1 d-flex justify-content-center align-items-center">
      <div class="card login-card shadow rounded-3 p-4 w-100">
        <div class="text-center mb-4">
          <h2 class="fw-bold mb-1">
            Login to <span class="text-primary">Parkwise</span>
          </h2>
          <p class="text-muted small mb-0">
            Secure your parking with one click
          </p>
        </div>

        <form @submit.prevent="handleLogin">
          <!-- Email -->
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input
              v-model="email"
              id="email"
              type="email"
              class="form-control form-control-lg rounded-3"
              placeholder="you@example.com"
              required
            />
          </div>

          <!-- Password -->
          <div class="mb-3 position-relative">
            <label for="password" class="form-label">Password</label>
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              id="password"
              class="form-control form-control-lg rounded-3 pe-5"
              placeholder="Password"
              required
            />
            <i
              :class="showPassword ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'"
              class="toggle-password-icon"
              @click="showPassword = !showPassword"
            ></i>
          </div>

          <!-- Submit -->
          <button
            type="submit"
            class="btn btn-primary w-100 py-2 rounded-3"
            :disabled="loading"
          >
            {{ loading ? 'Logging in...' : 'Login' }}
          </button>
        </form>

        <!-- Message in black -->
        <div class="mt-3 text-center text-dark small">{{ message }}</div>
        <div class="mt-3 text-center small">
          Don’t have an account?
          <router-link
            to="/register"
            class="text-primary fw-medium text-decoration-none"
          >
            Register
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      showPassword: false,
      message: '',
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.message = ''

      try {
        const res = await axios.post('http://127.0.0.1:5000/login', {
          email: this.email,
          password: this.password
        })

        const { access_token, role } = res.data

        localStorage.setItem('token', access_token)
        localStorage.setItem('role', role)
        localStorage.setItem('email', this.email)
        localStorage.setItem('password', this.password)

        this.message = 'Login successful! Redirecting...'
        const dashboardRoute =
          role === 'admin' ? '/admin-dashboard' : '/user/dashboard'
        setTimeout(() => this.$router.push(dashboardRoute), 800)
      } catch (err) {
        this.message =
          'Login failed: ' + (err.response?.data?.msg || 'Unknown error')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-card {
  max-width: 420px;
  padding: 1.5rem;
}

.logo-img {
  height: 32px;
  width: auto;
}

.toggle-password-icon {
  position: absolute;
  top: 70%;
  right: 1rem;
  transform: translateY(-50%);
  font-size: 1.25rem;
  color: #6c757d;
  cursor: pointer;
  z-index: 2;
}

/* Bump up input and button sizes back to original */
.form-control-lg {
  font-size: 1.125rem;
  height: 3rem;
}

.btn {
  font-size: 1rem;
  padding: 0.75rem;
}
</style>
