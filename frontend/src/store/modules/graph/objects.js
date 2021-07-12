import { getResponseAxios, postResponseAxios } from '@/plugins/axios_settings'
import { getActiveObject, getObjectFromWorkArea } from './index'

export default {
  state: {
    listOfPrimaryObjects: [],
  },
  getters: {
    listOfPrimaryObjects: state => { return state.listOfPrimaryObjects },
    primaryObject: state => id => { return state.listOfPrimaryObjects.find(object => object.id === id) },
  },
  mutations: {
    setListOfPrimaryObjects: (state, listObject) => { state.listOfPrimaryObjects = listObject },
    setFoundObjects: (state, response) => { response.activeObject.foundObjects = response.foundObjects },
    createNewObject(state, props) { props.object.params = props.classifier },
  },
  actions: {
    getListOfPrimaryObjects({commit}, config = {}) {
      return getResponseAxios('objects/list_type/', config)
        .then(response => { commit('setListOfPrimaryObjects', response.data) })
        .catch(() => {})
    },
    findObjectsOnServer({ commit, rootState }, config = {}) {
      let activeObject = getActiveObject(rootState)
      return postResponseAxios('objects/search', activeObject.searchTree, config)
        .then(response => {
          commit('setFoundObjects', { activeObject: activeObject, foundObjects: response.data })
          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) })
    },
    createNewObject({ commit, rootState }, object) {
      let neededClassifiers = []
      for (let classifier of rootState.graph.classifiers.listOfClassifiersOfObjects[object.object_id])
        if (classifier.need) neededClassifiers.push({ id: classifier.id, value: null, })
      commit('createNewObject', {
        classifier: neededClassifiers,
        object: getObjectFromWorkArea(rootState, object.tempId)
      })
    },
    createNewObjectFromServer({ commit, rootState }, config = {}) {
      let findObject = getActiveObject(rootState)
      let classifiers = []
      for (let classifier of findObject.params)
        if (classifier?.changed) {
          classifiers.push({id: classifier.id, value: classifier.value})
          delete classifier.changed
        }
      if (classifiers.length) {
        let request = { object_id: findObject.object_id, rec_id: findObject.rec_id, params: classifiers, }
        return postResponseAxios('objects/object', request, config)
          .then(response => {
            findObject.rec_id = response.data.object.rec_id
            findObject.params = response.data.object.params
          })
          .catch(() => {
          })
      }
    },
  }
}