import { postResponseAxios } from '@/plugins/axios_settings'


export default {
  state: {
    workAreaOfObjects: [],
    activeObjectId: null,
  },
  getters: {
    workAreaOfObjects: state => {
      return state.workAreaOfObjects
    },
    activeObject: state => {
      return state.workAreaOfObjects.find(object => object.tempId === state.activeObjectId)
    },
    windowActiveObject: state => {
      return state.workAreaOfObjects.find(object => object.tempId === state.activeObjectId)?.activeWindow
    },
    foundObjects: state => id => {
      return state.workAreaOfObjects.find(object => object.tempId === id).foundObjects
    },
  },
  mutations: {
    addObjectInWorkAreaOfObjects: (state, object) => {
      state.workAreaOfObjects.push(object)
    },
    removeObjectInWorkAreaAboveObjects: (state, id) => {
      let objectIndex = state.workAreaOfObjects.findIndex(object => object.tempId === id)
      state.workAreaOfObjects.splice(objectIndex, 1)
    },
    setActiveObjectId: (state, id) => {
      state.activeObjectId = id
    },
    findObjectOnServer: (state, objects) => {
      state.workAreaOfObjects.find(object => object.tempId === state.activeObjectId).foundObjects = objects
    },
    createNewObject(state, props) {
      let findObject = state.workAreaOfObjects.find(object => object.tempId === props.tempId)
      findObject.params = props.classifier
    },
    addClassifierToObject: (state, props) => {
      let findObject = state.workAreaOfObjects.find(object => object.tempId === props.tempId)
      findObject.params.push(props.classifier)
    }
  },
  actions: {
    addObjectInWorkAreaOfObjects ({ commit, state }, id) {
      let tempId = Number(Date.now().toString() + state.workAreaOfObjects.length.toString())
      commit('addObjectInWorkAreaOfObjects', {
        tempId: tempId,
        object_id: id,
        rec_id: 0,
        activeWindow: 'searchTree',
        searchTree: { object_id: id, rel_id: 0, request: '', rels: [], },
        foundObjects: [],
        params: [],
      })
      commit('setActiveObjectId', tempId)
    },
    removeObjectInWorkAreaAboveObjects ({ commit, state }, id) {
      commit('removeObjectInWorkAreaAboveObjects', id)
      if (state.workAreaOfObjects.length)
        commit('setActiveObjectId', state.workAreaOfObjects[state.workAreaOfObjects.length - 1].tempId)
      else commit('setActiveObjectId')
    },
    setActiveObjectId ({commit}, id) {
      commit('setActiveObjectId', id)
    },
    findObjectsOnServer({ commit, state }, config = {}) {
      let searchTree = state.workAreaOfObjects.find(object => object.tempId === state.activeObjectId)
      return postResponseAxios('objects/search', searchTree.searchTree, config)
        .then(response => {
          commit('findObjectOnServer', response.data)
          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) })
    },
    createNewObject({ commit, state, rootState }, object) {
      let neededClassifiers = []
      for (let classifier of rootState.graph.classifiers.listOfClassifiersOfObjects[object.object_id])
        if (classifier.need)
          neededClassifiers.push({ id: classifier.id, value: null, })
      commit('createNewObject', {
        classifier: neededClassifiers,
        tempId: object.tempId
      })
    },
    addClassifierToObject({ commit }, props) {
      commit('addClassifierToObject', props)
    },
  }
}
