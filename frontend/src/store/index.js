import Vue      from 'vue'
import Vuex     from 'vuex'
import siteControl from "@/store/modules/siteControl"
import treeview from "@/store/modules/treeview"
import script from "@/store/modules/script"
import map from "@/store/modules/map"
import report from "@/store/modules/report"
import graph from "@/store/modules/graph"
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
