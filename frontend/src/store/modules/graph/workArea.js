import { postResponseAxios } from '@/plugins/axios_settings'

export default {
  state: {
    positionNewGraphObject: null,
    selectedGraphObjectId: null,
  },
  getters: {
    positionNewGraphObject: state => { return state.positionNewGraphObject },
    selectedGraphObjectId: state => { return state.selectedGraphObjectId },
  },
  mutations: {
    setSelectedGraphObjectId: (state, id) => {
      state.selectedGraphObjectId = id
    },
    setPositionNewGraphObject: (state, position) => {
      state.positionNewGraphObject = position
    }
  },
  actions: {
    setSelectedGraphObjectId({ commit }, id) { commit('setSelectedGraphObjectId', id) },
    setPositionNewGraphObject({ commit }, position) { commit('setPositionNewGraphObject', position) },
    findObjectsOnServer({ commit, rootState }, props = {}) {
      return postResponseAxios('objects/search', props.searchTree, props?.config)
        .then(response => {
          return Promise.resolve(response)
        })
        .catch(error => { return Promise.reject(error) })
    },
  }
}
