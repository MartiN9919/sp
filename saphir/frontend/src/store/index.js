import Vue from 'vue'
import Vuex from 'vuex'
import authentication from './modules/authentication'
import treeview from './modules/treeview'
import modules_map from './modules/map/modules_map'
import alerts from './modules/alerts'
import socket from './modules/socket'
import report from './modules/report'
import map from './modules/map'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    authentication,
    treeview,
    map,
    report,
    alerts,
    socket,
    modules_map,
  }
})
