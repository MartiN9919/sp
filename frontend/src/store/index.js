import Vue      from 'vue'
import Vuex     from 'vuex'
import auth     from './modules/auth'
import treeview from './modules/treeview'
import map      from './modules/map/index'
import alerts   from './modules/alerts'
import socket   from './modules/socket'
import report   from './modules/report'
import graph   from './modules/graph'
import script   from './modules/script/index'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    auth,
    graph,
    treeview,
    script,
    report,
    alerts,
    socket,
    map,
  }
})

export default store

// export default {
//   store: new Vuex.Store({
//     modules: {
//       auth,
//       treeview,
//       script,
//       report,
//       alerts,
//       socket,
//       modules_map,
//     },
//   }),
// }
