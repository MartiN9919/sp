import Vue from 'vue'
import App from './App.vue'
import Map from './Map.vue'
import store from './store'

Vue.config.productionTip = false

new Vue({
  store,
  render: function (h) { return h(Map) }
}).$mount('#app')
