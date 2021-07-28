import { postResponseAxios } from '@/plugins/axios_settings'

export default {
  state: {
    searchTreeGraph: null,
    foundObjects: null,
  },
  getters: {
    searchTreeGraph: state => { return state.searchTreeGraph },
    foundObjects: state => { return state.foundObjects },
  },
  mutations: {
    setRootSearchTreeGraph: (state, rootObject) => { state.searchTreeGraph = rootObject },
    setActualRootSearchTree: (state, actual) => { state.searchTreeGraph.actual = actual },
    setFoundObjects: (state, objects) => { state.foundObjects = objects },
  },
  actions: {
    setRootSearchTreeGraph({ state, commit }, {objectId, actual=false}) {
      if (state.searchTreeGraph?.object_id !== objectId) {
        let rootObject = { object_id: objectId, rel: null, request: null, actual: actual, rels: [] }
        localStorage.setItem('searchDefaultIdGraph', objectId)
        commit('setRootSearchTreeGraph', rootObject)
      } else {
        commit('setActualRootSearchTree', actual)
      }
    },
    setDefaultRootSearchTreeGraph({ dispatch, rootGetters }) {
      let searchDefaultId = parseInt(localStorage.getItem('searchDefaultIdGraph')) || rootGetters.listOfPrimaryObjects[0].id
      dispatch('setRootSearchTreeGraph', { objectId: searchDefaultId })
    },
    findObjectsOnServer({ commit, rootState }, { searchTree, config={} }) {
      return postResponseAxios('objects/search', searchTree, config)
        .then(response => { commit('setFoundObjects', response.data) })
        .catch(error => {  })
    },
  }
}
