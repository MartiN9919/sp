import Vue from 'vue'
import Vuex from 'vuex'
//import UserSetting from "@/store/addition"
//console.log(1, UserSetting)
import map from "@/store/modules/map"

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
  },
  getters: {
  },
  mutations: {
  },
  actions: {
  },
  modules: {
    map,
  }
})

export default store
