import Vue from 'vue'
import Vuetify from 'vuetify/lib/framework'
import ru from 'vuetify/lib/locale/ru'
import '@mdi/font/css/materialdesignicons.css'

Vue.use(Vuetify)

export default new Vuetify({
  lang: {
    locales: { ru },
    current: 'ru',
  },
})
