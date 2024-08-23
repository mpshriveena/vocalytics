<script setup>
import NavBar from './views/NavBar.vue'
</script>

<template>
  <div id="app">
    <NavBar/>
    <router-view/>
  </div>
</template>

export default {
  name: 'App',
  components: {
    NavBar,

  },
}
<style>
body {
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  font-family: 'Poppins', 'sans-serif';
}
</style>