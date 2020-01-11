<template>
  <div id="app">
    <Index />
    <!-- <h1>hello</h1> -->
  </div>
</template>

<script src="/static/js/jquery.min.js"></script>
<script src="/static/js/materialize.min.js"></script>

<script>
  import Index from './components/Index.vue'

  export default {
    name: 'app',
    components: {
      Index
    },
  }
</script>

<style>
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 0px;
  }
</style>