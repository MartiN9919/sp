import Vue from 'vue'
import Vuex from 'vuex'
//import UserSetting from "@/store/addition"
//console.log(1, UserSetting)
import siteControl from "@/store/modules/siteControl"
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
    siteControl,
    map,
  }
})

export default store
