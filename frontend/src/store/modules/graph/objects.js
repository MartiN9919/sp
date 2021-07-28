import { getResponseAxios, postResponseAxios } from '@/plugins/axios_settings'
import { getActiveObject, getObjectFromWorkArea } from './index'

export default {
  state: {
    listOfPrimaryObjects: [],
    conflictingObjects: [],
  },
  getters: {
    listOfPrimaryObjects: state => { return state.listOfPrimaryObjects },
    primaryObject: state => id => { return state.listOfPrimaryObjects.find(object => object.id === id) },
    conflictingObjects: state => { return state.conflictingObjects },
  },
  mutations: {
    setListOfPrimaryObjects: (state, listObject) => { state.listOfPrimaryObjects = listObject },
    addConflictingObjects: (state, objects) => { state.conflictingObjects = objects },
    clearConflictingObjects: (state) => { state.conflictingObjects = [] },
    changeConflictingObjects: (state, newObject) => {
      let indexOldObject = state.conflictingObjects.findIndex(object => object.rec_id === newObject.rec_id)
      state.conflictingObjects[indexOldObject] = newObject
    }
  },
  actions: {
    clearConflictingObjects({ commit }) { commit('clearConflictingObjects') },
    changeConflictingObjects({ commit }, object) { commit('changeConflictingObjects', object) },
    getListOfPrimaryObjects({ commit, dispatch }, config = {}) {
      return getResponseAxios('objects/list_type/', config)
        .then(response => {
          commit('setListOfPrimaryObjects', response.data)
          dispatch('setDefaultRootSearchTreeGraph')
        })
        .catch(() => {})
    },
    createNewObjectFromServer({ commit, rootState }, props = {}) {
      let findObject = props?.object ? props.object : getActiveObject(rootState)
      let classifiers = []
      for (let classifier of findObject.params)
        if (classifier?.changed) {
          classifiers.push({id: classifier.id, value: classifier.value})
        }
      if (classifiers.length) {
        let request = { object_id: findObject.object_id, rec_id: findObject.rec_id, params: classifiers, }
        return postResponseAxios('objects/object', request, props?.config)
          .then(response => {
            if (response.data.status === 1) {
              findObject.rec_id = response.data.object.rec_id
              findObject.params = response.data.object.params
              for (let classifier of findObject.params)
                delete classifier.changed
            }
            if (response.data.status === 2) {
              commit('addConflictingObjects', response.data.objects)
            }
          })
          .catch(() => {
          })
      }
    },
  }
}