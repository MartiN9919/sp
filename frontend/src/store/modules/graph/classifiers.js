import { getResponseAxios } from '@/plugins/axios_settings'

export default {
  state: {
    listOfClassifiersOfObjects: {},
  },
  getters: {
    classifiersForObject: state => objectId => { return state.listOfClassifiersOfObjects[objectId] },
    classifierObject: state => objectIds => {
      let classifiers = state.listOfClassifiersOfObjects[objectIds.objectId]
      return classifiers.find(classifier => classifier.id === objectIds.classifierId)}
  },
  mutations: {
    addListOfClassifiersOfObjects: (state, { objectId, classifiers }) => {
      let listClassifiers = Object.assign({}, state.listOfClassifiersOfObjects)
      listClassifiers[objectId] = classifiers
      state.listOfClassifiersOfObjects = listClassifiers

    }
  },
  actions: {
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