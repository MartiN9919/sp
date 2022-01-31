import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import vuetify from './plugins/vuetify'
import CONST from '@/plugins/const'
import { VueMaskDirective } from 'v-mask'

Vue.directive('mask', VueMaskDirective)

Vue.config.productionTip = false
Vue.prototype.$CONST = CONST

new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
