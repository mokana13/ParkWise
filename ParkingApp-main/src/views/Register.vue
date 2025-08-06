<template>
  <div class="bg-light min-vh-100 d-flex flex-column">
    <!-- Brand Navbar -->
    <nav class="navbar bg-white shadow-sm px-4 py-2">
      <router-link
        to="/"
        class="navbar-brand d-flex align-items-center mb-0 text-dark text-decoration-none"
      >
        <img
          src="/images/parkwisee.png"
          alt="Parkwise Logo"
          class="logo-img"
        />
      </router-link>
    </nav>

    <!-- Centered Registration Card -->
    <div class="flex-grow-1 d-flex justify-content-center align-items-center">
      <div class="card register-card shadow rounded p-3">
        <div class="text-center mb-3">
          <h4 class="fw-bold mb-1">
            Create Your <span class="text-success">Parkwise</span> Account
          </h4>
          <p class="text-muted small mb-2">
            Get started with seamless parking access
          </p>
        </div>

        <form @submit.prevent="handleRegister">
          <!-- Full Name -->
          <div class="mb-2">
            <label for="fullname" class="form-label small">Full Name</label>
            <input
              v-model="fullname"
              id="fullname"
              class="form-control form-control-sm"
              placeholder="Your full name"
              required
            />
          </div>

          <!-- Email -->
          <div class="mb-2">
            <label for="email" class="form-label small">Email</label>
            <input
              v-model="email"
              id="email"
              type="email"
              class="form-control form-control-sm"
              placeholder="you@example.com"
              required
            />
          </div>

          <!-- Password -->
          <div class="mb-2 position-relative">
            <label for="password" class="form-label small">Password</label>
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              id="password"
              class="form-control form-control-sm pe-4"
              placeholder="Password"
              required
            />
            <i
              :class="showPassword ? 'bi bi-eye-slash-fill' : 'bi bi-eye-fill'"
              class="password-eye"
              @click="showPassword = !showPassword"
            ></i>
          </div>

          <!-- Address -->
          <div class="mb-2">
            <label for="address" class="form-label small">Address</label>
            <textarea
              v-model="address"
              id="address"
              class="form-control form-control-sm"
              placeholder="123 Main St"
              rows="2"
              required
            ></textarea>
          </div>

          <!-- Pincode -->
          <div class="mb-3">
            <label for="pincode" class="form-label small">Pincode</label>
            <input
              v-model="pincode"
              id="pincode"
              type="text"
              class="form-control form-control-sm"
              placeholder="600001"
              maxlength="6"
              pattern="\d{6}"
              required
            />
          </div>

          <button
            type="submit"
            class="btn btn-success btn-sm w-100 py-1"
            :disabled="loading"
          >
            {{ loading ? 'Registering...' : 'Register' }}
          </button>
        </form>

        <div class="mt-2 text-center text-muted small">{{ message }}</div>
        <div class="mt-3 text-center small">
          <span class="text-dark">Already have an account? </span>
          <router-link
            to="/login"
            class="text-success fw-semibold text-decoration-none"
          >
            Login
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    return {
      fullname: '',
      email: '',
      password: '',
      address: '',
      pincode: '',
      showPassword: false,
      message: '',
      loading: false
    }
  },
  methods: {
    async handleRegister() {
      this.loading = true
      this.message = ''

      try {
        await axios.post('http://127.0.0.1:5000/register', {
          fullname: this.fullname,
          email: this.email,
          password: this.password,
          address: this.address,
          pincode: this.pincode
        })

        this.message = 'Registered successfully! Logging you in...'

        const loginRes = await axios.post('http://127.0.0.1:5000/login', {
          email: this.email,
          password: this.password
        })

        const { access_token, role } = loginRes.data
        localStorage.setItem('token', access_token)
        localStorage.setItem('role', role)
        localStorage.setItem('username', this.fullname)

        // ← Redirect updated here to match your router
        const redirect = role === 'admin'
          ? '/admin-dashboard'
          : '/user/dashboard'

        setTimeout(() => this.$router.push(redirect), 800)
      } catch (err) {
        this.message =
          'Registration failed: ' +
          (err.response?.data?.msg || err.message || 'Unknown error')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
/* Slightly larger registration card */
.register-card {
  width: 100%;
  max-width: 400px; /* was 360px */
  padding: 1.25rem; /* adds more breathing room */
}

/* Show/hide password icon */
.password-eye {
  position: absolute;
  top: 70%;
  right: 0.75rem;
  transform: translateY(-50%);
  font-size: 1.1rem; /* slight increase */
  color: #6c757d;
  cursor: pointer;
  z-index: 10;
}

/* Logo unchanged */
.logo-img {
  height: 32px;
  width: auto;
  object-fit: contain;
}

/* Optional: form-control size tweak */
input.form-control,
textarea.form-control {
  font-size: 0.95rem;
  padding: 0.45rem 0.75rem;
}

label.form-label {
  font-size: 0.92rem;
}

button.btn {
  font-size: 0.95rem;
}
</style>
