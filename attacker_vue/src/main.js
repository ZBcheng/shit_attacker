import Vue from 'vue'
import App from './App.vue'

import '../static/css/icons.css'
import '../static/css/materialize.min.css'

import '../static/js/jquery.min.js'
import '../static/js/materialize.js'
import '../static/js/materialize.min.js'


Vue.config.productionTip = false


new Vue({
  render: h => h(App),
}).$mount('#app')
