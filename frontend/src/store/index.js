import Vue      from 'vue'
import Vuex     from 'vuex'
import siteControl from './modules/siteControl'
import map      from './modules/map'
import graph    from './modules/graph'
import treeview from './modules/treeview'
import report   from './modules/report'
import script   from './modules/script'
import _ from 'lodash'

Vue.use(Vuex)

const initialStoreModules = {siteControl, treeview, script, report, map, graph}

const createClearState = function (module=initialStoreModules) {
  let newState = {}
  for (const [key, value] of Object.entries(module))
    newState[key] = value.hasOwnProperty('modules')
      ? createClearState(Object.assign(value.modules))
      : _.cloneDeep(value.state)
  return newState
}

const store = new Vuex.Store({
  modules: _.cloneDeep(initialStoreModules),
  mutations: {
    resetState: () => store.replaceState(createClearState()),
  }
})

export default store
