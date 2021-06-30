import { getResponseAxios } from '@/plugins/axios_settings'

export default {
  state: {
    listOfClassifiersOfObjects: {},
  },
  getters: {
    listOfClassifiersOfObjects: state => id => {
      return state.listOfClassifiersOfObjects[id]
    },
    classifiersForObjects: state => objectId => {
      return state.listOfClassifiersOfObjects[objectId]
    },
  },
  mutations: {
    addListOfClassifiersOfObjects: (state, { objectId, classifiers }) => {
      state.listOfClassifiersOfObjects[objectId] = classifiers
    },
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