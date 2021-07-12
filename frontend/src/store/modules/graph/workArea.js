export default {
  state: {
    workAreaOfObjects: [],
    activeObjectId: null,
  },
  getters: {
    workAreaOfObjects: state => { return state.workAreaOfObjects },
    workAreaOfObject: state => id => { return state.workAreaOfObjects.find(object => object.tempId === id) },
    activeObject: state => { return state.workAreaOfObjects.find(object => object.tempId === state.activeObjectId) },
    foundObjects: state => id => { return state.workAreaOfObjects.find(object => object.tempId === id).foundObjects },
    windowActiveObject: state => {
      return state.workAreaOfObjects.find(object => object.tempId === state.activeObjectId)?.activeWindow
    },
  },
  mutations: {
    addObjectInWorkArea: (state, object) => { state.workAreaOfObjects.push(object) },
    setActiveObjectId: (state, id) => { state.activeObjectId = id },
    removeObjectInWorkArea: (state, id) => {
      state.workAreaOfObjects.splice(state.workAreaOfObjects.findIndex(object => object.tempId === id), 1)
    },
  },
  actions: {
    addObjectInWorkArea ({ commit, state }, id) {
      let tempId = Number(Date.now().toString() + state.workAreaOfObjects.length.toString())
      commit('addObjectInWorkArea', {
        tempId: tempId,
        object_id: id,
        rec_id: 0,
        activeWindow: 'searchTree',
        searchTree: {
          object_id: id,
          rel: {
            id: 0,
            value: null,
            date_time_start: null,
            date_time_end: null,
          },
          request: '',
          actual: false,
          rels: [],
        },
        foundObjects: [],
        params: [],
      })
      commit('setActiveObjectId', tempId)
    },
    removeObjectInWorkArea ({ commit, state }, id) {
      commit('removeObjectInWorkArea', id)
      if (state.workAreaOfObjects.length)
        commit('setActiveObjectId', state.workAreaOfObjects[state.workAreaOfObjects.length - 1].tempId)
      else commit('setActiveObjectId')
    },
    setActiveObjectId ({commit}, id) {
      commit('setActiveObjectId', id)
    },
  }
}
