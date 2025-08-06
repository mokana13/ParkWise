<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light">
    <div class="profile-wrapper p-4">
      <h2 class="profile-title">Your Profile</h2>

      <!-- Loading / Error -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
      </div>
      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

      <!-- Profile Content -->
      <div v-else>
        <!-- Edit Mode -->
        <form v-if="editing" @submit.prevent="saveProfile" class="profile-form pt-2">
          <div class="mb-4">
            <label class="form-label">Full Name</label>
            <input v-model="form.fullname" type="text" class="form-control" required />
          </div>
          <div class="mb-4">
            <label class="form-label">Email</label>
            <input v-model="form.email" type="email" class="form-control" required />
          </div>
          <div class="mb-4">
            <label class="form-label">Address</label>
            <input v-model="form.address" type="text" class="form-control" required />
          </div>
          <div class="mb-4">
            <label class="form-label">Pincode</label>
            <input v-model="form.pincode" type="text" class="form-control" maxlength="6" required />
          </div>
        </form>

        <!-- Read-Only Mode -->
        <div v-else class="profile-details">
          <div class="detail-row">
            <span class="label">Full Name:</span>
            <span class="value">{{ user.fullname }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Email:</span>
            <span class="value">{{ user.email }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Address:</span>
            <span class="value">{{ user.address }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Pincode:</span>
            <span class="value">{{ user.pincode }}</span>
          </div>
        
        </div>

        <!-- Action Buttons -->
        <div class="d-flex justify-content-end gap-3 mt-4">
          <template v-if="!editing">
            <button class="btn btn-outline-secondary" @click="$router.go(-1)">← Back</button>
            <button class="btn btn-outline-primary" @click="editing = true">Edit</button>
          </template>
          <template v-else>
            <button type="button" class="btn btn-outline-danger" @click="editing = false">Cancel</button>
            <button type="submit" class="btn btn-primary" @click="saveProfile">Save Changes</button>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'UserProfile',
  data() {
    return {
      user: null,
      loading: true,
      error: '',
      editing: false,
      form: {
        fullname: '',
        email: '',
        address: '',
        pincode: ''
      }
    }
  },
  async mounted() {
    const token = localStorage.getItem('token')
    if (!token) return this.$router.push('/login')

    try {
      const res = await axios.get('http://localhost:5000/user/profile', {
        headers: { Authorization: `Bearer ${token}` }
      })
      this.user = res.data
      Object.assign(this.form, this.user)
    } catch (err) {
      console.error(err)
      this.error = err.response?.data?.msg || 'Failed to load profile.'
    } finally {
      this.loading = false
    }
  },
  methods: {
    async saveProfile() {
      this.error = ''
      const token = localStorage.getItem('token')
      try {
        await axios.put(
          'http://localhost:5000/user/profile',
          { ...this.form },
          { headers: { Authorization: `Bearer ${token}` } }
        )
        this.user = { ...this.user, ...this.form }
        this.editing = false
      } catch (err) {
        console.error(err)
        this.error = err.response?.data?.msg || 'Failed to update profile.'
      }
    }
  }
}
</script>

<style scoped>
.profile-wrapper {
  max-width: 720px;
  width: 100%;
  background: #fff;
  border-radius: .5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.12);
  padding: 2rem;
}

.profile-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #000;
  margin-bottom: 1.5rem;
}

.profile-form .form-label {
  font-weight: 600;
}

.form-control {
  border-radius: .375rem;
  border: 1px solid #ccc;
  padding: .6rem .85rem;
  font-size: 1.05rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.label {
  font-weight: 600;
  color: #555;
  font-size: 1.05rem;
}

.value {
  color: #333;
  font-size: 1.05rem;
}
</style>
