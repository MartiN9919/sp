import Vue      from 'vue'
import Vuex     from 'vuex'
import auth     from './modules/auth'
import treeview from './modules/treeview'
import map      from './modules/map/index'
import toolsMenuControl      from './modules/toolsMenuControl'
import alerts   from './modules/alerts'
import socket   from './modules/socket'
import report   from './modules/report'
import script   from './modules/script/index'
import graph from "./modules/graph/index";

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    auth,
    treeview,
    script,
    report,
    alerts,
    socket,
    map,
    toolsMenuControl,
    graph,
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
