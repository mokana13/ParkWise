<template>
  <div class="home-wrapper">
    <div class="home-container text-center">
      <div class="content">
        <h1 class="display-3 fw-bold mb-3 fade-in">
          Welcome to <span class="text-primary">Parkwise</span>
        </h1>
        <p class="lead mb-4 fade-in delay-1">
          Intelligent 4-wheeler parking management. For operators. For drivers. For real-world scale.
        </p>
        <div class="fade-in delay-2">
          <router-link to="/login" class="btn btn-lg btn-primary me-3 px-4 py-2 shadow-sm">Login</router-link>
          <router-link to="/register" class="btn btn-lg btn-outline-secondary px-4 py-2">Register</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
}
</script>

<!-- ✅ GLOBAL STYLES (not scoped) -->
<style>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden !important;
}
</style>

<!-- ✅ COMPONENT-SCOPED STYLES -->
<style scoped>
.home-wrapper {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #fdfdfd, #e9ecef);
  color: #212529;
}

.home-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.content {
  max-width: 720px;
  padding: 0 1rem;
}

/* Animations */
.fade-in {
  opacity: 0;
  transform: translateY(10px);
  animation: fadeInUp 0.8s ease forwards;
}

.fade-in.delay-1 {
  animation-delay: 0.3s;
}

.fade-in.delay-2 {
  animation-delay: 0.6s;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
