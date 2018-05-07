<template>
  <div id="app">
    <h1>Movie Recommendations</h1>
    <Gplaces/>
  </div>
</template>

<script>
import Gplaces from './components/HelloWorld.vue'

export default {
  name: 'app',
  components: {
    Gplaces
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
