<script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div id="app">
    <router-view />
  </div>
</template>


<style>
/* Global fix: remove margin/padding + no scroll leaks */
html, body, #app {
  height: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}
html {
  overflow-y: scroll;
}

/* Optional: remove any default spacing from Bootstrap container if you're using one */
.container {
  padding: 0 !important;
  margin: 0 !important;
}


</style>
