import { getResponseAxios } from '@/plugins/axios_settings'
import { getObjectFromWorkArea } from "./index";

export default {
  state: {
    listOfClassifiersOfObjects: {},
  },
  getters: {
    listOfClassifiersOfObjects: state => id => { return state.listOfClassifiersOfObjects[id] },
    classifiersForObjects: state => objectId => { return state.listOfClassifiersOfObjects[objectId] },
  },
  mutations: {
    addClassifierToObject: (state, { object, classifier }) => { object.params.push(classifier) },
    addListOfClassifiersOfObjects: (state, { objectId, classifiers }) => {
      state.listOfClassifiersOfObjects[objectId] = classifiers
    }
  },
  actions: {
    addClassifierToObject({ commit, rootState }, props) {
      commit('addClassifierToObject', {
        object: getObjectFromWorkArea(rootState, props.tempId),
        classifier: props.classifier
      })
    },
    getListOfClassifiersOfObjects ({ commit, state }, config = {}) {
      let objectId = config.params.object_id
      if (!(objectId in state.listOfClassifiersOfObjects))
        return getResponseAxios('objects/list_classifier/', config)
          .then(response => {
            commit('addListOfClassifiersOfObjects', { objectId: objectId, classifiers: response.data, })
            return Promise.resolve(response)
          })
          .catch(error => { return Promise.reject(error) })
    },
  },
}