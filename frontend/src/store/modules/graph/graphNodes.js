import { getResponseAxios } from '@/plugins/axios_settings'


export default {
  state: {
    choosingObjects: [],
    objectsRelations: [],
  },
  getters: {
    choosingObjects: state => { return state.choosingObjects },
    objectsRelations: state => { return state.objectsRelations },
    lastObject: state => {
      let object = state.choosingObjects[state.choosingObjects.length - 1]
      return object ? object : null
    }
  },
  mutations: {
    addChoosingObject: (state, choosingObject) => { state.choosingObjects.push(choosingObject) },
    addObjectsRelation: (state, objectsRelation) => { state.objectsRelations.push(objectsRelation) },

  },
  actions: {
    addChoosingObject({ commit, }, choosingObject) {
        commit('addChoosingObject', choosingObject)
    },
  },
}