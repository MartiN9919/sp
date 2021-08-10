import { getResponseAxios } from '@/plugins/axios_settings'

export default {
  state: {
    listOfPrimaryObjects: [],
    conflictingObjects: [],
  },
  getters: {
    listOfPrimaryObjects: state => { return state.listOfPrimaryObjects },
    primaryObject: state => id => { return state.listOfPrimaryObjects.find(object => object.id === id) },
  },
  mutations: {
    setListOfPrimaryObjects: (state, listObject) => { state.listOfPrimaryObjects = listObject },
  },
  actions: {
    getListOfPrimaryObjects({ commit, dispatch }, config = {}) {
      return getResponseAxios('objects/list_type/', config)
        .then(response => {
          commit('setListOfPrimaryObjects', response.data)
          dispatch('setDefaultRootSearchTreeGraph')
        })
        .catch(() => {})
    },
  }
}