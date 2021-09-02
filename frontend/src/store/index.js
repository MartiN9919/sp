import Vue      from 'vue'
import Vuex     from 'vuex'
import siteControl from './modules/siteControl/index'
import map      from './modules/map/index'
import graph from "./modules/graph/index"
import treeview from './modules/treeview'
import report   from './modules/report'
import script   from './modules/script/index'

Vue.use(Vuex)

const store = new Vuex.Store({
  modules: {
    siteControl,
    treeview,
    script,
    report,
    map,
    graph,
  }
})

export default store
